# Author self-review — invalidated by peer review

The original authoring pass marked every item complete, but the degraded peer-review fallback disproved that claim. Only `architecture/` and the rewritten `protocol/` category currently carry replayable machine-checkable expectations.

- [ ] 8a — complete expected-shape consistency cannot be audited while 184 prose-only assertions remain.
- [ ] 8b — structural lint passes, but `scripts/validate-suite.py` correctly fails on non-replayable contracts.
- [ ] 8c — generic empty seeds and `params.scenario` do not establish request/seed coherence.
- [ ] 8d — placeholders must be re-audited after concrete outputs replace prose assertions.
- [ ] 8e — BDD descriptions must be checked against concrete expected values during each category rewrite.
- [ ] 8f — greenfield source citations must be narrowed to exact normative sections during rewrite.
- [ ] 8g — named negative cases exist as directory labels, but most do not yet carry decisive malformed inputs and exact outputs.

Implementation is blocked until these are completed and cross-vendor `/peerreview` converges.
