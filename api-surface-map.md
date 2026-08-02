# API surface map

| Surface | Classification | Categories | Coverage target |
|---|---|---|---:|
| JSON-RPC and MCP message schema | Standard/protocol | protocol, versioning | 100% selected MUSTs |
| Streamable HTTP, SSE, progress, cancellation | Standard/protocol | transport, streaming | 100% selected MUSTs |
| Discovery, tools, resources, prompts, pagination, caching, elicitation | Standard/protocol | discovery, primitives, cache, mrtr | 100% selected surface |
| Incident simulator and lifecycle | Domain rule | incidents | 100% transitions and failures |
| CLI and four-way provider matrix | Domain/derived | cli, interoperability | 100% commands and combinations |
| Security, observability, performance | Derived/NFR | security, observability, performance, properties | 100% PRD targets |
| Architecture, cloud, pipeline, dependencies | Structural/domain | architecture, infra, cicd, dependencies | 100% PLAN assertions |
| Auth, legacy sessions, extensions, GUI, production operations | Intentional gap | — | 0% by design |
