# protocol

Language-neutral exact fixtures for the protocol-core function boundary. A provider binding implements the closed operation vocabulary below and compares its complete normalized return value to `expected.json`; unknown operations or extra return fields fail.

- `validate_request`, `validate_notification`, `validate_message`
- `validate_result_response`, `validate_error_response`
- `decode_jsonrpc`, `dispatch_method`
- `validate_json_schema`

The binding must call the implementation's production codec/dispatcher/validator, never a parallel fixture oracle. `generated` schema inputs are deterministic fixture constructors owned by the runner; their complete parameters are committed and contain no hidden expected output.
