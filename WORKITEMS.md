# Work items

Status: `[ ]` pending · `[~]` in progress · `[x]` done · `[!]` blocked

Structure and ordering are immutable after conformance review; implementation changes status cells only.

## Phase 1: Architecture

- [ ] **WI-001** architecture contracts 1–3 (3 tests)
  - Tests: `conformance/architecture/boundaries/005-raw-public-module-boundaries`, `conformance/architecture/boundaries/006-sdk-public-module-boundaries`, `conformance/architecture/dependencies/001-raw-layer-dependencies`
  - Scope: `scripts/verify-architecture.ts, src/**/index.ts`
  - Depends on: none

- [ ] **WI-002** architecture contracts 4–6 (3 tests)
  - Tests: `conformance/architecture/dependencies/002-raw-adapter-independence`, `conformance/architecture/dependencies/003-sdk-layer-dependencies`, `conformance/architecture/dependencies/004-sdk-adapter-independence`
  - Scope: `scripts/verify-architecture.ts, src/**/index.ts`
  - Depends on: WI-001

## Phase 2: Protocol

- [ ] **WI-003** protocol contracts 1–3 (3 tests)
  - Tests: `conformance/protocol/001-valid-request-shape`, `conformance/protocol/002-valid-notification-shape`, `conformance/protocol/003-reject-null-request-id`
  - Scope: `src/protocol/codec.ts, src/protocol/schema.ts`
  - Depends on: WI-002

- [ ] **WI-004** protocol contracts 4–6 (3 tests)
  - Tests: `conformance/protocol/004-reject-nonscalar-request-id`, `conformance/protocol/005-complete-result-shape`, `conformance/protocol/006-input-required-result-shape`
  - Scope: `src/protocol/codec.ts, src/protocol/schema.ts`
  - Depends on: WI-003

- [ ] **WI-005** protocol contracts 7–9 (3 tests)
  - Tests: `conformance/protocol/007-error-shape-no-result-meta`, `conformance/protocol/008-parse-error`, `conformance/protocol/009-invalid-request-shape`
  - Scope: `src/protocol/codec.ts, src/protocol/schema.ts`
  - Depends on: WI-004

- [ ] **WI-006** protocol contracts 10–12 (3 tests)
  - Tests: `conformance/protocol/010-unknown-method-code`, `conformance/protocol/011-unknown-tool-is-invalid-params`, `conformance/protocol/012-schema-safety-bounds`
  - Scope: `src/protocol/codec.ts, src/protocol/schema.ts`
  - Depends on: WI-005

## Phase 3: Versioning

- [ ] **WI-007** versioning contracts 1–3 (3 tests)
  - Tests: `conformance/versioning/001-metadata-in-params`, `conformance/versioning/002-reject-top-level-meta-only`, `conformance/versioning/003-client-info-optional`
  - Scope: `src/protocol/version.ts, src/client/version.ts`
  - Depends on: WI-006

- [ ] **WI-008** versioning contracts 4–6 (3 tests)
  - Tests: `conformance/versioning/004-per-request-version`, `conformance/versioning/005-per-request-capabilities`, `conformance/versioning/006-unsupported-version`
  - Scope: `src/protocol/version.ts, src/client/version.ts`
  - Depends on: WI-007

- [ ] **WI-009** versioning contracts 7–10 (4 tests)
  - Tests: `conformance/versioning/007-client-version-recovery`, `conformance/versioning/008-no-discovery-prerequisite`, `conformance/versioning/009-no-session-id-response`, `conformance/versioning/010-no-session-affinity`
  - Scope: `src/protocol/version.ts, src/client/version.ts`
  - Depends on: WI-008

## Phase 4: Transport

- [ ] **WI-010** transport contracts 1–3 (3 tests)
  - Tests: `conformance/transport/001-post-json-response`, `conformance/transport/002-notification-accepted`, `conformance/transport/003-reject-batch-array`
  - Scope: `src/adapters/inbound/http.ts, src/client/http.ts`
  - Depends on: WI-009

