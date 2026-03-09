from dataclasses import dataclass


@dataclass(slots=True)
class MCPClient:
    """Reserved integration surface for future MCP server connectivity."""

    server_url: str

    def fetch_context(self, tenant_id: str, query: str) -> str:
        # Placeholder: wire to MCP protocol transport later.
        return f"MCP context for tenant={tenant_id}, query='{query[:40]}'"
