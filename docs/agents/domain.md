# Domain docs

This is a single-context repository.

Before changing skill behavior or workflow vocabulary, read:

- root `CONTEXT.md` for canonical terms and relationships; and
- applicable records under root `docs/adr/` for durable decisions.

No `CONTEXT-MAP.md` is configured, so there are no context-scoped glossary or ADR roots. Do not infer additional roots from `src/*`, `packages/*`, or another workspace layout.

Use glossary terms in skill descriptions, issue titles, tests, and documentation. If a proposed change conflicts with an ADR, surface the conflict explicitly instead of silently overriding it. Missing domain or ADR files are created lazily by `grill-with-docs` when qualifying terms or decisions are resolved.
