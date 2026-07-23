---
name: teach
description: Teach the user a new skill or concept, within this workspace.
argument-hint: "What would you like to learn about?"
---

Treat teaching as stateful work that may continue across multiple sessions.

## Teaching Workspace

Use the current directory as the teaching workspace and store learning state in these locations:

- `MISSION.md`: the user's reason for learning and the observable outcomes they seek. Base every lesson choice on it. Follow [MISSION-FORMAT.md](./MISSION-FORMAT.md).
- `reference/*.html`: printable lookup material extracted from lessons, including cheat sheets, algorithms, syntax, poses, and glossaries.
- `RESOURCES.md`: sources for knowledge and communities for practice. Follow [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md).
- `learning-records/*.md`: demonstrated learning, stated prior knowledge, corrected misconceptions, and mission changes used to select later lessons. Name files `0001-<dash-case-name>.md` and increment the highest existing number. Follow [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
- `lessons/*.html`: self-contained lessons. Follow [Lessons](#lessons).
- `assets/*`: reusable lesson components. Follow [Assets](#assets).
- `NOTES.md`: teaching preferences and temporary working notes.

## Teaching Model

Use all three sources of learning:

- **Knowledge** from cited primary or high-trust sources;
- **Skills** practiced in interactive lessons based on that knowledge;
- **Wisdom** tested with practitioners or learner communities.

Before writing a lesson, verify that `RESOURCES.md` contains a source supporting its factual content. If it does not, find and record one before drafting. Do not present parametric recall as a source.

Allocate lesson content according to the target: explanatory targets may emphasize knowledge acquisition; physical or procedural targets may emphasize guided practice.

### Fluency and Storage Strength

Distinguish immediate retrieval (**fluency strength**) from retention after a delay (**storage strength**). Select one or more of these methods when they support the lesson target:

- retrieval from memory rather than recognition alone;
- spaced reuse of prior material in later lessons;
- interleaving of related tasks during skills practice only.

Do not treat correct performance immediately after explanation as evidence of storage strength.

## Lessons

For each lesson, create one self-contained HTML file under `lessons/`. Use `0001-<dash-case-name>.html`, incrementing the highest existing lesson number.

A completed lesson should:

- target one observable ability or artifact that advances `MISSION.md`;
- contain one target and one practice cycle that can be completed in one focused sitting;
- require no unstated prerequisite knowledge;
- introduce no unrelated objective;
- teach only the knowledge required for the target ability;
- include user practice and a feedback loop;
- cite the factual claims it uses;
- recommend the primary source that most directly supports the lesson's factual content, preferring the source owner or official specification;
- link related existing lessons and reference documents using HTML anchors, including every artifact it cites or requires;
- remind the user that they can ask the agent follow-up questions.

The lesson should use a Tufte-style presentation. After writing the lesson, open it with an available CLI opener when that action is supported in the environment.

## Assets

Before authoring a lesson, inspect `assets/` and reuse each component that already provides behavior or styling required by the lesson. Components include stylesheets, quiz widgets, simulators, and diagram helpers.

If code or styling would be used by a second lesson, place it in `assets/` and link it rather than duplicating it inline. Create a shared stylesheet before creating the first lesson, and link every lesson to it.

## Mission

Before creating a lesson, interview the user about why they want to learn the topic when `MISSION.md` is absent, empty, or does not state both a concrete real-world goal and observable success criteria.

When the user proposes a mission change or learning evidence indicates that the mission may have changed:

1. State the proposed change.
2. Obtain the user's confirmation.
3. Update `MISSION.md`.
4. Add a learning record that captures the change.

Do not change the mission before confirmation.

## Zone of Proximal Development

If the user specifies the exact lesson target, use it when it advances the mission and fits the user's zone of proximal development.

Otherwise:

1. Read the active learning records.
2. Select the most mission-relevant target that fits the user's zone of proximal development.

## Knowledge and Skills

Lesson knowledge should come from sources recorded in `RESOURCES.md`. Cite each factual claim or contiguous group of claims with a link to the supporting external source.

Present required knowledge before asking the user to practice it. During knowledge acquisition, add no task difficulty beyond what is required to understand that knowledge; reserve retrieval difficulty and interleaving for skills practice. Exclude detail not required for the practice target or move it to a reference document.

Skills should be taught through interactive forms such as:

- quizzes or in-browser tasks;
- guided real-world procedures, such as a sequence of yoga poses.

Every practice activity should provide feedback in the next interaction after the user's response or action when the medium permits it. Prefer automatic feedback when correctness can be evaluated deterministically.

For multiple-choice quizzes, use the same word count for every answer. Also use the same character count when semantically equivalent wording can equalize the count without adding non-semantic tokens. Use identical formatting for all answers.

## Acquiring Wisdom

Treat a question as requiring wisdom when its answer depends on situational judgment or practitioner experience that published sources cannot verify. Provide the source-supported portion of the answer, then direct the user to a high-reputation online or offline community where they can test it in practice, unless `NOTES.md` records that the user declined community participation. Include paid classes only when the user's budget permits. If the user declines community participation, record that preference in `NOTES.md` and stop recommending communities.

## Reference Documents

While creating a lesson, you should create or update a file under `reference/` when the lesson contains material for independent lookup, including:

- programming syntax or code snippets;
- process algorithms or flowcharts;
- yoga poses or sequences;
- exercise or fitness routines;
- domain terminology.

The reference document should retain only the material needed for independent lookup. When a glossary exists, every later lesson should use its defined term for each concept.

## `NOTES.md`

Record teaching preferences and working constraints in `NOTES.md` when the user states them. Before designing a lesson, read each entry that affects its target, format, pacing, or exercises.
