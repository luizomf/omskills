#!/usr/bin/env python3
"""Focused structural and executable state-machine checks for dispatch-tickets."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = ROOT / "skills/engineering/dispatch-tickets/SKILL.md"
MANIFEST_ENTRY = "./skills/engineering/dispatch-tickets"
EXPECTED_PROMPT = """Repository: <repository>
Ticket: <ticket>
Load and follow installed `orchestrate`. Resolve all governing context and complete this Ticket yourself.
Return exactly one single-line JSON object with required string fields \"ticket\": \"<ticket>\" and \"status\": one of \"delivered\", \"blocked\", \"failed\", or \"cancelled\". Include non-empty string \"ref\" only for an essential durable reference and non-empty string \"blocker\" only when applicable. Include no other fields or output."""
IDENTITY = re.compile(
    r"\A[A-Za-z0-9._-]+/[A-Za-z0-9._-]+#[1-9][0-9]*\Z"
)


def require(text: str, *fragments: str) -> None:
    for fragment in fragments:
        assert fragment in text, f"missing contract fragment: {fragment}"


class ObjectPairs(list[tuple[str, object]]):
    """Distinguish decoded JSON objects from arrays and retain duplicate keys."""


ALLOWED_STATUSES = {"delivered", "blocked", "failed", "cancelled"}
ALLOWED_KEYS = {"ticket", "status", "ref", "blocker"}


def validate_input(tickets: list[str], authorized: bool) -> str:
    if not authorized:
        return "authorization"
    if not tickets:
        return "empty"
    if any(not isinstance(ticket, str) or not IDENTITY.fullmatch(ticket) for ticket in tickets):
        return "identity-syntax"
    if len(tickets) != len(set(tickets)):
        return "duplicate"
    return "accepted"


def validate_outcome(message: str, expected_ticket: str) -> tuple[str, dict[str, str]]:
    trimmed = message.strip()
    if "\n" in trimmed or "\r" in trimmed:
        return "syntax", {}
    try:
        decoded = json.loads(trimmed, object_pairs_hook=ObjectPairs)
    except (json.JSONDecodeError, TypeError):
        return "syntax", {}
    if not isinstance(decoded, ObjectPairs):
        return "shape", {}

    keys = [key for key, _ in decoded]
    if len(keys) != len(set(keys)):
        return "shape", {}
    outcome = dict(decoded)
    if not {"ticket", "status"} <= outcome.keys() or outcome.keys() - ALLOWED_KEYS:
        return "shape", {}
    if not isinstance(outcome["ticket"], str) or not isinstance(
        outcome["status"], str
    ):
        return "shape", {}
    if any(
        key in outcome
        and (not isinstance(outcome[key], str) or not outcome[key])
        for key in ("ref", "blocker")
    ):
        return "shape", {}
    if outcome["ticket"] != expected_ticket:
        return "identity", {}
    if outcome["status"] not in ALLOWED_STATUSES:
        return "status", {}
    return "accepted", outcome


@dataclass(frozen=True)
class CoordinatorReturn:
    coordinator: int
    path: str
    message: str | None
    outer_status: str = "completed"
    truncated: bool = False
    return_count: int = 1
    session: str | None = None


@dataclass(frozen=True)
class InterruptRequest:
    coordinator: int
    accepted: bool = True


@dataclass(frozen=True)
class OutcomeRecord:
    ticket: str
    status: str
    ref: str | None = None
    blocker: str | None = None
    session: str | None = None
    reason: str | None = None


