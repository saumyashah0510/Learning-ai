from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(loc : str) -> str:
    """_summary_
    Gets the weather of a location
    """
    return "Its always sunny in Gujarat"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")