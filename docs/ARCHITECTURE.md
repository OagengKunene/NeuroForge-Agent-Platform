# Architecture and engineering decisions

## Runtime boundaries

- **Agent API (.NET 8):** HTTP boundary, request validation, Semantic Kernel host and downstream ML client.
- **ML inference (Python):** independent FastAPI service. It owns model loading and input validation.
- **MCP tools:** stdio server for local agent/tool experimentation. It is deliberately not exposed over an unauthenticated network transport.
- **PostgreSQL:** initial persistence foundation. The API does not yet write session records; schema is provisioned for the next milestone.

## Request flow

1. Client submits a prompt to `POST /api/agent/ask`.
2. The API uses Semantic Kernel with an OpenAI chat completion when `OPENAI_API_KEY` is configured.
3. Without a key, a deterministic fallback makes local smoke testing possible.
4. ML inference requests are forwarded by the typed `MlInferenceClient` to the Python service.

## Reliability and security

- Each service has an independent container boundary.
- ML service has a Docker health check; API waits for it during Compose startup.
- Credentials are injected through environment variables and are not stored in source control.
- MCP uses stdio to avoid exposing tool execution to a network by default.
- Before production: add authentication/authorization, request limits, TLS, secret management, structured telemetry, database migrations, model provenance and threat modelling.

## Model governance

The included model is trained from seeded synthetic data only. Its purpose is to verify serialization, validation and inference wiring. It must not be used for real operational decisions. A production model needs documented data lineage, train/validation/test separation, baseline comparisons, metrics, bias/error analysis, drift monitoring and a versioned approval process.