@dataclass
class Mission:
    tickets: tuple[str, ...]
    mode: str
    cursor: int = 0
    state: str = "ready"
    coordinator: int | None = None
    active_session: str | None = None
    cancellation_intent: tuple[str, int] | None = None
    pending_failure: OutcomeRecord | None = None
    outcomes: list[OutcomeRecord] = field(default_factory=list)
    settled_coordinators: set[int] = field(default_factory=set)
    events: list[tuple[object, ...]] = field(default_factory=list)
    max_active: int = 0

    @classmethod
    def accept(cls, tickets: list[str], authorized: bool, mode: str) -> Mission:
        result = validate_input(tickets, authorized)
        if result != "accepted":
            raise ValueError(result)
        assert mode in {"interactive", "print"}
        return cls(tuple(tickets), mode)

    @property
    def current_ticket(self) -> str:
        return self.tickets[self.cursor]

    def start(self, coordinator: int, session: str | None = None) -> str | None:
        if self.state != "ready" or self.coordinator is not None:
            raise RuntimeError("coordinator already active or Mission not dispatchable")
        if coordinator in self.settled_coordinators:
            raise RuntimeError("coordinator identity was already settled")

        ticket = self.current_ticket
        self.coordinator = coordinator
        self.active_session = session
        self.state = "dispatched"
        self.max_active = max(self.max_active, 1)
        delivery = "async" if self.mode == "interactive" else "direct"
        self.events.append(("start", ticket, coordinator, delivery))
        if self.mode == "print":
            return None
        if self.cursor:
            prior = self.outcomes[-1]
            return (
                f"{format_record(prior)}; {self.cursor}/{len(self.tickets)} delivered; "
                f"{ticket} dispatched (#{coordinator}); root available; outcome pending."
            )
        return f"{ticket} dispatched (#{coordinator}); root available; outcome pending."

    def reject_start(self, reason: str = "transport", session: str | None = None) -> str:
        if self.state != "ready" or self.coordinator is not None:
            raise RuntimeError("Mission not awaiting a coordinator start")
        record = OutcomeRecord(
            ticket=self.current_ticket,
            status="failed",
            session=session,
            reason=f"dispatch-{reason}",
        )
        self.outcomes.append(record)
        self.events.append(("start-rejected", record.ticket, record.reason))
        self.state = "stopped"
        return self._terminal_report(current_not_dispatched=True)

    def receive(self, result: CoordinatorReturn) -> str:
        if self.state == "cancelling":
            return self._receive_cancellation_pong(result)
        if self.state == "cleanup":
            return self._receive_cleanup_pong(result)
        if self.coordinator is None:
            reason = (
                "duplicate-return"
                if result.coordinator in self.settled_coordinators
                else "unexpected-return"
            )
            return self._fail(reason, result.session, result.coordinator)

        expected_path = "pong" if self.mode == "interactive" else "direct"
        if result.return_count != 1:
            return self._fail("duplicate-return", result.session)
        if result.path != expected_path:
            return self._fail("wrong-path", result.session)
        if result.coordinator != self.coordinator:
            reason = (
                "duplicate-return"
                if result.coordinator in self.settled_coordinators
                else "mismatched-return"
            )
            if self.mode == "interactive":
                return self._begin_cleanup_failure(
                    reason, result.session, result.coordinator
                )
            return self._fail(reason, result.session, result.coordinator)
        if result.truncated:
            return self._fail("truncated", result.session)
        if result.outer_status != "completed":
            return self._fail("transport", result.session)
        if result.message is None:
            return self._fail("missing", result.session)

        validation, outcome = validate_outcome(result.message, self.current_ticket)
        if validation != "accepted":
            return self._fail(f"outcome-{validation}", result.session)

        record = OutcomeRecord(
            ticket=outcome["ticket"],
            status=outcome["status"],
            ref=outcome.get("ref"),
            blocker=outcome.get("blocker"),
            session=result.session or self.active_session,
        )
        coordinator = self.coordinator
        self.outcomes.append(record)
        self.events.append(("return", record.ticket, coordinator, result.path, record.status))
        self.settled_coordinators.add(coordinator)
        self.coordinator = None
        self.active_session = None

        if record.status == "delivered":
            self.cursor += 1
            if self.cursor == len(self.tickets):
                self.state = "complete"
                return self._terminal_report()
            self.state = "ready"
            return "advance"

        self.state = "stopped"
        return self._terminal_report()

    def steer(self, target: int | None, message: str) -> tuple[str, str] | None:
        if self.state != "dispatched" or target != self.coordinator:
            return None
        self.events.append(("steer", target))
        report = (
            f"{self.current_ticket} instruction forwarded (#{target}); "
            "root available; outcome pending."
        )
        return report, message

    def request_stop(self, target: int, request: InterruptRequest) -> str:
        if self.state != "dispatched" or target != self.coordinator:
            return self._fail("interrupt-mismatch", None)

        ticket = self.current_ticket
        coordinator = self.coordinator
        self.cancellation_intent = (ticket, coordinator)
        self.events.append(("interrupt-request", coordinator, "managed-lineage"))
        if request.coordinator != coordinator or not request.accepted:
            return self._begin_cleanup_failure(
                "interrupt-request", None, request.coordinator, request_cleanup=False
            )

        self.state = "cancelling"
        return (
            f"{ticket} cancellation requested (#{coordinator}); Mission stopped; "
            "confirmation pending; root available."
        )

    def _receive_cancellation_pong(self, result: CoordinatorReturn) -> str:
        ticket = self.current_ticket
        coordinator = self.coordinator
        matched = (
            coordinator is not None
            and self.cancellation_intent == (ticket, coordinator)
            and result.coordinator == coordinator
            and result.path == "pong"
            and result.outer_status == "interrupted"
            and not result.truncated
            and result.return_count == 1
        )
        if not matched:
            if coordinator is not None and result.coordinator != coordinator:
                return self._begin_cleanup_failure(
                    "interrupt-confirmation",
                    result.session,
                    result.coordinator,
                    request_cleanup=False,
                )
            return self._fail("interrupt-confirmation", result.session)

        record = OutcomeRecord(
            ticket=ticket,
            status="cancelled",
            session=result.session or self.active_session,
        )
        self.outcomes.append(record)
        self.events.append(
            ("interrupt-pong", ticket, coordinator, "managed-lineage-closed")
        )
        self.settled_coordinators.add(coordinator)
        self.coordinator = None
        self.active_session = None
        self.state = "stopped"
        return self._terminal_report()

    def _begin_cleanup_failure(
        self,
        reason: str,
        session: str | None,
        returned_coordinator: int,
        request_cleanup: bool = True,
    ) -> str:
        active = self.coordinator
        self.pending_failure = OutcomeRecord(
            ticket=self.current_ticket,
            status="failed",
            session=session or self.active_session,
            reason=reason,
        )
        self.events.append(
            ("failure-detected", self.current_ticket, active, returned_coordinator, reason)
        )
        action = "interrupt-cleanup" if request_cleanup else "await-terminal-cleanup"
        self.events.append((action, active, "managed-lineage"))
        self.state = "cleanup"
        return "cleanup-pending"

    def _receive_cleanup_pong(self, result: CoordinatorReturn) -> str:
        active = self.coordinator
        if (
            active is None
            or self.pending_failure is None
            or result.coordinator != active
            or result.path != "pong"
            or result.return_count != 1
        ):
            return self._fail("cleanup-confirmation", result.session)

        record = OutcomeRecord(
            ticket=self.pending_failure.ticket,
            status="failed",
            session=result.session or self.pending_failure.session,
            reason=self.pending_failure.reason,
        )
        self.outcomes.append(record)
        self.events.append(
            ("cleanup-pong", record.ticket, active, result.outer_status)
        )
        self.settled_coordinators.add(active)
        self.coordinator = None
        self.active_session = None
        self.pending_failure = None
        self.state = "stopped"
        return self._terminal_report()

    def _fail(
        self,
        reason: str,
        session: str | None,
        returned_coordinator: int | None = None,
    ) -> str:
        if self.cursor >= len(self.tickets):
            ticket = self.tickets[-1]
        else:
            ticket = self.current_ticket
        active = self.coordinator
        record = OutcomeRecord(
            ticket=ticket,
            status="failed",
            session=session or self.active_session,
            reason=reason,
        )
        self.outcomes.append(record)
        self.events.append(("failure", ticket, active, returned_coordinator, reason))
        if active is not None:
            self.settled_coordinators.add(active)
        self.coordinator = None
        self.active_session = None
        self.state = "stopped"
        return self._terminal_report()

    def _terminal_report(self, current_not_dispatched: bool = False) -> str:
        current = format_record(self.outcomes[-1])
        progress = f"{self.cursor}/{len(self.tickets)} delivered"
        if self.state == "complete":
            ending = "Mission complete"
        elif current_not_dispatched:
            undelivered = len(self.tickets) - self.cursor
            ending = (
                "Mission stopped; current not dispatched; "
                f"{undelivered} undelivered"
            )
        else:
            remaining = len(self.tickets) - self.cursor - 1
            ending = f"Mission stopped; {max(remaining, 0)} remaining"
        mode = (
            "root available"
            if self.mode == "interactive"
            else "print settled; no pong pending"
        )
        if self.mode == "print" and len(self.outcomes) > 1:
            current = " | ".join(format_record(item) for item in self.outcomes)
        return f"{current}; {progress}; {ending}; {mode}."


