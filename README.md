# RCA-MCP Connector

<!-- mcp-name: io.github.dave1362/rca-mcp-connector -->

![Python](https://img.shields.io/badge/python-3.12+-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![PulseMCP](https://img.shields.io/badge/PulseMCP-listed-orange)

> **⚠️ Early access.** RCA-MCP's backend is live and this connector has been
> verified end-to-end against it. The `api.rca-mcp.com` custom domain isn't
> wired up yet — point `RCA_MCP_API_URL` at the current backend URL below.
> Tool schemas and documentation may still change before the first stable
> public launch.

## What is RCA-MCP?

The only MCP server purpose-built for causal Root Cause Analysis. 56 tools covering
causal graph construction, 10 RCA model families plus 3 dedicated PyRCA algorithms
(Salesforce PyRCA, BSD-3-Clause), multi-model consensus, and PDF/HTML/Excel/Markdown
report generation. Works with Claude, Ollama, Groq, OpenAI, Gemini, LangChain,
Cursor — 10 providers.

---

## Quick Start (2 minutes)

`rca-mcp-connector` is a published PyPI package — no clone needed. Point any MCP
client at it with `uvx` (or `pip install rca-mcp-connector` if you'd rather manage
the install yourself):

```bash
uvx rca-mcp-connector
```

Get a free API key at [rca-mcp.pages.dev](https://rca-mcp.pages.dev) — no credit
card required — then set `RCA_MCP_API_KEY` in your MCP client's config (examples
below).

---

## Claude Code Setup

Add to `.mcp.json` in your workspace root:

```json
{
  "mcpServers": {
    "rca-mcp": {
      "command": "uvx",
      "args": ["rca-mcp-connector"],
      "env": {
        "RCA_MCP_API_URL": "https://rcamcp-production.up.railway.app",
        "RCA_MCP_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Ollama Setup

```bash
go install github.com/mark3labs/mcphost@latest
mcphost -m ollama:qwen3:14b --config providers/mcp-servers.json
```

## OpenAI Agents SDK

```python
from agents import Agent, MCPServerStdio
import asyncio

async def main():
    async with MCPServerStdio(
        params={
            "command": "uvx",
            "args": ["rca-mcp-connector"],
            "env": {
                "RCA_MCP_API_URL": "https://rcamcp-production.up.railway.app",
                "RCA_MCP_API_KEY": "your_api_key_here",
            },
        }
    ) as rca_server:
        agent = Agent(name="RCA Agent", model="gpt-4o", mcp_servers=[rca_server])
        result = await agent.run("Find the root cause of the API latency spike.")
        print(result.final_output)

asyncio.run(main())
```

## LangChain

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
import asyncio

async def main():
    async with MultiServerMCPClient({
        "rca-mcp": {
            "command": "uvx", "args": ["rca-mcp-connector"],
            "env": {
                "RCA_MCP_API_URL": "https://rcamcp-production.up.railway.app",
                "RCA_MCP_API_KEY": "your_api_key_here",
            },
            "transport": "stdio",
        }
    }) as client:
        tools = await client.get_tools()
        agent = create_react_agent(ChatAnthropic(model="claude-sonnet-4-6"), tools)
        result = await agent.ainvoke({"messages": [{"role": "user", "content": "Run an FMEA analysis"}]})
        print(result["messages"][-1].content)

asyncio.run(main())
```

See `providers/` for ready-to-use config templates and full examples (Groq, Gemini,
OpenRouter, Claude Desktop).

---

## Third-Party Licences

**PyRCA (Salesforce):** BSD-3-Clause
Copyright (c) 2022, salesforce.com, inc.
https://github.com/salesforce/PyRCA

Algorithms in `rca_pyrca_*` tools are independently-written adaptations of PyRCA's
published methods (Zheng et al. 2023, arXiv:2306.11417), not direct copies of PyRCA
source code, per the private API's `models/pyrca_adapter.py`.

---

## Citing RCA-MCP

```bibtex
@software{rcamcp2026,
  title  = {RCA-MCP: An MCP Server for Causal Root Cause Analysis},
  author = {davetj},
  year   = {2026},
  url    = {https://github.com/dave1362/rca-mcp-connector},
  note   = {v4.1.12}
}
```
