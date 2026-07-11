# openai_rca_client.py
#
# Requires: pip install openai-agents
#
# Connects RCA-MCP to an OpenAI Agent via the openai-agents SDK's
# native MCP client support (openai-agents>=0.0.10).

from agents import Agent, MCPServerStdio
import asyncio


async def main():
    async with MCPServerStdio(
        params={
            "command": "python",
            "args": ["/path/to/rca_mcp/server.py"],
            "env": {
                "RCA_MCP_TRANSPORT": "stdio",
                "RCA_MCP_SECRET_KEY": "your_secret",
            },
        }
    ) as rca_server:
        agent = Agent(
            name="RCA Agent",
            model="gpt-4o",
            mcp_servers=[rca_server],
            instructions="You are an expert Root Cause Analysis agent. "
                         "Use the RCA-MCP tools to identify incident root causes.",
        )
        result = await agent.run(
            "Analyse this incident: API latency spiked to 2000ms at 14:00. "
            "Use granger causality to find which metric caused it."
        )
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