def format_record(record: OutcomeRecord) -> str:
    value = f"{record.ticket} {record.status}"
    if record.reason:
        value += f" ({record.reason})"
    for label, detail in (
        ("ref", record.ref),
        ("blocker", record.blocker),
        ("session", record.session),
    ):
        if detail:
            value += f"; {label} {detail}"
    return value


def check_input_scenarios() -> None:
    scenarios = [
        (["luizomf/omskills#38"], False, "authorization"),
        ([], True, "empty"),
        (["#38"], True, "identity-syntax"),
        (["luizomf/omskills#0"], True, "identity-syntax"),
        (["luizomf/om skills#38"], True, "identity-syntax"),
        (
            ["luizomf/omskills#38", "luizomf/omskills#38"],
            True,
            "duplicate",
        ),
        (
            ["luizomf/omskills#38", "luizomf/omskills#35"],
            True,
            "accepted",
        ),
    ]
    for tickets, authorized, expected in scenarios:
        assert validate_input(tickets, authorized) == expected

    supplied = ["Owner_Name/repo.name#9", "other/repo-2#10"]
    mission = Mission.accept(supplied, True, "interactive")
    supplied.reverse()
    assert mission.tickets == ("Owner_Name/repo.name#9", "other/repo-2#10")


def check_outcome_validation_scenarios() -> None:
    ticket = "luizomf/omskills#38"
    scenarios = [
        (f'{{"ticket":"{ticket}","status":"delivered","ref":"abc123"}}', "accepted"),
        (f'{{"ticket":"{ticket}","status":"blocked","blocker":"setup missing"}}', "accepted"),
        (f'{{"ticket":"{ticket}","status":"failed"}}', "accepted"),
        (f'{{"ticket":"{ticket}","status":"cancelled"}}', "accepted"),
        ("[]", "shape"),
        (f'{{"ticket":"{ticket}"}}', "shape"),
        (
            f'{{"ticket":"{ticket}","ticket":"{ticket}","status":"delivered"}}',
            "shape",
        ),
        (f'{{"ticket":"{ticket}","status":"done"}}', "status"),
        ('{"ticket":"luizomf/omskills#39","status":"delivered"}', "identity"),
        (f'{{"ticket":"{ticket}","status":"delivered","next":"#39"}}', "shape"),
        (f'prefix {{"ticket":"{ticket}","status":"delivered"}}', "syntax"),
        (
            f'{{"ticket":"{ticket}","status":"delivered"}}\nimplementation complete',
            "syntax",
        ),
    ]
    for message, expected in scenarios:
        result, _ = validate_outcome(message, ticket)
        assert result == expected, message


