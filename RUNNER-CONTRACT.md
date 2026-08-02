# Conformance runner contract

The golden files are provider-neutral declarative contracts. A provider binding MUST execute each `input.json` scenario through the named public boundary and evaluate every assertion in `expected.json`; it MUST NOT return a precomputed pass record or derive actual output from `expected.json`.

## Assertion vocabulary

- `contract`: execute `subject` and prove the complete behavior in `must`. The runner reports a mismatch with concrete expected/actual evidence for every clause; a missing observer is a failure, never a skip.
- `strict_http_shape`: compare status, selected headers, and the complete normalized body exactly. Undeclared body fields fail; only an object carrying `{{ALLOW_EXTRA}}` tolerates undeclared keys.
- `no_import`: scan every file selected by `from_glob`; fail closed if the glob is unexpectedly empty; reject any canonical import matching `import_pattern`.
- `no_deep_import`: resolve cross-module imports and permit only `allowed_entry`; `same_module: allow` exempts imports within the owning module.

Property boundaries execute the `property` block with a property-testing library, always replay `examples`, and emit `{"holds": true}` only after all iterations hold. Metric assertions run only under the controlled profile named by the test and emit their measured evidence on failure.

## Provider and fixture rules

`providers` selects raw, SDK, or both. HTTP requests target the selected provider's `/raw/mcp` or `/sdk/mcp` binding even when the fixture uses `/raw/mcp` as the canonical path. `SEEDED-DETERMINISTIC-INCIDENT-LAB` is reset before each test. Generated IDs and timestamps are normalized only after the runner has checked UUID/entropy and RFC 3339 constraints. The runner rejects unknown assertion types, unknown fields, tests with no assertion, missing observations, and empty architecture globs.
