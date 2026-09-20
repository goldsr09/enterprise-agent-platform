

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json
from langchain_core.messages import HumanMessage, ToolMessage
from pydantic.v1.utils import truncate
from app.tools.sql_tool import get_metrics_tool
from langgraph.graph import MessagesState, StateGraph, START, END
from app.tools.rag_tool import search_runbook_semantically

class AgentState(MessagesState):
    insufficient_data: bool
    tool_error: bool


load_dotenv()

model = ChatOpenAI(
    model="gpt-5.6-luna",
    reasoning_effort="none"

)


tools = [
    
    get_metrics_tool,
    search_runbook_semantically,

]

tools_by_name= { tool.name: tool for tool in tools}



model_with_tools = model.bind_tools(tools)

def call_model(state: AgentState):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def execute_tools(state: AgentState):
    last_message = state["messages"][-1]
    tool_messages = []
    insufficient_data = state.get("insufficient_data", False)
    tool_error = state.get("tool_error", False)



    for tool_call in last_message.tool_calls:
        try:
            tool = tools_by_name[tool_call["name"]]
            result = tool.invoke(tool_call["args"])
            print(result)
        


            if tool_call["name"] == "get_metrics_tool" and not result:
                insufficient_data = True
        
            content = json.dumps(result, default=str)
        
            message_status = "success"

        except Exception as error:
            print(f"{tool_call['name']} failed: {error}")

            tool_error = True
            content = (
                f"{tool_call['name']} failed with "
                f"{type(error).__name__}."
            )
            message_status = "error"

        
        tool_message = ToolMessage(
                    content=content,
                    tool_call_id=tool_call["id"],
                    status=message_status
        )
        tool_messages.append(tool_message)

    return {
        "messages": tool_messages,
        "insufficient_data": insufficient_data,
        "tool_error": tool_error
        }

def route_after_model(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"

    return END


builder = StateGraph[
    AgentState,
    None,
    AgentState,
    AgentState
](AgentState)
builder.add_node("model", call_model)
builder.add_node("tools", execute_tools)


builder.add_edge(START, "model")

builder.add_conditional_edges(
    "model",
    route_after_model,
    ["tools", END]
)

builder.add_edge("tools", "model")

agent_graph = builder.compile()


def investigate(question: str):
    result = agent_graph.invoke({
        "messages": [HumanMessage(content=question)],
        "insufficient_data": False,
        "tool_error": False
    },
    
        config={
             "run_name": "investigate",
             "tags": [
                 "api",
                 "enterprise-agent"],
            "metadata": {
                "question_length": len(question)

        }
    })
    
    if result["tool_error"]:
        status = "error"
    elif result["insufficient_data"]:
        status = "insufficient_data"
    else:
        status = "completed"

    return {
        "answer": result["messages"][-1].content,
        "status": status
    }