- [ ] **WI-011** transport contracts 4–6 (3 tests)
  - Tests: `conformance/transport/004-reject-client-response`, `conformance/transport/005-get-method-not-allowed`, `conformance/transport/006-delete-method-not-allowed`
  - Scope: `src/adapters/inbound/http.ts, src/client/http.ts`
  - Depends on: WI-010

- [ ] **WI-012** transport contracts 7–9 (3 tests)
  - Tests: `conformance/transport/007-invalid-origin-first`, `conformance/transport/008-ignore-last-event-id`, `conformance/transport/009-required-version-header`
  - Scope: `src/adapters/inbound/http.ts, src/client/http.ts`
  - Depends on: WI-011

- [ ] **WI-013** transport contracts 10–12 (3 tests)
  - Tests: `conformance/transport/010-required-method-header`, `conformance/transport/011-required-name-header`, `conformance/transport/012-header-body-value-match`
  - Scope: `src/adapters/inbound/http.ts, src/client/http.ts`
  - Depends on: WI-012

- [ ] **WI-014** transport contracts 13–15 (3 tests)
  - Tests: `conformance/transport/013-header-names-case-insensitive`, `conformance/transport/014-base64-sentinel-roundtrip`, `conformance/transport/015-omit-null-param-header`
  - Scope: `src/adapters/inbound/http.ts, src/client/http.ts`
  - Depends on: WI-013

- [ ] **WI-015** transport contracts 16–18 (3 tests)
  - Tests: `conformance/transport/016-invalid-header-annotation-hidden`, `conformance/transport/017-payload-too-large`, `conformance/transport/018-deadline-before-stream`
  - Scope: `src/adapters/inbound/http.ts, src/client/http.ts`
  - Depends on: WI-014

## Phase 5: Discovery

- [ ] **WI-016** discovery contracts 1–3 (3 tests)
  - Tests: `conformance/discovery/001-supported-version`, `conformance/discovery/002-exact-capabilities`, `conformance/discovery/003-no-list-changed`
  - Scope: `src/application/discover.ts`
  - Depends on: WI-015

- [ ] **WI-017** discovery contracts 4–6 (3 tests)
  - Tests: `conformance/discovery/004-no-subscribe-logging-completions`, `conformance/discovery/005-identity-and-guidance`, `conformance/discovery/006-public-cache-hints`
  - Scope: `src/application/discover.ts`
  - Depends on: WI-016

## Phase 6: Primitives

- [ ] **WI-018** primitives contracts 1–3 (3 tests)
  - Tests: `conformance/primitives/001-tools-list-order`, `conformance/primitives/002-tools-list-schemas`, `conformance/primitives/003-tools-list-pagination`
  - Scope: `src/application/catalogs.ts, src/application/tools.ts`
  - Depends on: WI-017

- [ ] **WI-019** primitives contracts 4–6 (3 tests)
  - Tests: `conformance/primitives/004-resources-list-safe-catalog`, `conformance/primitives/005-resource-templates-list`, `conformance/primitives/006-resources-list-order`
  - Scope: `src/application/catalogs.ts, src/application/tools.ts`
  - Depends on: WI-018

- [ ] **WI-020** primitives contracts 7–9 (3 tests)
  - Tests: `conformance/primitives/007-topology-read`, `conformance/primitives/008-runbook-read`, `conformance/primitives/009-timeline-read`
  - Scope: `src/application/catalogs.ts, src/application/tools.ts`
  - Depends on: WI-019

- [ ] **WI-021** primitives contracts 10–12 (3 tests)
  - Tests: `conformance/primitives/010-unknown-resource`, `conformance/primitives/011-prompts-list-order`, `conformance/primitives/012-triage-prompt-get`
  - Scope: `src/application/catalogs.ts, src/application/tools.ts`
  - Depends on: WI-020

