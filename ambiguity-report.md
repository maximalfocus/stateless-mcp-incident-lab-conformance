# Ambiguity report

## AMB-001: Deterministic fictional fixture content

**Affected:** PRIM-001, PRIM-002, PRIM-003, PRIM-004, PRIM-005, PRIM-006, PRIM-007, PRIM-008, PRIM-009, PRIM-010, PRIM-011, PRIM-012, PRIM-013, PRIM-014, PRIM-015, PRIM-016, PRIM-017, PRIM-018, PRIM-019, PRIM-020; INC-001, INC-002, INC-003, INC-004, INC-005, INC-006, INC-007, INC-008, INC-009, INC-010, INC-011, INC-012; CLI-001, CLI-002, CLI-003, CLI-004, CLI-005, CLI-006, CLI-007, CLI-008, CLI-009, CLI-010, CLI-011, CLI-012, CLI-013, CLI-014.

**Ambiguity:** The PRD intentionally leaves service names, telemetry text, runbook prose, and seeded incident values to authoring.

**Decision:** Implementations use one shared logical fixture vocabulary supplied by the conformance runner; exact prose may differ only where a golden uses `{{ANY_STRING}}`. Ordering, IDs, state, severity, timestamps, and relationships remain exact.

**Rationale:** Representative deterministic data tests protocol and domain logic without pretending production rates or names are requirements.

## AMB-002: Concrete cache TTL and progress cadence

**Affected:** DISC-006, CACHE-002, CACHE-005, CACHE-006, CACHE-009, STREAM-003.

**Ambiguity:** Requirements constrain semantics but permit concrete TTL and cadence choices.

**Decision:** Runners use a fake clock; assertions require nonnegative TTL, freshness boundaries, monotonic progress, and rate limiting without pinning wall-clock durations beyond requestState's required five-minute expiry.

**Rationale:** This preserves observable laws and eliminates timing flakes.

## AMB-003: SDK package version

**Affected:** DEP-001, DEP-002, DEP-003, DEP-004, DEP-005 and the SDK implementation binding.

**Ambiguity:** PLAN-001 requires the first stable SDK release declaring 2026-07-28 support, but no version is normatively fixed in the protocol contract.

**Decision:** Conformance pins protocol revision and observable behavior, not an SDK semver. Implementation must select and lock a stable supporting release; if none exists it stops for user review.

**Rationale:** A package version is an implementation binding and must not weaken the shared cross-provider contract.

## AMB-004: Work-item completion across independent implementations

**Affected:** `WORKITEMS.md`; all implementation consumers.

**Ambiguity:** One status cell cannot represent completion independently for raw and SDK implementations, while interoperability, infrastructure, and CI/CD contracts are not owned by either implementation repository.

**Decision:** Work items are partitioned into five explicit lanes: `raw`, `sdk`, `integration`, `infrastructure`, and `cicd`. One `/cdd-implement` invocation selects exactly one lane and never mutates another. Shared goldens are replayed independently in both implementation lanes; family integration begins only after both implementation lanes complete.

**Rationale:** Status now records the repository that actually proved the contract and cannot cause the second implementation to skip work completed only by the first.

## AMB-005: HTTPS topology under restricted AWS account permissions

**Affected:** INFRA-004, INFRA-005, INFRA-006, INFRA-010, WI-112, WI-113.

**Ambiguity:** The PRD requires public HTTPS, but the target account cannot create an ACM certificate, custom hostname, or CDK bootstrap stack. The earlier public-ALB certificate topology is therefore undeployable in the intended account.

**Decision:** Follow accepted ADR-0005: CloudFront's generated hostname and default certificate are the sole public endpoint; a VPC origin reaches an internal ALB; synthesis is bootstrapless and asset-free; direct CloudFormation drives the reviewed multi-stack lifecycle.

**Rationale:** This preserves HTTPS, private workloads, horizontal routing, streaming, WAF, and deterministic teardown without requiring unavailable account capabilities or weakening the public transport requirement.
