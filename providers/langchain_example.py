# langchain_rca_client.py
#
# Requires: pip install langchain-mcp-adapters langchain-anthropic
#
# Connects RCA-MCP as a LangGraph ReAct agent's toolset via
# langchain-mcp-adapters, which converts MCP tool schemas into
# LangChain Tool objects. Works with any LangChain-compatible LLM.

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
import asyncio


async def main():
    async with MultiServerMCPClient({
        "rca-mcp": {
            "command": "uvx",
            "args": ["rca-mcp-connector"],
            "env": {
                "RCA_MCP_API_URL": "https://rcamcp-production.up.railway.app",
                "RCA_MCP_API_KEY": "your_api_key_here",
            },
            "transport": "stdio",
        }
    }) as client:
        tools = await client.get_tools()
        model = ChatAnthropic(model="claude-sonnet-4-6")
        agent = create_react_agent(model, tools)
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content":
                "Run an FMEA analysis on: DB timeout severity=9, Auth failure severity=5"}]
        })
        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