- [ ] **WI-022** primitives contracts 13–15 (3 tests)
  - Tests: `conformance/primitives/013-review-prompt-get`, `conformance/primitives/014-unknown-prompt`, `conformance/primitives/015-missing-prompt-argument`
  - Scope: `src/application/catalogs.ts, src/application/tools.ts`
  - Depends on: WI-021

- [ ] **WI-023** primitives contracts 16–18 (3 tests)
  - Tests: `conformance/primitives/016-create-incident-output`, `conformance/primitives/017-query-telemetry-output`, `conformance/primitives/018-run-diagnostic-output`
  - Scope: `src/application/catalogs.ts, src/application/tools.ts`
  - Depends on: WI-022

- [ ] **WI-024** primitives contracts 19–20 (2 tests)
  - Tests: `conformance/primitives/019-invalid-cursor`, `conformance/primitives/020-domain-error-split`
  - Scope: `src/application/catalogs.ts, src/application/tools.ts`
  - Depends on: WI-023

## Phase 7: Incidents

- [ ] **WI-025** incidents contracts 1–3 (3 tests)
  - Tests: `conformance/incidents/001-create-open-incident`, `conformance/incidents/002-get-current-incident`, `conformance/incidents/003-open-to-investigating`
  - Scope: `src/domain/incident.ts, src/application/incidents.ts`
  - Depends on: WI-024

- [ ] **WI-026** incidents contracts 4–6 (3 tests)
  - Tests: `conformance/incidents/004-investigating-diagnostic`, `conformance/incidents/005-propose-remediation`, `conformance/incidents/006-accepted-to-mitigated`
  - Scope: `src/domain/incident.ts, src/application/incidents.ts`
  - Depends on: WI-025

- [ ] **WI-027** incidents contracts 7–9 (3 tests)
  - Tests: `conformance/incidents/007-open-to-resolved`, `conformance/incidents/008-investigating-to-resolved`, `conformance/incidents/009-mitigated-to-resolved`
  - Scope: `src/domain/incident.ts, src/application/incidents.ts`
  - Depends on: WI-026

- [ ] **WI-028** incidents contracts 10–12 (3 tests)
  - Tests: `conformance/incidents/010-reject-resolved-transition`, `conformance/incidents/011-unknown-handle-recovery`, `conformance/incidents/012-expired-handle-recovery`
  - Scope: `src/domain/incident.ts, src/application/incidents.ts`
  - Depends on: WI-027

## Phase 8: Mrtr

- [ ] **WI-029** mrtr contracts 1–3 (3 tests)
  - Tests: `conformance/mrtr/001-initial-input-required`, `conformance/mrtr/002-form-capability-required`, `conformance/mrtr/003-url-only-capability-rejected`
  - Scope: `src/application/mrtr.ts, src/adapters/outbound/request-state.ts`
  - Depends on: WI-028

- [ ] **WI-030** mrtr contracts 4–6 (3 tests)
  - Tests: `conformance/mrtr/004-bare-elicitation-supports-form`, `conformance/mrtr/005-flat-primitive-schema`, `conformance/mrtr/006-new-retry-id`
  - Scope: `src/application/mrtr.ts, src/adapters/outbound/request-state.ts`
  - Depends on: WI-029

- [ ] **WI-031** mrtr contracts 7–9 (3 tests)
  - Tests: `conformance/mrtr/007-exact-state-echo`, `conformance/mrtr/008-accept-executes-once`, `conformance/mrtr/009-decline-no-effect`
  - Scope: `src/application/mrtr.ts, src/adapters/outbound/request-state.ts`
  - Depends on: WI-030

- [ ] **WI-032** mrtr contracts 10–12 (3 tests)
  - Tests: `conformance/mrtr/010-cancel-no-effect`, `conformance/mrtr/011-incomplete-reelicits`, `conformance/mrtr/012-tampered-state`
  - Scope: `src/application/mrtr.ts, src/adapters/outbound/request-state.ts`
  - Depends on: WI-031

