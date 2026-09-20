import anyio
from mcp import Client
from app.mcp_server import mcp

async def main():
    async with Client(mcp, raise_exceptions=True) as client:
        tools_result = await client.list_tools()
        print("Available tools:")
        for tool in tools_result.tools:
            print(f"\n- {tool.name}")
            print("  Description:", tool.description)
            print("  Input schema:", tool.input_schema)

        result = await client.call_tool(
            "search_runbook",
            {
                "query": (
                    "What should I investigate when "
                    "Android traffic drops?"
                )
            }
        )

        print("\nTool failed:", result.is_error)
        print("Structured result:")
        print(result.structured_content)


if __name__ == "__main__":
    anyio.run(main)        