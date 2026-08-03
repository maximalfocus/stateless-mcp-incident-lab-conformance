# Problem

Define the complete, implementation-independent behavioral contract for Stateless MCP Incident Lab before either TypeScript realization exists. The suite must faithfully encode selected MCP 2026-07-28 wire behavior, explicit incident state, MRTR, streaming, cache, CLI, security, observability, architecture, infrastructure, CI, and four-way raw/SDK interoperability.

## Source of truth

1. `../stateless-mcp-incident-lab-prd/PRD.md` and active `PLAN-001-stateless-core.md` at `91cd6b984a27c29cca8e8505a7ec1f088251650f`.
2. Captured MCP `2026-07-28` specification and authoritative `schema.ts` under the PRD repo's `sources/`; schema wins over captured prose on type shape.
3. Accepted ADRs and boundary YAML in `../stateless-mcp-incident-lab-architecture/` at `182e756eb4bdbb6c27fd66d185aff90466c28697`.

## Scope

All 19 PLAN-001 categories and their 197 individually identified tests: protocol, versioning, transport, discovery, primitives, incidents, MRTR, streaming, cache, CLI, interoperability, properties, security, observability, performance, architecture, infrastructure, CI/CD, and dependencies. Both raw and SDK providers consume the same language-neutral contract.

## Non-goals

Implementation code; graphical frontend; authentication/OAuth/identity; legacy MCP sessions; extensions excluded by PLAN-001; real remediation or permanent deployment. This review may correct the conformance suite and its own validation/docs, but must not weaken PRD behavior or edit sibling source-of-truth repos silently.

## Acceptance criteria

1. Exactly 197 unique `test.json` leaves exist across exactly 19 planned categories and are bijectively listed in `coverage-tracking.md`. `WORKITEMS.md` assigns each golden exactly once to every applicable owning lane (`raw`, `sdk`, `integration`, `infrastructure`, or `cicd`), never shares a completion status across repositories, and keeps every WI to 2–5 tests with unique ordered IDs and backward-only dependencies.
2. Every test is replayable at its declared public boundary from committed, self-contained input/request/seed fixtures. No expected result depends on hidden generator state or a runner-hardcoded scenario oracle.
3. Expected files pin complete machine-checkable observable shapes or a closed, documented executable assertion DSL. Prose-only “contract satisfied” assertions, generic pseudo-RPCs, and assertions an implementation can satisfy without exercising the named behavior are forbidden.
4. Selected MCP wire shapes, validation precedence, HTTP status/header/body behavior, JSON-RPC IDs/errors, capabilities, pagination, caching, progress/cancellation, and MRTR retry semantics faithfully match the PRD and captured normative schema.
5. Incident fixtures discriminate every allowed transition, terminal failure, unknown/expired handle, decline/cancel path, and conditional at-most-once effect without relying on process/session affinity.
6. Security contracts exercise Origin/header/body/schema/deadline/state-tamper/redaction/simulated-only boundaries and never introduce real infrastructure effects or bearer leakage.
7. Raw↔SDK four-way interoperability and replica independence are expressed without provider-specific logic except explicitly allowed metadata normalization; family integration work depends on completion of both independent implementation lanes.
8. `architecture/dependencies/` and `architecture/boundaries/` are non-vacuous, cite Accepted ADRs, and byte-faithfully mirror parseable upstream YAML semantics for both implementations.
9. `convention-reference.json`, `suite-invariants.json`, all expected shapes, placeholders, IDs, null/absent rules, error envelopes, and auth absence are cross-file consistent.
10. Properties have complete executable definitions and decisive examples; performance/infra/CI policy assertions are mechanism-neutral where the PRD permits alternatives and document any necessary runner correlation obligation.
11. Ambiguities add no invented domain/protocol structure, preserve the PRD decision boundaries, and identify every affected spec ID individually.
12. Validation fails closed on malformed JSON, missing files/fields, duplicate IDs, coverage/WORKITEM lane drift, wrong-lane or duplicate assignment, unknown/forward WI dependencies, unknown assertions, empty architecture globs, leaked wrapper tags, stale ADR citations, and prohibited golden auto-update behavior.

## Verification

```bash
python3 scripts/validate-suite.py
node ~/personal/cdd-skills/tools/golden-lint.ts conformance
python3 ../stateless-mcp-incident-lab-prd/scripts/verify-prd.py
python3 -m unittest discover -s scripts -p 'test_*.py'
git diff --check
```

The reviewer also parses both sibling `rules/*.yaml` using Ruby's standard YAML loader (PyYAML is not installed), compares their deny/boundary tuples to ARCH-001–006, and independently re-derives high-risk MCP schema/error fixtures from the captured source rather than trusting this suite's own descriptions.

## Residuals

Executable provider runs and mutation scores are evidenced and gated in the owning raw and SDK implementation repositories; both currently replay this suite's 159-contract implementation lane. This conformance review still judges the complete 197-contract language-neutral suite and does not treat provider green as evidence that a golden is faithful, replayable, or discriminating.