- [ ] **WI-033** mrtr contracts 13–16 (4 tests)
  - Tests: `conformance/mrtr/013-expired-state`, `conformance/mrtr/014-wrong-method-binding`, `conformance/mrtr/015-wrong-arguments-binding`, `conformance/mrtr/016-cross-replica-retry`
  - Scope: `src/application/mrtr.ts, src/adapters/outbound/request-state.ts`
  - Depends on: WI-032

## Phase 9: Streaming

- [ ] **WI-034** streaming contracts 1–3 (3 tests)
  - Tests: `conformance/streaming/001-string-progress-token`, `conformance/streaming/002-integer-progress-token`, `conformance/streaming/003-monotonic-progress`
  - Scope: `src/adapters/inbound/sse.ts, src/client/sse.ts`
  - Depends on: WI-033

- [ ] **WI-035** streaming contracts 4–6 (3 tests)
  - Tests: `conformance/streaming/004-progress-before-final`, `conformance/streaming/005-no-progress-after-final`, `conformance/streaming/006-disconnect-cancels`
  - Scope: `src/adapters/inbound/sse.ts, src/client/sse.ts`
  - Depends on: WI-034

- [ ] **WI-036** streaming contracts 7–9 (3 tests)
  - Tests: `conformance/streaming/007-broken-stream-reissue`, `conformance/streaming/008-non-buffering-header`, `conformance/streaming/009-deadline-after-stream`
  - Scope: `src/adapters/inbound/sse.ts, src/client/sse.ts`
  - Depends on: WI-035

## Phase 10: Cache

- [ ] **WI-037** cache contracts 1–3 (3 tests)
  - Tests: `conformance/cache/001-exact-six-cacheable`, `conformance/cache/002-nonnegative-ttl`, `conformance/cache/003-scope-by-resource`
  - Scope: `src/client/cache.ts`
  - Depends on: WI-036

- [ ] **WI-038** cache contracts 4–6 (3 tests)
  - Tests: `conformance/cache/004-key-method-params-cursor`, `conformance/cache/005-fresh-hit`, `conformance/cache/006-ttl-not-polling`
  - Scope: `src/client/cache.ts`
  - Depends on: WI-037

- [ ] **WI-039** cache contracts 7–10 (4 tests)
  - Tests: `conformance/cache/007-no-hints-no-cache`, `conformance/cache/008-no-mrtr-cache`, `conformance/cache/009-stale-on-refresh-error`, `conformance/cache/010-full-list-rewalk`
  - Scope: `src/client/cache.ts`
  - Depends on: WI-038

## Phase 11: Cli

- [ ] **WI-040** cli contracts 1–3 (3 tests)
  - Tests: `conformance/cli/001-discover-command`, `conformance/cli/002-tools-list-command`, `conformance/cli/003-tools-inspect-command`
  - Scope: `src/adapters/inbound/cli.ts`
  - Depends on: WI-039

- [ ] **WI-041** cli contracts 4–6 (3 tests)
  - Tests: `conformance/cli/004-tools-call-command`, `conformance/cli/005-resources-list-command`, `conformance/cli/006-resources-templates-command`
  - Scope: `src/adapters/inbound/cli.ts`
  - Depends on: WI-040

- [ ] **WI-042** cli contracts 7–9 (3 tests)
  - Tests: `conformance/cli/007-resources-read-command`, `conformance/cli/008-prompts-list-command`, `conformance/cli/009-prompts-get-command`
  - Scope: `src/adapters/inbound/cli.ts`
  - Depends on: WI-041

- [ ] **WI-043** cli contracts 10–12 (3 tests)
  - Tests: `conformance/cli/010-demo-approve-command`, `conformance/cli/011-demo-decline-command`, `conformance/cli/012-demo-cancel-command`
  - Scope: `src/adapters/inbound/cli.ts`
  - Depends on: WI-042

- [ ] **WI-044** cli contracts 13–14 (2 tests)
  - Tests: `conformance/cli/013-wire-redaction`, `conformance/cli/014-no-cache-and-exit-codes`
  - Scope: `src/adapters/inbound/cli.ts`
  - Depends on: WI-043

