import anyio

from mcp import Client


async def main():
    async with Client(
        "http://127.0.0.1:8001/mcp"
    ) as client:
        tools_result = await client.list_tools()

        print(
            "Available tools:",
            [tool.name for tool in tools_result.tools]
        )

        result = await client.call_tool(
            "search_runbook",
            {
                "query": (
                    "What should I investigate when "
                    "Android traffic drops?"
                )
            }
        )
        

        print("Tool failed:", result.is_error)
        print("Result:", result.structured_content)

        metrics_result = await client.call_tool(
    "get_metrics",
    {
        "platform": "Android",
        "start_date": "2026-09-15",
        "end_date": "2026-09-16"
    }
)

        print("\nMetrics tool failed:", metrics_result.is_error)
        print("Metrics result:", metrics_result.structured_content)


if __name__ == "__main__":
    anyio.run(main)