def check_terminal_and_cursor_scenarios() -> None:
    tickets = ["acme/repo#1", "acme/repo#2", "acme/repo#3"]
    stop_scenarios = [
        ("blocked", '"blocker":"dependency unresolved"'),
        ("failed", ""),
        ("cancelled", ""),
    ]
    for status, optional in stop_scenarios:
        mission = Mission.accept(tickets, True, "interactive")
        mission.start(11)
        assert mission.receive(
            CoordinatorReturn(11, "pong", '{"ticket":"acme/repo#1","status":"delivered"}')
        ) == "advance"
        mission.start(12)
        suffix = f",{optional}" if optional else ""
        report = mission.receive(
            CoordinatorReturn(
                12,
                "pong",
                f'{{"ticket":"acme/repo#2","status":"{status}"{suffix}}}',
                session="session-12",
            )
        )
        assert mission.cursor == 1
        assert [item.status for item in mission.outcomes] == ["delivered", status]
        assert mission.state == "stopped"
        assert "1/3 delivered" in report
        assert "Mission stopped; 1 remaining" in report
        assert "session session-12" in report

    complete = Mission.accept(tickets[:2], True, "interactive")
    complete.start(21)
    assert complete.receive(
        CoordinatorReturn(21, "pong", '{"ticket":"acme/repo#1","status":"delivered"}')
    ) == "advance"
    advance_report = complete.start(22)
    assert advance_report == (
        "acme/repo#1 delivered; 1/2 delivered; acme/repo#2 dispatched (#22); "
        "root available; outcome pending."
    )
    complete_report = complete.receive(
        CoordinatorReturn(
            22,
            "pong",
            '{"ticket":"acme/repo#2","status":"delivered","ref":"commit-2",'
            '"blocker":"informational"}',
            session="session-22",
        )
    )
    assert complete.cursor == 2
    assert complete.state == "complete"
    assert complete_report == (
        "acme/repo#2 delivered; ref commit-2; blocker informational; "
        "session session-22; 2/2 delivered; Mission complete; root available."
    )


