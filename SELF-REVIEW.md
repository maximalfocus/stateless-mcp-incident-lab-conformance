# Author self-review

Completed for the executable-golden evolution at PRD commit `91cd6b984a27c29cca8e8505a7ec1f088251650f`.

- [x] **8a — Cross-file consistency.** All 197 `expected.json` files were parsed and audited for JSON-RPC envelopes, IDs, result metadata, placeholders, null use, collection order, cache fields, and HTTP header shape. Errors use one JSON-RPC 2.0 envelope; transport-level 403/405 bodies and notification bodies are `null` by contract.
- [x] **8b — Structural validation and lint.** `python3 scripts/validate-suite.py conformance` passes 197 tests, 19 categories, and 197 unique IDs. `deno run --allow-read ~/personal/cdd-skills/tools/golden-lint.ts conformance` reports 0 errors and 0 warnings.
- [x] **8c — Seed/request/expected coherence.** Requests no longer contain runner-only `params.scenario`. Incident/remediation handles used by HTTP and MRTR fixtures exist in each test's seed; unknown and expired handles are explicitly negative fixtures. All HTTP tests use public MCP methods or health endpoints.
- [x] **8d — Placeholder realism.** Only placeholders declared by `suite-invariants.json` are accepted. Generated IDs and timestamps appear only for server-created values; replica IDs use `{{ANY_STRING}}`; no ellipsis or undeclared placeholder remains.
- [x] **8e — BDD alignment.** Every `description_bdd.then` was checked against its exact output. Composite client scenarios expose all requests and observations rather than hiding behavior behind prose.
- [x] **8f — Source verification.** Protocol shapes were checked against captured `sources/spec-2026-07-28/schema.ts`; MRTR uses `inputRequests` keyed to `elicitation/create`, retries use sibling `inputResponses`/`requestState`, and header encoding uses the normative `=?base64?...?=` sentinel.
- [x] **8g — Negative coverage.** Exact malformed-input, unsupported-version/capability, header mismatch, cursor, unknown handle/resource/prompt, MRTR tamper/expiry/reuse, body limit, deadline, origin, schema bound, cache-disabled, and feature-unsupported observations are present.

## Multi-implementation handoff evolution

- [x] `WORKITEMS.md` has independent raw, SDK, integration, infrastructure, and CI/CD status lanes.
- [x] Each WI contains 2–5 tests; IDs are globally unique and sequential; every dependency resolves backward.
- [x] Raw and SDK lanes independently cover their applicable contracts without mixing provider-only architecture or health tests.
- [x] Integration, infrastructure, and CI/CD goldens are assigned only to their owning family lane.
- [x] The validator rejects missing/extra lane assignments and unknown/forward dependencies; both failure modes have mutation tests.

## Mechanical evidence

- `python3 scripts/validate-suite.py conformance`
- `python3 -m unittest scripts/test_validate_suite.py`
- `deno run --allow-read ~/personal/cdd-skills/tools/golden-lint.ts conformance`
- `python3 ../stateless-mcp-incident-lab-prd/scripts/verify-prd.py`
- architecture sibling: `python3 scripts/verify-architecture.py` plus its 18-case mutation script in an isolated PyYAML environment

## Degraded peer-review hardening

The 2026-08-02 Codex-host fallback found and corrected a shared-object generation defect that had put `2025-11-25` body metadata into 79 otherwise-current requests, plus missing seed references, non-discriminating CLI/interoperability/security/cache cases, and open-ended operation/policy dispatch. The suite now ships closed `operation-registry.json` and `policy-registry.json` contracts with mutation-tested validator enforcement, including header/body mirror checks and policy execution receipts.

The same-vendor fallback gate is sufficient to proceed in degraded mode, but cross-vendor sign-off remains owed because the Claude CLI was not authenticated.