## Phase 12: Properties

- [ ] **WI-045** properties contracts 1–3 (3 tests)
  - Tests: `conformance/properties/001-header-codec-roundtrip`, `conformance/properties/002-cache-key-stability`, `conformance/properties/003-cache-key-separation`
  - Scope: `src/protocol/headers.ts, src/client/cache-key.ts`
  - Depends on: WI-044

- [ ] **WI-046** properties contracts 4–7 (4 tests)
  - Tests: `conformance/properties/004-deterministic-catalog-order`, `conformance/properties/005-request-state-tamper-rejection`, `conformance/properties/006-replica-independence`, `conformance/properties/007-remediation-at-most-once`
  - Scope: `src/protocol/headers.ts, src/client/cache-key.ts`
  - Depends on: WI-045

## Phase 13: Security

- [ ] **WI-047** security contracts 1–3 (3 tests)
  - Tests: `conformance/security/001-origin-rebinding-defense`, `conformance/security/002-header-injection-rejected`, `conformance/security/003-bounded-schema-depth`
  - Scope: `src/protocol/validation.ts, src/adapters/inbound/security.ts`
  - Depends on: WI-046

- [ ] **WI-048** security contracts 4–6 (3 tests)
  - Tests: `conformance/security/004-bounded-subschema-count`, `conformance/security/005-network-ref-refused`, `conformance/security/006-body-bound-no-effect`
  - Scope: `src/protocol/validation.ts, src/adapters/inbound/security.ts`
  - Depends on: WI-047

- [ ] **WI-049** security contracts 7–9 (3 tests)
  - Tests: `conformance/security/007-deadline-no-partial-effect`, `conformance/security/008-handle-entropy-and-ttl`, `conformance/security/009-catalog-handle-non-enumeration`
  - Scope: `src/protocol/validation.ts, src/adapters/inbound/security.ts`
  - Depends on: WI-048

- [ ] **WI-050** security contracts 10–12 (3 tests)
  - Tests: `conformance/security/010-sensitive-log-redaction`, `conformance/security/011-simulated-actions-only`, `conformance/security/012-dependency-severity-floor`
  - Scope: `src/protocol/validation.ts, src/adapters/inbound/security.ts`
  - Depends on: WI-049

## Phase 14: Dependencies

- [ ] **WI-051** dependencies contracts 1–3 (3 tests)
  - Tests: `conformance/dependencies/001-lockfile-reproducible`, `conformance/dependencies/002-approved-licenses`, `conformance/dependencies/003-audit-floor`
  - Scope: `package.json, package-lock.json`
  - Depends on: WI-050

- [ ] **WI-052** dependencies contracts 4–5 (2 tests)
  - Tests: `conformance/dependencies/004-expiring-suppressions`, `conformance/dependencies/005-raw-sdk-absence`
  - Scope: `package.json, package-lock.json`
  - Depends on: WI-051

## Phase 15: Interoperability

- [ ] **WI-053** interoperability contracts 1–3 (3 tests)
  - Tests: `conformance/interoperability/001-raw-client-raw-server-discovery`, `conformance/interoperability/002-raw-client-sdk-server-discovery`, `conformance/interoperability/003-sdk-client-raw-server-discovery`
  - Scope: `test/conformance/interop-runner.ts`
  - Depends on: WI-052

- [ ] **WI-054** interoperability contracts 4–6 (3 tests)
  - Tests: `conformance/interoperability/004-sdk-client-sdk-server-discovery`, `conformance/interoperability/005-raw-client-raw-server-workflow`, `conformance/interoperability/006-raw-client-sdk-server-workflow`
  - Scope: `test/conformance/interop-runner.ts`
  - Depends on: WI-053

- [ ] **WI-055** interoperability contracts 7–9 (3 tests)
  - Tests: `conformance/interoperability/007-sdk-client-raw-server-workflow`, `conformance/interoperability/008-sdk-client-sdk-server-workflow`, `conformance/interoperability/009-matrix-equivalent-observables`
  - Scope: `test/conformance/interop-runner.ts`
  - Depends on: WI-054