def check_fail_closed_scenarios() -> None:
    ticket = "acme/repo#7"
    scenarios = [
        (CoordinatorReturn(31, "direct", f'{{"ticket":"{ticket}","status":"delivered"}}'), "wrong-path"),
        (CoordinatorReturn(31, "pong", None), "missing"),
        (CoordinatorReturn(31, "pong", f'{{"ticket":"{ticket}","status":"delivered"}}', truncated=True), "truncated"),
        (CoordinatorReturn(31, "pong", f'{{"ticket":"{ticket}","status":"delivered"}}', return_count=2), "duplicate-return"),
        (CoordinatorReturn(31, "pong", None, outer_status="failed"), "transport"),
        (CoordinatorReturn(31, "pong", f'{{"ticket":"{ticket}","status":"done"}}'), "outcome-status"),
        (CoordinatorReturn(31, "pong", '{"ticket":"acme/repo#8","status":"delivered"}'), "outcome-identity"),
        (CoordinatorReturn(31, "pong", "not JSON"), "outcome-syntax"),
        (CoordinatorReturn(31, "pong", f'{{"ticket":"{ticket}","status":"delivered"}}\nnarrative'), "outcome-syntax"),
    ]
    for result, reason in scenarios:
        mission = Mission.accept([ticket, "acme/repo#8"], True, "interactive")
        mission.start(31, "accepted-session")
        report = mission.receive(result)
        assert mission.state == "stopped"
        assert mission.cursor == 0
        assert mission.outcomes[-1].status == "failed"
        assert mission.outcomes[-1].reason == reason
        assert "Mission complete" not in report
        assert "Mission stopped; 1 remaining" in report

    mismatched = Mission.accept([ticket, "acme/repo#8"], True, "interactive")
    mismatched.start(31, "active-session")
    assert mismatched.receive(
        CoordinatorReturn(
            99,
            "pong",
            f'{{"ticket":"{ticket}","status":"delivered"}}',
        )
    ) == "cleanup-pending"
    assert mismatched.state == "cleanup"
    assert mismatched.coordinator == 31
    assert mismatched.outcomes == []
    assert mismatched.events[-1] == (
        "interrupt-cleanup",
        31,
        "managed-lineage",
    )
    report = mismatched.receive(
        CoordinatorReturn(
            31,
            "pong",
            None,
            outer_status="interrupted",
            session="active-session",
        )
    )
    assert mismatched.state == "stopped"
    assert mismatched.outcomes[-1].reason == "mismatched-return"
    assert "session active-session" in report

    duplicate = Mission.accept([ticket, "acme/repo#8"], True, "interactive")
    duplicate.start(40)
    assert duplicate.receive(
        CoordinatorReturn(40, "pong", f'{{"ticket":"{ticket}","status":"delivered"}}')
    ) == "advance"
    duplicate.start(41, "session-41")
    assert duplicate.receive(
        CoordinatorReturn(40, "pong", f'{{"ticket":"{ticket}","status":"delivered"}}')
    ) == "cleanup-pending"
    report = duplicate.receive(
        CoordinatorReturn(
            41,
            "pong",
            None,
            outer_status="interrupted",
            session="session-41",
        )
    )
    assert duplicate.outcomes[-1].reason == "duplicate-return"
    assert duplicate.cursor == 1
    assert "1/2 delivered" in report


