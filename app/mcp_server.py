import json
from dotenv import load_dotenv
from mcp.server import MCPServer
from app.tools.rag_tool import search_runbook_semantically
from app.tools.sql_tool import get_metrics_tool
import os


load_dotenv()

mcp = MCPServer(
    "enterprise-agent-platform"
)

@mcp.tool()
def get_metrics(platform: str, start_date: str,end_date: str ) -> list[dict]:
    """Get platform metrics for an inclusive ISO date range."""

    result = get_metrics_tool.invoke({
        "platform": platform,
        "start_date": start_date,
        "end_date": end_date
    })

    return json.loads(
        json.dumps(result, default=str)
    )


@mcp.tool()
def search_runbook(query: str) -> list[dict]:
    """Search operational guidance using semantic similarity."""

    return search_runbook_semantically.invoke({
        "query": query
    })


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8001")),
        stateless_http=True,
        json_response=True,
    )