- [ ] **WI-056** interoperability contracts 10–12 (3 tests)
  - Tests: `conformance/interoperability/010-allowed-metadata-difference`, `conformance/interoperability/011-local-public-distribution`, `conformance/interoperability/012-local-direct-cross-replica`
  - Scope: `test/conformance/interop-runner.ts`
  - Depends on: WI-055

## Phase 16: Observability

- [ ] **WI-057** observability contracts 1–3 (3 tests)
  - Tests: `conformance/observability/001-raw-health-ready`, `conformance/observability/002-sdk-health-ready`, `conformance/observability/003-health-unavailable`
  - Scope: `src/adapters/outbound/telemetry.ts, src/adapters/inbound/health.ts`
  - Depends on: WI-056

- [ ] **WI-058** observability contracts 4–7 (4 tests)
  - Tests: `conformance/observability/004-trace-context-propagation`, `conformance/observability/005-structured-log-fields`, `conformance/observability/006-error-log-replica`, `conformance/observability/007-sensitive-fields-absent`
  - Scope: `src/adapters/outbound/telemetry.ts, src/adapters/inbound/health.ts`
  - Depends on: WI-057

## Phase 17: Performance

- [ ] **WI-059** performance contracts 1–3 (3 tests)
  - Tests: `conformance/performance/001-catalog-latency`, `conformance/performance/002-replica-distribution`, `conformance/performance/003-concurrent-idempotency`
  - Scope: `test/performance/catalog.js, test/performance/mrtr.js`
  - Depends on: WI-058

## Phase 18: Infra

- [ ] **WI-060** infra contracts 1–3 (3 tests)
  - Tests: `conformance/infra/001-dynamodb-policy`, `conformance/infra/002-immutable-images`, `conformance/infra/003-two-task-services`
  - Scope: `../stateless-mcp-incident-lab-infrastructure/lib/stack.ts`
  - Depends on: WI-059

- [ ] **WI-061** infra contracts 4–6 (3 tests)
  - Tests: `conformance/infra/004-https-only-alb`, `conformance/infra/005-waf-rate-rule`, `conformance/infra/006-least-privilege-network-iam`
  - Scope: `../stateless-mcp-incident-lab-infrastructure/lib/stack.ts`
  - Depends on: WI-060

- [ ] **WI-062** infra contracts 7–10 (4 tests)
  - Tests: `conformance/infra/007-secret-manager-state-key`, `conformance/infra/008-access-log-redaction`, `conformance/infra/009-required-tags-retention`, `conformance/infra/010-deploy-verify-destroy`
  - Scope: `../stateless-mcp-incident-lab-infrastructure/lib/stack.ts`
  - Depends on: WI-061

## Phase 19: Cicd

- [ ] **WI-063** cicd contracts 1–3 (3 tests)
  - Tests: `conformance/cicd/001-quality-gates`, `conformance/cicd/002-four-way-local-matrix`, `conformance/cicd/003-architecture-gate`
  - Scope: `../stateless-mcp-incident-lab-cicd/.github/workflows/quality.yml`
  - Depends on: WI-062

- [ ] **WI-064** cicd contracts 4–6 (3 tests)
  - Tests: `conformance/cicd/004-golden-integrity`, `conformance/cicd/005-immutable-build-output`, `conformance/cicd/006-secretless-oidc`
  - Scope: `../stateless-mcp-incident-lab-cicd/.github/workflows/quality.yml`
  - Depends on: WI-063

- [ ] **WI-065** cicd contracts 7–8 (2 tests)
  - Tests: `conformance/cicd/007-no-ci-cloud-deploy`, `conformance/cicd/008-teardown-on-acceptance`
  - Scope: `../stateless-mcp-incident-lab-cicd/.github/workflows/quality.yml`
  - Depends on: WI-064
