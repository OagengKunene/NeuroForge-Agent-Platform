"""Minimal MCP stdio server exposing safe, deterministic platform tools.

Run with: python src/NeuroForge.Mcp/server.py
The MCP server is a local developer tool and is not exposed as an unauthenticated network service.
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("NeuroForge Tools")


@mcp.tool()
def platform_status() -> dict:
    """Return static platform capability information."""
    return {
        "name": "NeuroForge Agent Platform",
        "status": "development",
        "capabilities": ["semantic-kernel-agent-host", "python-ml-inference", "docker-compose", "ci-cd"],
    }


@mcp.tool()
def explain_ml_demo() -> str:
    """Explain the limitations of the bundled demonstration ML model."""
    return (
        "The bundled regression model is trained on synthetic data for integration tests only. "
        "It is not validated for real-world decisions. Replace it with a domain dataset, "
        "document feature provenance, evaluate against held-out data, and version the artifact."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