def check_steering_and_cancellation_scenarios() -> None:
    ticket = "acme/repo#9"
    mission = Mission.accept([ticket, "acme/repo#10"], True, "interactive")
    mission.start(51, "native-session-51")
    unrelated_state = (mission.cursor, mission.state, tuple(mission.events))
    assert mission.steer(None, "What is the weather?") is None
    assert mission.steer(99, "Change the implementation") is None
    assert (mission.cursor, mission.state, tuple(mission.events)) == unrelated_state

    instruction = "Preserve API v1 exactly; do not rename it."
    steering = mission.steer(51, instruction)
    assert steering == (
        f"{ticket} instruction forwarded (#51); root available; outcome pending.",
        instruction,
    )
    assert mission.events[-1] == ("steer", 51)
    assert instruction not in repr(mission.__dict__)

    cancellation_scenarios = [("writer", mission, 51), ("reviewer", None, 52)]
    for nested_role, current, coordinator in cancellation_scenarios:
        if current is None:
            current = Mission.accept([ticket, "acme/repo#10"], True, "interactive")
            current.start(coordinator, f"native-session-{coordinator}")
        nested_work = {coordinator: [nested_role]}
        pending = current.request_stop(
            coordinator,
            InterruptRequest(coordinator=coordinator),
        )

        assert current.cancellation_intent == (ticket, coordinator)
        assert current.state == "cancelling"
        assert current.outcomes == []
        assert current.events[-1] == (
            "interrupt-request",
            coordinator,
            "managed-lineage",
        )
        assert nested_work[coordinator] == [nested_role]
        assert "confirmation pending" in pending
        assert not any(event[0] == "interrupt-descendant" for event in current.events)

        # The harness emits the pong only after coordinator/descendant process closure.
        nested_work[coordinator].clear()
        cancelled = current.receive(
            CoordinatorReturn(
                coordinator,
                "pong",
                None,
                outer_status="interrupted",
                session=f"native-session-{coordinator}",
            )
        )
        assert nested_work[coordinator] == []
        assert current.events[-1] == (
            "interrupt-pong",
            ticket,
            coordinator,
            "managed-lineage-closed",
        )
        assert current.outcomes[-1] == OutcomeRecord(
            ticket=ticket,
            status="cancelled",
            session=f"native-session-{coordinator}",
        )
        assert f"session native-session-{coordinator}" in cancelled
        assert "0/2 delivered" in cancelled
        assert "Mission stopped; 1 remaining" in cancelled

    wrong_confirmation = Mission.accept([ticket], True, "interactive")
    wrong_confirmation.start(61, "session-61")
    wrong_confirmation.request_stop(61, InterruptRequest(61))
    report = wrong_confirmation.receive(
        CoordinatorReturn(61, "pong", None, outer_status="failed", session="session-61")
    )
    assert wrong_confirmation.outcomes[-1].status == "failed"
    assert wrong_confirmation.outcomes[-1].reason == "interrupt-confirmation"
    assert "Mission complete" not in report

    mismatched_confirmation = Mission.accept([ticket], True, "interactive")
    mismatched_confirmation.start(62, "session-62")
    mismatched_confirmation.request_stop(62, InterruptRequest(62))
    assert mismatched_confirmation.receive(
        CoordinatorReturn(99, "pong", None, outer_status="interrupted")
    ) == "cleanup-pending"
    report = mismatched_confirmation.receive(
        CoordinatorReturn(
            62,
            "pong",
            None,
            outer_status="interrupted",
            session="session-62",
        )
    )
    assert mismatched_confirmation.outcomes[-1].status == "failed"
    assert mismatched_confirmation.outcomes[-1].reason == "interrupt-confirmation"
    assert "Mission complete" not in report

    rejected_request = Mission.accept([ticket], True, "interactive")
    rejected_request.start(63, "session-63")
    assert rejected_request.request_stop(
        63,
        InterruptRequest(63, accepted=False),
    ) == "cleanup-pending"
    report = rejected_request.receive(
        CoordinatorReturn(
            63,
            "pong",
            f'{{"ticket":"{ticket}","status":"delivered"}}',
            session="session-63",
        )
    )
    assert rejected_request.outcomes[-1].status == "failed"
    assert rejected_request.outcomes[-1].reason == "interrupt-request"
    assert "Mission complete" not in report

    unsolicited = Mission.accept([ticket], True, "interactive")
    unsolicited.start(70)
    report = unsolicited.receive(
        CoordinatorReturn(70, "pong", None, outer_status="interrupted", session="session-70")
    )
    assert unsolicited.outcomes[-1].reason == "transport"
    assert "failed" in report


