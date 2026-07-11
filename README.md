# RCA-MCP Connector

![Python](https://img.shields.io/badge/python-3.12+-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![PulseMCP](https://img.shields.io/badge/PulseMCP-listed-orange)

## What is RCA-MCP?

The only MCP server purpose-built for causal Root Cause Analysis. 55 tools covering
causal graph construction, 13 RCA model families (including Salesforce PyRCA
algorithms), multi-model consensus, and PDF/HTML/Excel/Markdown report generation.
Works with Claude, Ollama, Groq, OpenAI, Gemini, LangChain — 9 providers.

---

## Quick Start (2 minutes)

```bash
git clone https://github.com/dave1362/rca-mcp-connector.git
cd rca-mcp-connector
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set RCA_MCP_API_KEY to your key from https://rca-mcp.com/upgrade
```

Get an API key at [rca-mcp.com](https://rca-mcp.com) — a free tier is available,
no credit card required.

---

## Claude Code Setup

Add to `.mcp.json` in your workspace root:

```json
{
  "mcpServers": {
    "rca-mcp": {
      "command": "python",
      "args": ["/absolute/path/to/rca-mcp-connector/connector/server.py"],
      "env": {
        "RCA_MCP_API_URL": "https://api.rca-mcp.com",
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
            "command": "python",
            "args": ["connector/server.py"],
            "env": {"RCA_MCP_API_KEY": "your_key"},
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
            "command": "python", "args": ["connector/server.py"],
            "env": {"RCA_MCP_API_KEY": "your_key"}, "transport": "stdio",
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

## Tier Comparison

| Feature | Free | Starter ($19) | Pro ($79) | Enterprise ($399) |
|---|---|---|---|---|
| Rate limit/min | 20 | 60 | 120 | 300 |
| Max models | 5 | 20 | Unlimited | Unlimited |
| Max results stored | 100 | 10,000 | Unlimited | Unlimited |
| Batch analysis | ❌ | 5 incidents | 20 incidents | 20 incidents |
| Report: Markdown | ✅ | ✅ | ✅ | ✅ |
| Report: HTML + PDF | ❌ | ✅ | ✅ | ✅ |
| Report: Excel | ❌ | ❌ | ✅ | ✅ |
| PyRCA algorithms | ❌ | ✅ | ✅ | ✅ |
| Causal discovery | ❌ | ❌ | ✅ | ✅ |
| Graph versioning | ❌ | ✅ | ✅ | ✅ |
| Model ensembling | ❌ | ❌ | ✅ | ✅ |
| Async task runner | ❌ | ❌ | ✅ | ✅ |
| Multiple API keys | ❌ | ❌ | Up to 5 | Unlimited |
| Audit log export | ❌ | ❌ | ✅ | ✅ |
| Custom report branding | ❌ | ❌ | ❌ | ✅ |
| Admin role (purge) | ❌ | ❌ | ❌ | ✅ |
| SLA (99.9% uptime) | ❌ | ❌ | ❌ | ✅ |
| Dedicated instance | ❌ | ❌ | ❌ | ✅ |
| Token expiry | 24 h | 7 days | 30 days | 1 year |
| Guide ingestion | ❌ | 10 guides | 100 guides | Unlimited |
| Guide search results | 3 | 20 | 20 | 20 |
| Interactive diagnostics (dtree) | ❌ | ✅ | ✅ | ✅ |
| Diagnostic reports | ❌ | Markdown | PDF/HTML/MD | PDF/HTML/MD |
| FMEA-to-tree generation | ❌ | ✅ | ✅ | ✅ |
| PDF guide ingestion | ❌ | ✅ (counts toward guide limit) | ✅ | ✅ |
| PDF OCR (scanned docs) | ❌ | ✅ | ✅ | ✅ |

---

## All 55 Tools

Legend: ✅ All plans · 🌟 Starter+ · 💎 Pro+ · 👑 Enterprise only

### Group A — Causal Graph

| Tool | Plan | Description |
|---|---|---|
| `rca_graph_create` | ✅ | Create an empty causal DAG |
| `rca_graph_get` | ✅ | Retrieve a graph as JSON / DOT / adjacency |
| `rca_graph_score` | ✅ | Structural quality scoring |
| `rca_graph_discover` | 💎 | Auto-discover causal structure from data (PC-algorithm) |
| `rca_graph_merge` | 💎 | Merge two graphs for cross-system RCA |
| `rca_graph_list_versions` | 🌟 | List historical graph snapshots |
| `rca_graph_restore_version` | 👑 | Roll back to a historical version (admin) |
| `rca_graph_delete` | 👑 | Delete a graph permanently (admin) |

### Group B — RCA Models

| Tool | Plan | Description |
|---|---|---|
| `rca_model_create` | ✅ | Register a model spec (up to plan's model limit) |
| `rca_model_list` | ✅ | List registered models |
| `rca_model_update_status` | ✅ | Advance model lifecycle |
| `rca_model_validate` | ✅ | Validate on hold-out data |
| `rca_model_delete` | 👑 | Delete a model (admin) |

### Group C — Analysis

| Tool | Plan | Description |
|---|---|---|
| `rca_analysis_run` | ✅ | Run RCA, get ranked root causes |
| `rca_analysis_run_async` | 💎 | Submit a long-running analysis (returns task_id) |
| `rca_analysis_poll_task` | 💎 | Poll an async task's status |
| `rca_analysis_ensemble` | 💎 | Combine 2-5 models via weighted-vote consensus |
| `rca_analysis_get_result` | ✅ | Retrieve a stored result |
| `rca_analysis_list_results` | ✅ | Paginated result listing |
| `rca_analysis_query_results` | ✅ | Filter results by family/confidence/tags |
| `rca_analysis_compare` | ✅ | Cross-model consensus comparison |
| `rca_analysis_explain` | ✅ | Narrative explanation of a result |
| `rca_analysis_batch` | 🌟 | Batch analysis (5 incidents Starter, 20 Pro+) |

### Group D — Graph Operations

| Tool | Plan | Description |
|---|---|---|
| `rca_graph_add_node` | ✅ | Add a typed node |
| `rca_graph_remove_node` | ✅ | Remove a node |
| `rca_graph_add_edge` | ✅ | Add a directed causal edge (cycle-safe) |
| `rca_graph_remove_edge` | ✅ | Remove an edge |
| `rca_graph_score_paths` | ✅ | Rank causal paths to a target node |
| `rca_graph_markov_blanket` | ✅ | Get parents/children/co-parents of a node |

### Group E — Admin & Auth

| Tool | Plan | Description |
|---|---|---|
| `rca_auth_generate_token` | ✅ | Generate API key + JWT — call this first |
| `rca_auth_revoke_token` | 👑 | Invalidate a JWT before expiry (admin) |
| `rca_auth_list_keys` | 👑 | List API keys (admin + Pro+ multi-key feature) |
| `rca_auth_rotate_key` | 👑 | Rotate an API key (admin + Pro+ multi-key feature) |
| `rca_admin_health` | ✅ | Server health snapshot |
| `rca_admin_read_audit_log` | ✅ | Read structured audit entries |
| `rca_admin_purge_namespace` | 👑 | Delete all records in a namespace (admin) |
| `rca_admin_show_plan_info` | ✅ | Show current plan, limits, and upgrade options |

### Group F — Reports & Providers

| Tool | Plan | Description |
|---|---|---|
| `rca_report_generate` | ✅/🌟/💎 | Markdown all plans; HTML/PDF Starter+; Excel Pro+ |
| `rca_report_compare` | ✅/🌟 | Comparative report; Markdown all, HTML Starter+ |
| `rca_provider_list_configs` | ✅ | Setup instructions for any of the 9 providers |

### Group G — PyRCA Algorithms [PyRCA — BSD-3-Clause]

| Tool | Plan | Description |
|---|---|---|
| `rca_pyrca_epsilon_diagnosis` | 🌟 | z-score anomalous metric identification |
| `rca_pyrca_random_walk` | 🌟 | Personalised PageRank root cause localisation |
| `rca_pyrca_ht_diagnosis` | 🌟 | Hypothesis testing with descendant adjustment |
| `rca_pyrca_validate_setup` | ✅ | Check PyRCA strategy and licence compliance |

### Group H — Equipment Knowledge (Phase 9)

| Tool | Plan | Description |
|---|---|---|
| `rca_guide_ingest` | 🌟 | Ingest a troubleshooting guide (markdown/plain/json_dtree) |
| `rca_guide_search` | ✅ | Search guides by symptom (TF-IDF); Free capped at 3 results |
| `rca_guide_get` | ✅ | Retrieve a full guide or a specific section |
| `rca_guide_list` | ✅ | List ingested guides with equipment_type/tag filters |
| `rca_dtree_start` | 🌟 | Begin an interactive diagnostic decision-tree session |
| `rca_dtree_answer` | 🌟 | Answer a diagnostic question; returns next question or diagnosis |
| `rca_dtree_list_sessions` | 🌟 | List diagnostic sessions with equipment/status filters |
| `rca_guide_generate_report` | 🌟/💎 | Maintenance report from a resolved session; Markdown Starter+, PDF/HTML Pro+ |
| `rca_dtree_generate_from_fmea` | 🌟 | Auto-generate a decision tree from FMEA results |
| `rca_guide_pdf_preview` | 🌟 | Preview PDF quality before ingestion |
| `rca_guide_ingest_pdf` | 🌟 | Parse a PDF equipment manual → knowledge base |

Ships with 4 built-in sample guides (pump, vacuum interface valve, ML pipeline,
CFD solver) auto-loaded on first startup, and supports 26 equipment types.
PDF ingestion supports 4 parsing strategies (text_native, ocr, table, mixed).

---

## Get an API Key

[rca-mcp.com/upgrade](https://rca-mcp.com/upgrade) — Free tier available, plans from
**$19/month** (Starter), **$79/month** (Pro), **$399/month** (Enterprise).

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
  note   = {v3.0.0}
}
```
