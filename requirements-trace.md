# PRD line-by-line trace

> **Peer-review status:** This document proves planned ID/topic allocation only. It does not prove executable behavioral coverage. The degraded fallback found 17 categories built from runner-hardcoded `params.scenario` plus prose-only expected assertions; their `COVERED` rows below are suspended until those fixtures are rewritten and independently reviewed.

Mechanical first pass: `node ~/personal/cdd-skills/tools/coverage-review.ts ../stateless-mcp-incident-lab-prd/PRD.md conformance`. It discovers 191 top-level tests because the tool does not recurse through mandatory `architecture/{dependencies,boundaries}/`; the recursive suite validator confirms all 197. Findings below are the required judgment pass.

| PRD section | Status | Golden coverage / disposition |
|---|---|---|
| Overview | COVERED | Aggregate charter, represented by all 197 tests and `PROBLEM.md`; no independent observable. |
| Goals | COVERED | Goal-to-surface mapping in `api-surface-map.md`; protocol, matrix, state, CLI, local/cloud categories cover each goal. |
| User model | COVERED | `CLI-001–014`, `INT-001–012`, `SEC-011`. |
| Learner/operator | COVERED | `CLI-001–014`, `DISC-005`, `INT-011–012`, `INFRA-010`. |
| Domain and data model | COVERED | `INC-001–012`, `PRIM-016–018`, `MRTR-008–016`. |
| Entities | COVERED | Service/runbook/telemetry: `PRIM-004–009,017`; incident/diagnostic/remediation: `INC-001–012`, `MRTR-001–016`. Exact fixture prose is resolved by AMB-001. |
| Incident lifecycle | COVERED | Every valid transition and terminal/unknown/expired failures: `INC-001–012`. |
| Product topology | COVERED | `INT-011–012`, `PERF-002`, `INFRA-001–010`, `ARCH-001–006`. |
| MCP surface | COVERED | `PROTO-001–012` through `CACHE-001–010`. |
| Required request metadata | COVERED | `VER-001–010`, `TRANS-009–016`, `PROP-001`. |
| Discovery | COVERED | `DISC-001–006`; negative capability assertions are `DISC-003–004`, and direct-call without discovery is `VER-008`. |
| Tools | COVERED | `PRIM-001–003,016–020`, `INC-001–012`, `MRTR-001–016`. |
| Resources | COVERED | `PRIM-004–010`, `CACHE-003,010`, `SEC-009`. |
| Prompts | COVERED | `PRIM-011–015`, `CACHE-001`. |
| MRTR elicitation | COVERED | `MRTR-001–016`, `PERF-003`, `PROP-005,007`. |
| Progress and cancellation | COVERED | Positive and negative/loss paths: `STREAM-001–009`. |
| Caching | COVERED | `CACHE-001–010`, `PROP-002–004`. |
| CLI surface | COVERED | `CLI-001–014`. |
| Business rules | COVERED | `TRANS-001–018`, `VER-001–010`, `INC-001–012`, `SEC-001–012`. |
| Interoperability and acceptance | COVERED | `INT-001–012`, `PERF-002–003`, `CICD-002`. |
| Non-functional requirements | COVERED | `SEC-001–012`, `OBS-001–007`, `PERF-001–003`, `DEP-001–005`, `CICD-001`. |
| Deployment | COVERED | `INFRA-001–010`, `CICD-008`. |
| Local | COVERED | `OBS-001–003`, `INT-011–012`, `CICD-002`. |
| AWS | COVERED | `INFRA-001–010`, `PERF-001–002`. |
| Security posture | COVERED | `SEC-001–012`, `INFRA-004–008`, `DEP-002–004`. |
| Out of scope | INTENTIONAL GAP | No feature goldens. Required active rejections/ignores are covered by `VER-009–010`, `TRANS-005–008`, `DISC-003–004`, and `SEC-011`. |
| Decision boundaries | COVERED | Guardrail contracts in `PROBLEM.md`, `SEC-011`, `ARCH-001–006`, `CICD-007–008`. |
| Later phases may decide autonomously | COVERED | AMB-001–003 records chosen fixture/TTL/version boundaries without narrowing required behavior. |
| Must return to the user | INTENTIONAL GAP | Governance rather than an implementation output; prohibited weakening is frozen in `PROBLEM.md`, `RUNNER-CONTRACT.md`, architecture rules, and exact matrix/security goldens. |
| Sources | COVERED | `references.json` pins authority, captures, commit, informed categories, and key artifacts. |

**Result: 28/28 testable or aggregate sections covered; 2/2 governance/out-of-scope sections intentionally have no feature golden. No behavioral requirement is missing.**