def check_start_rejection_scenarios() -> None:
    tickets = ["acme/repo#1", "acme/repo#2"]

    first = Mission.accept(tickets, True, "interactive")
    report = first.reject_start("capacity")
    assert first.cursor == 0
    assert first.state == "stopped"
    assert first.events == [("start-rejected", tickets[0], "dispatch-capacity")]
    assert "current not dispatched; 2 undelivered" in report
    assert "root available" in report

    later = Mission.accept(tickets, True, "interactive")
    later.start(75)
    assert later.receive(
        CoordinatorReturn(
            75,
            "pong",
            '{"ticket":"acme/repo#1","status":"delivered"}',
        )
    ) == "advance"
    report = later.reject_start("preflight")
    assert later.cursor == 1
    assert [item.status for item in later.outcomes] == ["delivered", "failed"]
    assert "1/2 delivered" in report
    assert "current not dispatched; 1 undelivered" in report

    printed = Mission.accept(tickets, True, "print")
    printed.start(76)
    assert printed.receive(
        CoordinatorReturn(
            76,
            "direct",
            '{"ticket":"acme/repo#1","status":"delivered"}',
        )
    ) == "advance"
    report = printed.reject_start("transport", "session-rejected")
    assert "acme/repo#1 delivered | acme/repo#2 failed (dispatch-transport)" in report
    assert "session session-rejected" in report
    assert "current not dispatched; 1 undelivered" in report
    assert "print settled; no pong pending" in report


def check_mode_progression_scenarios() -> None:
    tickets = ["acme/repo#1", "acme/repo#2", "acme/repo#3"]
    interactive = Mission.accept(tickets[:2], True, "interactive")
    interactive.start(81)
    assert interactive.receive(
        CoordinatorReturn(81, "pong", '{"ticket":"acme/repo#1","status":"delivered"}')
    ) == "advance"
    interactive.start(82)
    assert [event[0] for event in interactive.events] == ["start", "return", "start"]
    assert all(event[0] not in {"poll", "sleep", "list"} for event in interactive.events)
    assert interactive.max_active == 1
    try:
        interactive.start(83)
    except RuntimeError as error:
        assert "already active" in str(error)
    else:
        raise AssertionError("parallel coordinator start was accepted")

    direct_results = [
        CoordinatorReturn(
            coordinator=coordinator,
            path="direct",
            message=f'{{"ticket":"{ticket}","status":"delivered"}}',
            session=f"session-{coordinator}",
        )
        for coordinator, ticket in zip((91, 92, 93), tickets, strict=True)
    ]
    printed = Mission.accept(tickets, True, "print")
    report = ""
    for index, result in enumerate(direct_results):
        assert printed.start(result.coordinator) is None
        report = printed.receive(result)
        if index < len(direct_results) - 1:
            assert report == "advance"
    assert printed.state == "complete"
    assert printed.cursor == len(tickets)
    assert [event[3] for event in printed.events if event[0] == "start"] == [
        "direct",
        "direct",
        "direct",
    ]
    assert printed.max_active == 1
    assert "Mission complete" in report
    assert "print settled; no pong pending" in report
    assert all(f"session-{coordinator}" in report for coordinator in (91, 92, 93))


def check_reference_scenarios() -> None:
    check_input_scenarios()
    check_outcome_validation_scenarios()
    check_terminal_and_cursor_scenarios()
    check_fail_closed_scenarios()
    check_steering_and_cancellation_scenarios()
    check_start_rejection_scenarios()
    check_mode_progression_scenarios()


