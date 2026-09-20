import json

import anyio
from dotenv import load_dotenv
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_openai import ChatOpenAI
from mcp import Client


load_dotenv()

model = ChatOpenAI(
    model="gpt-5.6-luna",
    reasoning_effort="none",
)


async def main():
    async with Client(
        "http://127.0.0.1:8001/mcp"
    ) as mcp_client:
        tools_result = await mcp_client.list_tools()

        tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema,
                },
            }
            for tool in tools_result.tools
        ]

        model_with_tools = model.bind_tools(tool_definitions)

        messages = [
            SystemMessage(
                content=(
                    "Use tools to obtain metrics and operational guidance. "
                    "A failed tool call does not mean no data exists. "
                    "If a tool fails, explain the failure and do not retry "
                    "that tool during this investigation. "
                    "Never invent metrics. "
                    "Cite the source and chunk numbers for runbook guidance. "
                    "Runbook guidance does not prove the cause of a change."
                )
            ),
            HumanMessage(
                content=(
                    "Compare Android sessions between "
                    "2026-09-15 and 2026-09-16. "
                    "Then find relevant operational guidance."
                )
            ),
        ]

        # Bound the loop so the agent cannot run indefinitely.
        for step in range(8):
            response = await model_with_tools.ainvoke(messages)
            messages.append(response)

            if not response.tool_calls:
                print("\nFinal answer:")
                print(response.content)
                return

            for tool_call in response.tool_calls:
                result = await mcp_client.call_tool(
                    tool_call["name"],
                    tool_call["args"],
                )

                print("\nTool:", tool_call["name"])
                print("Arguments:", tool_call["args"])
                print("Failed:", result.is_error)
                print("Content:", result.content)
                print("Structured result:", result.structured_content)

                if result.is_error:
                    payload = {
                        "status": "error",
                        "message": (
                            "Tool execution failed. "
                            "This does not mean no data exists."
                        ),
                        "details": [
                            block.text
                            for block in result.content
                            if block.type == "text"
                        ],
                    }
                elif result.structured_content is not None:
                    payload = result.structured_content
                else:
                    payload = {
                        "content": [
                            block.text
                            for block in result.content
                            if block.type == "text"
                        ]
                    }

                messages.append(
                    ToolMessage(
                        content=json.dumps(payload, default=str),
                        tool_call_id=tool_call["id"],
                        status=(
                            "error" if result.is_error else "success"
                        ),
                    )
                )

        raise RuntimeError(
            "Agent reached the limit of 8 model calls "
            "without producing a final answer."
        )


if __name__ == "__main__":
    anyio.run(main)