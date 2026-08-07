# infra

Declarative, language-neutral function contracts. `expected.json` is authoritative and must never be auto-updated. The implementation runner evaluates each closed policy-registry check against synthesized CloudFormation and lifecycle artifacts, and separately proves each declared cross-resource correlation obligation, receipting both in `evaluated_checks` and `proved_obligations`.

## Policy requirement notation

Every `policy-registry.json` check is dispatched by its complete check ID; unknown IDs, selectors, operators, or unresolved paths fail closed. Its `requirement` is the normative, implementation-neutral expression the dispatcher must prove:

- `;` joins predicates with logical AND.
- A dotted selector identifies one semantic value in the rendered artifact; selectors resolve wiring, not mere resource existence.
- `=` requires exact scalar equality; comma-separated right-hand values denote an exact unordered set.
- `>`, `>=`, and `<=` compare numeric values.
- `selector[index]=source` requires the named map or header entry to be assigned from that source. `overwrite[...]` additionally requires replacement of any input value, never append or preserve.
- Compound selectors such as `waf.rate_rule.custom_key` refer to one resource instance; predicates sharing that prefix must be satisfied by the same rate rule.
- `|` lists explicitly permitted alternatives. No unlisted mechanism is accepted.

A `correlation_obligation` is not prose evidence: the runner must inspect the synthesized cross-resource graph or execute the lifecycle behavior, then copy the obligation exactly into `proved_obligations`. In particular, INFRA-005 requires the viewer-request overwrite association on every CloudFront behavior that forwards to the ALB.

INFRA-004–006 and INFRA-010 implement accepted ADR-0005: CloudFront-generated HTTPS, a private VPC-origin ALB, bootstrapless asset-free synthesis, and direct CloudFormation deploy/verify/destroy. INFRA-005's viewer-IP WAF mechanism additionally follows accepted ADR-0006, which supersedes ADR-0005's invalid forwarded-IP contract.
