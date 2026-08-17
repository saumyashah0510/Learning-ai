from langchain_mcp_adapters.client import MultiServerMCPClient

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

import asyncio

load_dotenv()

model = ChatGoogleGenerativeAI(
    model = "gemini-3.1-flash-lite",
    google_api_key = os.getenv("GOOGLE_API_KEY")
)

async def main():
    client = MultiServerMCPClient(
        {
            "math" : {
                "command" : "python",
                "args" : ["mathserver.py"],
                "transport" : "stdio"
            },

            "weather" : {
                "url" : "http://localhost:8000/mcp",
                "transport" : "streamable_http"
            }
        }
    )


    tools = await client.get_tools()

    agent = create_agent(
        model = model,
        tools = tools
    )

    math_response = await agent.ainvoke(
        {"messages" : [{
                "role" : "user",
                "content" : "What is (3 + 5) x 12"
            }]
        }
    )

    weather_response = await agent.ainvoke(
        {
            "messages" : [
                {
                    "role" : "user",
                    "content" : "What is the weather in Gujarat?"
                }
            ]
        }
    )

    print("Math response : ",math_response["messages"][-1].text)
    print("\nWeather response : ",weather_response["messages"][-1].text)

asyncio.run(main())