def main() -> None:
    skill = SKILL_PATH.read_text()
    frontmatter = re.match(r"\A---\n(.*?)\n---", skill, re.DOTALL)
    assert frontmatter, "dispatch-tickets frontmatter is missing"
    require(
        frontmatter.group(1),
        "name: dispatch-tickets",
        "description: Dispatch ",
        "disable-model-invocation: true",
    )

    manifests = [
        json.loads((ROOT / ".codex-plugin/plugin.json").read_text()),
        json.loads((ROOT / ".claude-plugin/plugin.json").read_text()),
    ]
    assert manifests[0] == manifests[1], "plugin manifests are not mirrored"
    assert manifests[0]["skills"].count(MANIFEST_ENTRY) == 1

    require(
        (ROOT / "README.md").read_text(),
        "(./skills/engineering/dispatch-tickets/SKILL.md)",
        "fixed ordered list",
    )
    require(
        (ROOT / "skills/engineering/README.md").read_text(),
        "(./dispatch-tickets/SKILL.md)",
        "fixed ordered list",
    )
    require(
        (ROOT / "scripts/check-catalog.py").read_text(),
        '"dispatch-tickets"',
    )

    prompt_match = re.search(
        r"Use this exact coordinator prompt, replacing both placeholders without adding text:\n\n"
        r"```text\n(.*?)\n```",
        skill,
        re.DOTALL,
    )
    assert prompt_match, "exact coordinator prompt is not extractable"
    prompt = prompt_match.group(1)
    assert prompt == EXPECTED_PROMPT, "coordinator prompt widened or changed"
    for forbidden in ("next", "writer", "reviewer", "diff", "tests", "acceptance criteria"):
        assert forbidden not in prompt.lower(), f"coordinator prompt contains work detail: {forbidden}"

    require(
        skill,
        "use the skill loader to read and follow the installed `caveman` skill",
        "That composition read is the root's sole file read",
        "non-empty ordered list",
        "unique",
        "freeze",
        "`<owner>/<repository>#<positive-integer>`",
        "only ASCII letters, digits, `.`, `_`, or `-`",
        "explicitly states Mission authorization",
        "performs no tracker, repository, or remote discovery",
        "cursor",
        "one fresh coordinator at a time",
        "`PI_PROVIDER`, `PI_MODEL`, and `PI_REASONING_LEVEL`",
        "retain none of their values in dispatcher state",
        "`subagent_start`",
        '`delivery: "async"`',
        '`delivery: "direct"`',
        "`maxDepth: 3`",
        "`maxChildren: 1`",
        "Omit `tools`",
        "without waiting, sleeping, polling",
        "new turn",
        "one finite invocation",
        "one top-level JSON object",
        "duplicate JSON keys",
        "byte-for-byte",
        "duplicate return",
        "truncated",
        "wrong return path",
        "Do not adjudicate implementation semantics",
        "`subagent_steer`",
        "literally",
        "Do not retain",
        "cancellation intent",
        "`subagent_interrupt`",
        "only enters `cancelling`",
        "one later pong",
        "managed descendants have closed",
        "recursive descendant cleanup is harness-owned",
        "native child session reference",
        "matching mechanical caller interruption",
        "current not dispatched",
        "Mission complete",
        "No child receives or returns `next`",
        "no retry, skip, heartbeat",
        "no persistent workflow state",
        "no wormhole or tmux dependency",
        "no Queue/TTS side effect",
        "publishing, tagging, or release",
    )

    staged_fragments = {
        ROOT / "CONTEXT.md": (
            "accepted sequence extension later adds",
            "active one-Ticket **Ticket dispatcher**",
        ),
        ROOT / "skills/productivity/writing-great-skills/SKILL.md": (
            "Ordered sequences remain outside the active dispatcher",
        ),
        ROOT / "skills/engineering/to-tickets/SKILL.md": (
            "Ordered-sequence dispatch remains unavailable",
        ),
        ROOT / "skills/engineering/triage/SKILL.md": (
            "Ordered-sequence dispatch remains unavailable",
        ),
    }
    for path, fragments in staged_fragments.items():
        text = path.read_text()
        for fragment in fragments:
            assert fragment not in text, f"staged routing remains in {path}: {fragment}"

    routed_sources = {
        ROOT / "CONTEXT.md": "already-resolved ordered list",
        ROOT / "skills/productivity/writing-great-skills/SKILL.md": (
            "already-resolved ordered list"
        ),
        ROOT / "skills/productivity/write-a-skill/SKILL.md": (
            "already-resolved ordered list"
        ),
        ROOT / "skills/engineering/triage/SKILL.md": "already-resolved ordered list",
        ROOT / "skills/engineering/to-tickets/SKILL.md": (
            "already-resolved ordered list"
        ),
    }
    for path, fragment in routed_sources.items():
        require(path.read_text(), fragment)

    check_reference_scenarios()
    print("dispatch-tickets contract and state-machine scenarios ok")


if __name__ == "__main__":
    main()
