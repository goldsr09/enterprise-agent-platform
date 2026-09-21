import json
import subprocess
import os
import anyio
import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

MCP_URL = "https://enterprise-agent-mcp-kyanbv5hhq-uc.a.run.app/mcp"


async def main():
    token = os.getenv("MCP_ID_TOKEN")

    if not token:
        token = subprocess.check_output(
            ["gcloud", "auth", "print-identity-token"],
            text=True,
        ).strip()

    async with httpx2.AsyncClient(
        headers={"Authorization": f"Bearer {token}"},
        timeout=120.0,
    ) as http:
        transport = streamable_http_client(
            MCP_URL,
            http_client=http,
        )

        async with Client(transport) as client:
            tools = await client.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])

            cases = [
                (
                    "get_metrics",
                    {
                        "platform": "Android",
                        "start_date": "2026-09-15",
                        "end_date": "2026-09-16",
                    },
                ),
                (
                    "search_runbook",
                    {"query": "What should I investigate when Android traffic drops?"},
                ),
            ]

            failures = []
            for name, arguments in cases:
                result = await client.call_tool(name, arguments)
                print(f"\nTool: {name}")
                print("Failed:", result.is_error)
                print(json.dumps(result.structured_content, indent=2, default=str))

                if result.is_error:
                    print("Error details:", result.content)
                    failures.append(name)

            if failures:
                raise RuntimeError(f"Cloud tool tests failed: {failures}")

            print("\nBoth cloud MCP tools succeeded.")


if __name__ == "__main__":
    anyio.run(main)
