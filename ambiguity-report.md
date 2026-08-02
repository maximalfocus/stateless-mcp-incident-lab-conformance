# Ambiguity report

## AMB-001: Deterministic fictional fixture content

**Affected:** PRIM-001–020, INC-001–012, CLI-001–014.

**Ambiguity:** The PRD intentionally leaves service names, telemetry text, runbook prose, and seeded incident values to authoring.

**Decision:** Implementations use one shared logical fixture vocabulary supplied by the conformance runner; exact prose may differ only where a golden uses `{{ANY_STRING}}`. Ordering, IDs, state, severity, timestamps, and relationships remain exact.

**Rationale:** Representative deterministic data tests protocol and domain logic without pretending production rates or names are requirements.

## AMB-002: Concrete cache TTL and progress cadence

**Affected:** DISC-006, CACHE-002/005/006/009, STREAM-003.

**Ambiguity:** Requirements constrain semantics but permit concrete TTL and cadence choices.

**Decision:** Runners use a fake clock; assertions require nonnegative TTL, freshness boundaries, monotonic progress, and rate limiting without pinning wall-clock durations beyond requestState's required five-minute expiry.

**Rationale:** This preserves observable laws and eliminates timing flakes.

## AMB-003: SDK package version

**Affected:** DEP-001–005 and the SDK implementation binding.

**Ambiguity:** PLAN-001 requires the first stable SDK release declaring 2026-07-28 support, but no version is normatively fixed in the protocol contract.

**Decision:** Conformance pins protocol revision and observable behavior, not an SDK semver. Implementation must select and lock a stable supporting release; if none exists it stops for user review.

**Rationale:** A package version is an implementation binding and must not weaken the shared cross-provider contract.

## AMB-004: Work-item completion across independent implementations

**Affected:** `WORKITEMS.md`; all implementation consumers.

**Ambiguity:** One status cell cannot represent completion independently for raw and SDK implementations, while interoperability, infrastructure, and CI/CD contracts are not owned by either implementation repository.

**Decision:** Work items are partitioned into five explicit lanes: `raw`, `sdk`, `integration`, `infrastructure`, and `cicd`. One `/cdd-implement` invocation selects exactly one lane and never mutates another. Shared goldens are replayed independently in both implementation lanes; family integration begins only after both implementation lanes complete.

**Rationale:** Status now records the repository that actually proved the contract and cannot cause the second implementation to skip work completed only by the first.
