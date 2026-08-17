from typing import Annotated
from typing_extensions import TypedDict
from IPython.display import display,Image

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langgraph.types import Command, interrupt
from langchain_core.messages import BaseMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.1-flash-lite",
    google_api_key = os.getenv("GOOGLE_API_KEY")
)


class State(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

def make_tool_graph():

    @tool
    def add(a: float, b: float) -> float:
        """Add two numbers"""
        return a + b

    tools = [add]

    llm_with_tools = llm.bind_tools(tools)

    def call_llm_model(state: State):
        return {
            "messages": [
                llm_with_tools.invoke(state["messages"])
            ]
        }

    builder = StateGraph(State)

    builder.add_node("tool_calling_llm", call_llm_model)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "tool_calling_llm")

    builder.add_conditional_edges(
        "tool_calling_llm",
        tools_condition
    )

    builder.add_edge("tools", "tool_calling_llm")

    graph = builder.compile()

    return graph

tool_agent = make_tool_graph()