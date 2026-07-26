---
name: model-routing
description: Select models and reasoning effort for direction-setting, coordination, implementation, review, audit, and mechanical delegated work. Use when selecting a model or reasoning effort for an active session or delegated agent.
---

# Model Routing

Route work by consequence, then use the matching model from the current vendor. This file is the single source of truth for role-to-model selection.

## Routes

| Route | Use for | Anthropic | OpenAI | Google | Effort |
| --- | --- | --- | --- | --- | --- |
| **Direction setter** | Grilling, wayfinding, specs, ticket creation, and other outputs that govern downstream agents | `claude-opus-5` | `gpt-5.6-sol` | `gemini-3.1-pro-preview` | `high` |
| **Coordinator** | Selecting and adjudicating prepared work, correcting candidates, and integrating results | `claude-sonnet-5` | `gpt-5.6-terra` | `gemini-3.6-flash` | `high` |
| **Writer** | Implementing a prepared issue and running its verification | `claude-sonnet-5` | `gpt-5.6-terra` | `gemini-3.6-flash` | `medium` |
| **Reviewer** | Independently checking implementation against governing sources and risks | `claude-opus-5` | `gpt-5.6-sol` | `gemini-3.1-pro-preview` | `high` |
| **Audit reviewer** | Comparing reconstructed intent with authoritative intent | `claude-sonnet-5` | `gpt-5.6-terra` | `gemini-3.6-flash` | `high` |
| **Utility** | Mechanical reading, extraction, classification, transformation, and focused summaries | `claude-haiku-4-5` | `gpt-5.6-luna` | `gemini-3.1-flash-lite` | `low` |

A prompt-audit interpreter is the exception: use the exact model and effort intended for the audited executor.

## Selection Rules

1. An explicit user model or effort choice wins.
2. Stay within the current vendor unless the user requests another vendor.
3. For a delegated agent, pass the selected model and effort explicitly instead of inheriting the parent defaults.
4. For work spanning routes, use the route governing its highest-consequence output. Ordinary implementation remains **Writer** even when it requires local planning.
5. If the exact model is unavailable, use the closest available model in the same vendor and capability tier, and report the substitution.
6. If the harness cannot select the active model, continue with the active model; do not interrupt the work solely to enforce this policy.
7. Use only `low`, `medium`, and `high`. Increase effort only when the route or concrete task complexity requires it.

## Example

For prepared OpenAI work:

```text
coordinator  -> gpt-5.6-terra, high
writer       -> gpt-5.6-terra, medium
reviewer     -> gpt-5.6-sol, high
file summary -> gpt-5.6-luna, low
```
