# Author self-review

- [x] 8a — all expected files recursively audited against convention-reference and suite-invariants.
- [x] 8b — recursive structural validator and shared golden-lint passed.
- [x] 8c — HTTP fixtures use deterministic empty seed where no domain seed is needed; logical fixture scenario is declared consistently.
- [x] 8d — placeholders restricted to declared values; generated IDs/timestamps are normalized, never hard-coded.
- [x] 8e — every BDD then clause is generated from and equal in meaning to the authoritative description.
- [x] 8f — not applicable: greenfield suite; source citations point to PRD/PLAN and captured normative specification rather than implementation code.
- [x] 8g — transport/protocol/domain/MRTR/security negative conditions include 400/403/404/405/409-equivalent domain conflict, 413/504, capability-disabled, tamper, expiry, decline, and cancellation paths.
