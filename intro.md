# API Fundamentals — Reference, Tests & Configs

This repository collects an actionable companion for a short course on **API fundamentals**:
- a concise introduction to core API concepts and best practices;
- practical, ready-to-run **test cases** (YAML) for functional, security, and fuzz testing;
- sample **payloads** and **server/client configs** you can drop into CI, Postman, or fuzzing tools.

Purpose
-------
This docset is intended to:
1. Help engineers understand core API design principles (HTTP methods, status codes, idempotency, DTO vs entity, versioning).
2. Provide reproducible test cases (expected status and headers included) for QA, security, and automated CI scanning.
3. Offer hardened configuration examples for deployment (TLS, CORS, rate-limiting) and example OpenAPI fragments for contract-driven development.

How to use
----------
- `tests.yaml` — load into your test harness (e.g., custom runner, Postman, Newman, or a fuzzer adapter) or convert into unit tests.
- `payloads.yaml` — example request bodies and boundary inputs used by test cases.
- `configs.yaml` — reference server and gateway snippets to enforce security, rate limits, and content negotiation.

Conventions
-----------
- Each test entry includes: `id`, `description`, `method`, `path`, `headers`, `body-ref` (from payloads.yaml), `expected_status`, `expected_headers`, and `notes`.
- Tests aim to be deterministic where possible (i.e., use fixed inputs) and also include negative/fuzz tests to expose parsing and validation errors.
- Sensitive values and secrets are represented as environment variables (e.g., `JWT_SECRET`, `DB_CONN`).

License & Attribution
---------------------
MIT — use freely. If you modify and publish, please attribute the original author.
