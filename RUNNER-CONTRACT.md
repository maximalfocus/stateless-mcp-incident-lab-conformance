# Conformance runner contract

The golden files are provider-neutral declarative contracts. A provider binding MUST execute `input.json` through the named public boundary and compare its normalized observation with the complete `expected.json`; it MUST NOT return a precomputed pass record, derive actual output from `expected.json`, or dispatch on `spec_id`/directory name. The input's `operation`, `subject`, `profile`, or `argv` selects a real public adapter. `operation-registry.json` is the single closed named-function registry: every provider binding implements those names verbatim, and the suite validator rejects unknown/dangling names and top-level input/expected fields.

## Boundary dispatch and exact observations

- `http` and `tool-call`: reset `seed.json`, issue `request.json`, and compare status, selected headers, and the complete body. A test with explicit `input.json.requests` executes that sequence and compares the resulting composite observation.
- `sse`: issue `request.json`, apply only the transport fault declared in `input.json`, then compare ordered events, headers, close/cancel state, resources, and any reissued IDs.
- `function`, `state-machine`, `contract`, `workflow-assertion`, `lint-assertion`, `trace-span`, and `metric-assertion`: invoke the named operation/subject/profile against the implementation or artifact and compare the complete returned observation exactly.
- `cli`: execute `argv`; compare exit code, exact stdout/stderr, network-call count, and declared cache observations. JSON embedded in stdout is parsed before placeholder normalization and then serialized compactly with a trailing newline.
- `property`: execute the `property` block with a property-testing library, always replay concrete `examples`, and emit `{"holds": true}` only after all iterations hold.

## Assertion vocabulary

- `strict_http_shape`: exact status, declared headers, and complete normalized body. Undeclared body fields fail. `{{ALLOW_EXTRA}}` tolerates undeclared keys only in its containing object; a sibling `forbidden_headers` list still rejects those names.
- `no_import`: scan every file selected by `from_glob`; fail closed if the glob is unexpectedly empty; reject any canonical import matching `import_pattern`.
- `no_deep_import`: resolve cross-module imports and permit only `allowed_entry`; `same_module: allow` exempts imports within the owning module.

`contract` assertions and free-form prose predicates are forbidden. For non-assertion boundaries, the complete `expected.json` is itself the executable assertion. A missing observer, unknown operation, unknown assertion/field, or empty artifact glob fails rather than skipping.

## Provider and fixture rules

`providers` selects raw, SDK, or both. HTTP requests target the selected provider's `/raw/mcp` or `/sdk/mcp` binding even when the fixture uses `/raw/mcp` as the canonical path. `SEEDED-DETERMINISTIC-INCIDENT-LAB` is reset before each test. Generated IDs and timestamps are normalized only after UUID/entropy and RFC 3339 checks. Placeholder matching applies recursively, including parsed JSON compatibility text; it never replaces an implementation value before validating that value's declared format. The runner rejects spec-ID dispatch, unknown operations, unknown fields, tests with no expected observation, missing observations, and empty architecture globs.
