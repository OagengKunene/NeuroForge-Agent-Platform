# Development guide

## Local services

Start the complete stack:

```bash
cp .env.example .env
docker compose up --build
```

Stop services:

```bash
docker compose down
```

Remove local database data too:

```bash
docker compose down -v
```

## Python tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r ml-service/requirements.txt
PYTHONPATH=ml-service pytest ml-service/tests -q
```

## .NET tests

```bash
dotnet restore NeuroForge.sln
dotnet test NeuroForge.sln
```

## MCP server

Install the MCP dependencies and run the stdio tool server:

```bash
pip install -r src/NeuroForge.Mcp/requirements.txt
python src/NeuroForge.Mcp/server.py
```

Connect it from a compatible MCP client using a local stdio process configuration. Do not publish local MCP tools to the public internet without authentication and a threat review.
