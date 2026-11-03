# NeuroForge Agent Platform

An advanced, modular AI-agent platform demonstrating **C# / Microsoft Semantic Kernel**, **Python machine-learning services**, **Model Context Protocol (MCP)**, **Docker Compose**, and **GitHub Actions CI/CD**.

> Portfolio engineering project. The initial release provides a runnable local development foundation and clear extension points. It does not claim production deployment, trained model performance, or cloud hosting.

## Architecture

```text
                  Client / API consumer
                           |
                    .NET 8 Web API
                 Semantic Kernel host
                    /           \
             MCP tools       ML service
             (stdio)         FastAPI
                                |
                         scikit-learn model
                                |
                          model artifact

       Docker Compose: API + ML API + PostgreSQL
       GitHub Actions: lint/test/build on push and PR
```

## Stack

| Layer | Technology |
|---|---|
| Agent orchestration | C# / .NET 8 / Semantic Kernel |
| ML inference | Python 3.11 / FastAPI / scikit-learn |
| Tool integration | MCP server (Python, stdio transport) |
| Persistence | PostgreSQL |
| Packaging | Docker / Docker Compose |
| Quality gates | GitHub Actions, pytest, .NET tests |
| Model lifecycle | MLflow-ready extension point; baseline artifact pipeline |

## Quick start

Requirements: Docker Desktop with Compose, or .NET 8 and Python 3.11 for running services separately.

```bash
cp .env.example .env
docker compose up --build
```

- Agent API: http://localhost:8080/health
- ML API: http://localhost:8000/health
- ML prediction: `POST http://localhost:8000/predict`

Example request:

```json
{
  "features": {
    "temperature": 22.5,
    "humidity": 61.0,
    "pressure": 1012.4
  }
}
```

The included model is a deterministic synthetic demonstration model, not a validated real-world predictor. Replace the sample dataset and evaluation protocol before making domain claims.

## Repository layout

```text
src/
  NeuroForge.Api/       .NET API and Semantic Kernel orchestration
  NeuroForge.Mcp/       MCP tool server
ml-service/             FastAPI inference service and model training
tests/
  NeuroForge.Api.Tests/ .NET API tests
  ml-service/           Python tests
infra/                  PostgreSQL initialization
.github/workflows/      CI pipelines
```

## Configuration

Copy `.env.example` to `.env`. The API supports an optional OpenAI-compatible chat deployment through environment variables. Without credentials, deterministic local orchestration remains available for smoke tests. Never commit API keys or connection secrets.

## Development

Python:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r ml-service/requirements.txt
pytest ml-service/tests -q
```

.NET:

```bash
dotnet test
dotnet run --project src/NeuroForge.Api
```

## CI/CD

GitHub Actions runs Python tests, .NET build/tests, and Docker image builds on pushes and pull requests. Deployment is intentionally not configured until a target registry/hosting provider and repository secrets are selected.

## Security notes

- Use environment variables or a secret manager for credentials.
- Restrict exposed ports and database access in production.
- Add authentication, authorization, rate limiting, structured audit logging, and TLS before public deployment.
- Treat model inputs and tool outputs as untrusted.
- Review dependency updates and pin production images by digest.

## Roadmap

- [x] Modular .NET agent host and Python inference service
- [x] Docker Compose local stack
- [x] MCP tool server
- [x] Automated test and build workflows
- [ ] Add a real, versioned domain dataset and model evaluation report
- [ ] Add authenticated user sessions and durable agent memory
- [ ] Add MLflow tracking and model registry
- [ ] Add deployment workflow after hosting target is chosen

## License

MIT. See [LICENSE](LICENSE).
