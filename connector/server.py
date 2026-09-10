"""
RCA-MCP Public Connector — FastMCP Server
============================================
Thin MCP server exposing all 55 RCA-MCP tool names and schemas.
Every tool is a pure forwarder to the private RCA-MCP API via
RCAMCPClient — no analytical logic, no security enforcement, no
storage. All of that lives in the private core and is enforced
server-side regardless of what a forked connector does.
"""

from __future__ import annotations

import os

from mcp.server.fastmcp import FastMCP

from .client import RCAMCPClient
from .models import (
    AuditInput,
    AuthSetupInput,
    BatchAnalysisInput,
    CompareResultsInput,
    DTreeAnswerInput,
    DTreeGenerateFromFmeaInput,
    DTreeListInput,
    DTreeStartInput,
    EdgeOpInput,
    EnsembleInput,
    EpsilonDiagnosisInput,
    ExplainInput,
    GetResultInput,
    GraphCreateInput,
    GraphDeleteInput,
    GraphDiscoverInput,
    GraphGetInput,
    GraphListVersionsInput,
    GraphMergeInput,
    GraphRestoreVersionInput,
    GraphScoreInput,
    GuideDeleteInput,
    GuideGetInput,
    GuideIngestInput,
    GuideListInput,
    GuidePDFIngestInput,
    GuidePDFPreviewInput,
    GuideReportInput,
    GuideSearchInput,
    HealthInput,
    HTDiagnosisInput,
    ListKeysInput,
    ListResultsInput,
    MarkovBlanketInput,
    ModelCreateInput,
    ModelDeleteInput,
    ModelListInput,
    ModelStatusInput,
    ModelValidateInput,
    NodeOpInput,
    PathScoreInput,
    PlanInfoInput,
    PollTaskInput,
    ProviderConfigInput,
    PurgeInput,
    PyRCASetupInput,
    QueryResultsInput,
    RandomWalkInput,
    RemoveEdgeInput,
    RemoveNodeInput,
    ReportCompareInput,
    ReportGenerateInput,
    RevokeTokenInput,
    RotateKeyInput,
    RunAnalysisAsyncInput,
    RunAnalysisInput,
)

mcp = FastMCP("rca-mcp")

_client = RCAMCPClient()   # reads RCA_MCP_API_URL / RCA_MCP_API_KEY from env


TOOL_ROUTES = {
    "rca_auth_generate_token": "auth/generate_token",
    "rca_auth_list_keys": "auth/list_keys",
    "rca_auth_rotate_key": "auth/rotate_key",
    "rca_auth_revoke_token": "auth/revoke_token",
    "rca_admin_health": "admin/health",
    "rca_admin_read_audit_log": "admin/read_audit_log",
    "rca_admin_purge_namespace": "admin/purge_namespace",
    "rca_graph_create": "graph/create",
    "rca_graph_get": "graph/get",
    "rca_graph_score": "graph/score",
    "rca_graph_discover": "graph/discover",
    "rca_graph_delete": "graph/delete",
    "rca_graph_list_versions": "graph/list_versions",
    "rca_graph_restore_version": "graph/restore_version",
    "rca_graph_merge": "graph/merge",
    "rca_graph_add_node": "graph/add_node",
    "rca_graph_remove_node": "graph/remove_node",
    "rca_graph_add_edge": "graph/add_edge",
    "rca_graph_remove_edge": "graph/remove_edge",
    "rca_graph_score_paths": "graph/score_paths",
    "rca_graph_markov_blanket": "graph/markov_blanket",
    "rca_model_create": "model/create",
    "rca_model_list": "model/list",
    "rca_model_update_status": "model/update_status",
    "rca_model_validate": "model/validate",
    "rca_model_delete": "model/delete",
    "rca_analysis_run": "analysis/run",
    "rca_analysis_get_result": "analysis/get_result",
    "rca_analysis_list_results": "analysis/list_results",
    "rca_analysis_query_results": "analysis/query_results",
    "rca_analysis_compare": "analysis/compare",
    "rca_analysis_explain": "analysis/explain",
    "rca_analysis_batch": "analysis/batch",
    "rca_analysis_ensemble": "analysis/ensemble",
    "rca_pyrca_epsilon_diagnosis": "pyrca/epsilon_diagnosis",
    "rca_pyrca_random_walk": "pyrca/random_walk",
    "rca_pyrca_ht_diagnosis": "pyrca/ht_diagnosis",
    "rca_report_generate": "report/generate",
    "rca_report_compare": "report/compare",
    "rca_provider_list_configs": "provider/list_configs",
    "rca_pyrca_validate_setup": "pyrca/validate_setup",
    "rca_analysis_run_async": "analysis/run_async",
    "rca_analysis_poll_task": "analysis/poll_task",
    "rca_admin_show_plan_info": "admin/show_plan_info",
    "rca_guide_ingest": "guide/ingest",
    "rca_guide_search": "guide/search",
    "rca_guide_get": "guide/get",
    "rca_guide_list": "guide/list",
    "rca_guide_delete": "guide/delete",
    "rca_dtree_start": "dtree/start",
    "rca_dtree_answer": "dtree/answer",
    "rca_dtree_list_sessions": "dtree/list_sessions",
    "rca_guide_generate_report": "guide/generate_report",
    "rca_dtree_generate_from_fmea": "dtree/generate_from_fmea",
    "rca_guide_pdf_preview": "guide/pdf_preview",
    "rca_guide_ingest_pdf": "guide/ingest_pdf",
}

@mcp.tool(
    name="rca_auth_generate_token",
    annotations={'title': 'Generate API Key', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_auth_generate_token(params: AuthSetupInput) -> str:
    """
    Generate a new API key for authenticating all other tools. Always
    issues the Free plan.

    Call this FIRST before using any other RCA-MCP tool.
    Store the returned api_key securely — it cannot be recovered later.
    Pass it as the 'token' field in every subsequent tool call. It does
    not expire.

    Paid plans (Starter/Pro/Enterprise) are NOT requested here — they are
    issued automatically, tied to your payment, the moment a Paystack
    subscription payment succeeds. Upgrade at https://rca-mcp.com/upgrade.

    Args:
        params (AuthSetupInput):
            - roles: audit-only metadata for this API key (not authorization)
            - key_id: accepted for backward compatibility, ignored
            - key_label: optional human-readable label for this key

    Returns:
        str: JSON with api_key, plan, roles, instruction
    """
    return await _client.call("auth/generate_token", params.model_dump())


@mcp.tool(
    name="rca_auth_list_keys",
    annotations={'title': 'List API Keys', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_auth_list_keys(params: ListKeysInput) -> str:
    """
    List your own API keys and their metadata. Never returns raw or
    hashed key material. Requires the multi-key feature (Pro plan or
    above -- up to 5 keys on Pro, unlimited on Enterprise); Free/Starter
    keys get a security_violation error, since those plans only ever
    have the one key they authenticated with.

    Use the returned key_id values with rca_auth_rotate_key or
    rca_auth_revoke_token to act on a specific key.

    Returns:
        str: JSON with total and a list of {key_id, label, plan_at_issue,
             created_at, last_used_at, is_active}
    """
    return await _client.call("auth/list_keys", params.model_dump())


@mcp.tool(
    name="rca_auth_rotate_key",
    annotations={'title': 'Rotate API Key', 'readOnlyHint': False, 'destructiveHint': True, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_auth_rotate_key(params: RotateKeyInput) -> str:
    """
    Deactivate one of your existing API keys and generate a replacement
    for the same account in one call. Requires the multi-key feature
    (Pro plan or above -- up to 5 keys on Pro, unlimited on Enterprise).

    Use rca_auth_list_keys first to find key_id if you don't already
    have it. Prefer this over rca_auth_revoke_token when you want a
    like-for-like replacement key in one step rather than just shutting
    the old one off.

    Args:
        params (RotateKeyInput):
            - key_id: UUID of the existing key to deactivate (from
              rca_auth_list_keys), not the raw key string itself

    Returns:
        str: JSON with old_key_id, new_key_id, api_key (new raw key --
             store it now, it cannot be recovered later)
    """
    return await _client.call("auth/rotate_key", params.model_dump())


@mcp.tool(
    name="rca_auth_revoke_token",
    annotations={'title': 'Revoke API Key', 'readOnlyHint': False, 'destructiveHint': True, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_auth_revoke_token(params: RevokeTokenInput) -> str:
    """
    Deactivate one of your own API keys immediately — useful when a key
    is compromised or an integration is being retired. Unlike
    rca_auth_list_keys/rca_auth_rotate_key, this has no plan gate at
    all — every plan can revoke, including Free/Starter with only one
    key (revoking your only key means you'll need rca_auth_generate_token
    again, or your dashboard, to get back in).

    If you don't already know key_id_to_revoke and you're Free/Starter
    (so rca_auth_list_keys is unavailable to you), check your account
    dashboard for the key's ID instead.

    Args:
        params (RevokeTokenInput):
            - token: your API key, to authenticate this call
            - key_id_to_revoke: UUID of the key to deactivate (may be
              the same key presented in 'token')

    Returns:
        str: JSON confirmation with the revoked key_id
    """
    return await _client.call("auth/revoke_token", params.model_dump())


@mcp.tool(
    name="rca_admin_health",
    annotations={'title': 'Server Health Check', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_admin_health(params: HealthInput) -> str:
    """
    Return server health status and instance-wide aggregate counts. Any
    authenticated key can call this (minimum viewer role) -- use this
    to confirm the server is reachable and to see which model families
    are supported, not to check your own account's usage.

    Note: models_in_registry/graphs_on_disk/results_on_disk are counts
    across ALL users on this server instance, not just yours -- for
    your own data, use rca_model_list, rca_graph_list_versions, or
    rca_analysis_list_results instead.

    Args:
        params (HealthInput): token, client_id

    Returns:
        str: JSON health snapshot (status, timestamp, instance-wide
             counts, supported model_families_supported list)
    """
    return await _client.call("admin/health", params.model_dump())


@mcp.tool(
    name="rca_admin_read_audit_log",
    annotations={'title': 'Read Audit Log', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_admin_read_audit_log(params: AuditInput) -> str:
    """
    Read YOUR OWN structured audit log entries for a given hour bucket —
    one entry per tool call you made, showing which tool ran, when, and
    whether it succeeded or was denied.

    Requires the audit_log_export feature (Pro plan or above --
    Free/Starter get a plan_required-style security_violation error;
    use rca_admin_show_plan_info to check your own plan first). Never
    returns another user's activity, regardless of plan.

    Use this to investigate why a call was denied or confirm a
    destructive action (e.g. rca_graph_delete) actually ran — it's an
    hourly snapshot, not a live stream, so it's not suited to
    real-time monitoring.

    Args:
        params (AuditInput):
            - hour_key: hour bucket as YYYYMMDD_HH, e.g. "20260803_14"
              (defaults to the current UTC hour if omitted)

    Returns:
        str: JSON {hour_key, entry_count, entries: [{tool, timestamp,
             outcome, ...}, ...]}
    """
    return await _client.call("admin/read_audit_log", params.model_dump())


@mcp.tool(
    name="rca_admin_purge_namespace",
    annotations={'title': 'Purge Storage Namespace', 'readOnlyHint': False, 'destructiveHint': True, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_admin_purge_namespace(params: PurgeInput) -> str:
    """
    Permanently delete ALL of YOUR OWN records in a storage namespace
    (graphs/models/results) in one call. Requires confirm=true. This
    action is IRREVERSIBLE. Only affects data you own -- there is no
    cross-account purge capability exposed via this or any other tool.

    Enterprise plan only (a deliberate tier feature, not a bug --
    Free/Starter/Pro get a security_violation error). On those plans,
    delete records one at a time instead: rca_graph_delete for graphs,
    rca_model_delete for models. There's currently no per-item delete
    tool for results.

    Args:
        params (PurgeInput):
            - namespace: one of "graphs", "models", "results" -- purges
              only that one namespace, not all three at once
            - confirm: must be true, or this returns an "aborted" error
              without deleting anything

    Returns:
        str: JSON {namespace, deleted_count}
    """
    return await _client.call("admin/purge_namespace", params.model_dump())


@mcp.tool(
    name="rca_graph_create",
    annotations={'title': 'Create Causal Graph', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_graph_create(params: GraphCreateInput) -> str:
    """
    Create a new, empty causal DAG. Populate it with rca_graph_add_node
    and rca_graph_add_edge afterward, or use rca_graph_discover instead
    if you have observational data and want the graph inferred rather
    than hand-built.

    Args:
        params (GraphCreateInput):
            - name: graph display name (for your own reference)
            - description: optional free-text notes on this graph's purpose

    Returns:
        str: JSON {graph_id, name, message}
    """
    return await _client.call("graph/create", params.model_dump())


@mcp.tool(
    name="rca_graph_get",
    annotations={'title': 'Get Causal Graph', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_graph_get(params: GraphGetInput) -> str:
    """
    Retrieve a causal graph's current state. Use "json" (default) to
    inspect it programmatically, "dot" to render it visually with
    Graphviz, or "adjacency" for a plain source->targets mapping.

    Args:
        params (GraphGetInput):
            - graph_id: the graph to retrieve
            - format: "json" (full node/edge detail, default), "dot"
              (Graphviz source), or "adjacency" (simple mapping)

    Returns:
        str: Graph data in the requested format, or a not_found error
             if the graph doesn't exist or belongs to another user
    """
    return await _client.call("graph/get", params.model_dump())


@mcp.tool(
    name="rca_graph_score",
    annotations={'title': 'Score Causal Graph Quality', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_graph_score(params: GraphScoreInput) -> str:
    """
    Compute structural quality scores for a causal graph -- a sanity
    check on the graph's shape itself (is it a valid DAG, how
    connected is it), not a root-cause analysis. Use this after
    building or editing a graph by hand, or after rca_graph_discover,
    to catch structural issues (e.g. disconnected components, a graph
    that isn't actually a DAG) before running rca_analysis_run on it.

    Args:
        params (GraphScoreInput): graph_id -- the graph to score

    Returns:
        str: JSON GraphScore {node_count, edge_count, dag_valid,
             density, avg_in_degree, avg_out_degree, max_path_length,
             connected_components, root_nodes, leaf_nodes,
             structural_score, coverage_score} -- both scores in [0,1]
    """
    return await _client.call("graph/score", params.model_dump())


@mcp.tool(
    name="rca_graph_discover",
    annotations={'title': 'Auto-Discover Causal Graph from Data', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_graph_discover(params: GraphDiscoverInput) -> str:
    """
    Automatically discover a causal skeleton from observational metric
    data using partial-correlation + Fisher-Z conditional independence
    tests (PC-algorithm). Requires the causal_discovery feature (Pro+).

    Creates and saves a new graph, same as rca_graph_create, but with
    edges inferred from data instead of asserted by hand -- use
    rca_graph_create + rca_graph_add_edge instead if you already know
    the causal structure and just want to encode it directly. Always
    review the discovered edges (rca_graph_get or rca_graph_score)
    before trusting them for RCA -- statistical discovery finds
    correlational structure consistent with the data, not guaranteed
    ground truth.

    Args:
        params (GraphDiscoverInput):
            - name: name for the resulting graph
            - data: {variable: [float values]} — min 30 rows, max 50 variables
            - significance: p-value threshold (default 0.05)

    Returns:
        str: JSON with graph_id and discovered edge summary
    """
    return await _client.call("graph/discover", params.model_dump())


@mcp.tool(
    name="rca_graph_delete",
    annotations={'title': 'Delete Causal Graph', 'readOnlyHint': False, 'destructiveHint': True, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_graph_delete(params: GraphDeleteInput) -> str:
    """
    Delete a causal graph permanently. Requires confirm=true. This
    action is IRREVERSIBLE via this tool -- if graph versioning is
    available on your plan, restoring an old version first won't help
    since the whole graph record is gone, not just its edges.

    You only need this to remove a graph entirely; to fix a graph
    you're still using, edit its nodes/edges instead
    (rca_graph_add_node/remove_node/add_edge/remove_edge).

    Args:
        params (GraphDeleteInput):
            - graph_id: the graph to delete
            - confirm: must be true, or this returns an "aborted" error
              without deleting anything

    Returns:
        str: JSON {deleted: graph_id}, or a not_found error if the
             graph doesn't exist or belongs to another user
    """
    return await _client.call("graph/delete", params.model_dump())


@mcp.tool(
    name="rca_graph_list_versions",
    annotations={'title': 'List Causal Graph Versions', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_graph_list_versions(params: GraphListVersionsInput) -> str:
    """
    List all historical versions of a causal graph. A new version is
    snapshotted automatically every time the graph is saved (node/edge
    additions, removals, etc) -- there's no separate "save version"
    step. Requires the graph_versioning feature (Starter+).

    Use the returned version_id values with rca_graph_restore_version
    to roll back to an earlier state.

    Args:
        params (GraphListVersionsInput): graph_id -- the graph to list
            versions for

    Returns:
        str: JSON {graph_id, total, versions: [{version_id, created_at,
             node_count, edge_count}, ...]}, newest first
    """
    return await _client.call("graph/list_versions", params.model_dump())


@mcp.tool(
    name="rca_graph_restore_version",
    annotations={'title': 'Restore Causal Graph Version', 'readOnlyHint': False, 'destructiveHint': True, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_graph_restore_version(params: GraphRestoreVersionInput) -> str:
    """
    Restore a causal graph to a specific historical version. This creates
    a new current state from the version snapshot — the version history
    itself is preserved (the restore operation is snapshotted too, so
    restoring is itself undoable by restoring forward again). Requires
    confirm=true and the graph_versioning feature (Starter+).

    Use rca_graph_list_versions first to find a version_id.

    Args:
        params (GraphRestoreVersionInput):
            - graph_id: the graph to restore
            - version_id: from rca_graph_list_versions
            - confirm: must be true, or this returns an "aborted" error

    Returns:
        str: JSON with graph_id, restored_from version_id, node/edge counts
    """
    return await _client.call("graph/restore_version", params.model_dump())


@mcp.tool(
    name="rca_graph_merge",
    annotations={'title': 'Merge Causal Graphs', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_graph_merge(params: GraphMergeInput) -> str:
    """
    Merge two causal graphs into a unified graph for cross-system RCA
    (e.g. combining a network-layer graph with an application-layer graph).
    Duplicate edges keep the higher-weight version; edges that would
    introduce a cycle are dropped and counted, not silently ignored.
    Requires the causal_discovery feature (Pro+); both source graphs
    must belong to you.

    Args:
        params (GraphMergeInput):
            - graph_id_a, graph_id_b: the two graphs to merge (both
              must be yours)
            - merged_name: name for the new, third graph created by
              this call (graph_id_a/b are left untouched)
            - conflict_resolution: "union" (default -- keep all nodes
              from both graphs) or "intersection" (only nodes present
              in both)

    Returns:
        str: JSON {merged_graph_id, node_count, edge_count,
             cycles_removed}, or a not_found error if either graph
             doesn't exist or belongs to another user
    """
    return await _client.call("graph/merge", params.model_dump())


@mcp.tool(
    name="rca_graph_add_node",
    annotations={'title': 'Add Node to Causal Graph', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_graph_add_node(params: NodeOpInput) -> str:
    """
    Add a typed node to a causal graph. Node names must be unique
    within the graph -- adding a node with a name that already exists
    raises an error rather than overwriting it; remove the existing
    one first with rca_graph_remove_node if you want to replace it.

    Args:
        params (NodeOpInput):
            - graph_id: the graph to add to
            - name: unique node name within this graph
            - node_type: metric | incident | symptom | root_cause |
              intermediate (default "metric") -- classifies the node
              for reports and graph views, doesn't affect analysis
            - description, metadata: optional, for your own reference

    Returns:
        str: JSON {added_node, node_type, total_nodes}, or a value
             error if the name already exists in this graph
    """
    return await _client.call("graph/add_node", params.model_dump())


@mcp.tool(
    name="rca_graph_remove_node",
    annotations={'title': 'Remove Node from Causal Graph', 'readOnlyHint': False, 'destructiveHint': True, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_graph_remove_node(params: RemoveNodeInput) -> str:
    """
    Remove a node and all its incident edges from a causal graph.
    Destructive and irreversible via this tool — undo only by
    rebuilding the node/edges with rca_graph_add_node +
    rca_graph_add_edge, or restoring an earlier version with
    rca_graph_restore_version if versioning is available on your plan.

    Use this to correct a mistaken node, not to prune weak paths — for
    that, adjust edge weights instead, or use rca_graph_score_paths
    first to see which paths actually matter before deciding what to
    remove.

    Args:
        params (RemoveNodeInput):
            - graph_id: the graph to modify
            - name: exact node name (case-sensitive) — use
              rca_graph_get first if you're not sure of the exact name

    Returns:
        str: JSON {removed_node, total_nodes} (post-removal count), or
             a not_found/value error if the node doesn't exist
    """
    return await _client.call("graph/remove_node", params.model_dump())


@mcp.tool(
    name="rca_graph_add_edge",
    annotations={'title': 'Add Causal Edge', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_graph_add_edge(params: EdgeOpInput) -> str:
    """
    Add a directed causal edge (source → target) to a graph. Both
    nodes must already exist -- add them first with rca_graph_add_node.
    Automatically rejects edges that would create a cycle (DAG
    enforcement) rather than silently allowing an invalid graph.

    Args:
        params (EdgeOpInput):
            - graph_id: the graph to add to
            - source, target: existing node names (cause -> effect)
            - weight: causal strength, 0.0-1.0 (default 1.0)
            - confidence: how sure you are of this edge, 0.0-1.0
              (default 1.0) -- distinct from weight; a weak-but-certain
              edge and a strong-but-uncertain one score differently
            - method: free-text provenance label, e.g. "manual",
              "granger_causality", "domain_expert" -- display only

    Returns:
        str: JSON {added_edge, weight, confidence, total_edges}, or a
             value/not_found error if either node doesn't exist or the
             edge would create a cycle
    """
    return await _client.call("graph/add_edge", params.model_dump())


@mcp.tool(
    name="rca_graph_remove_edge",
    annotations={'title': 'Remove Causal Edge', 'readOnlyHint': False, 'destructiveHint': True, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_graph_remove_edge(params: RemoveEdgeInput) -> str:
    """
    Remove a directed edge (source → target) from a causal graph.
    Destructive and irreversible via this tool — undo by re-adding the
    edge with rca_graph_add_edge, or restoring an earlier version with
    rca_graph_restore_version.

    Use this when an edge was added in error or a causal hypothesis is
    disproven. Use rca_graph_remove_node instead if you want the node
    itself gone — that already removes all its edges, so you don't
    need to remove them individually first.

    Args:
        params (RemoveEdgeInput):
            - graph_id: the graph to modify
            - source, target: exact node names (case-sensitive); the
              edge must currently exist — check with rca_graph_get if
              unsure

    Returns:
        str: JSON {removed_edge: "source → target"}, or a
             not_found/value error if the edge or either node doesn't
             exist
    """
    return await _client.call("graph/remove_edge", params.model_dump())


@mcp.tool(
    name="rca_graph_score_paths",
    annotations={'title': 'Score Causal Paths to Target', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_graph_score_paths(params: PathScoreInput) -> str:
    """
    Find and rank all causal paths from every root (no-incoming-edge)
    node to a target incident node. Score = geometric-mean(edge
    weights) × avg_confidence / sqrt(hops) — shorter, higher-weight,
    higher-confidence paths rank above longer or weaker ones.

    Use this on a graph you've built by hand (rca_graph_create +
    rca_graph_add_edge) to see which manually-asserted causal chains
    are strongest. For a data-driven ranking instead of a hand-built
    graph, use rca_analysis_run with a model family like
    granger_causality or dowhy_causal_inference instead.

    Args:
        params (PathScoreInput):
            - graph_id: the graph to search
            - target_node: the incident/effect node to trace backward
              from (must exist in the graph; check with rca_graph_get)
            - top_k: how many top-ranked paths to return, 1-50
              (default 10)

    Returns:
        str: JSON {target_node, paths_found, top_paths: [ScoredPath,
             ...]} ranked by score descending; empty list if no path
             from any root node reaches the target
    """
    return await _client.call("graph/score_paths", params.model_dump())


@mcp.tool(
    name="rca_graph_markov_blanket",
    annotations={'title': 'Get Markov Blanket of a Node', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_graph_markov_blanket(params: MarkovBlanketInput) -> str:
    """
    Return the Markov blanket of a node: parents ∪ children ∪
    co-parents -- the minimal set of other nodes needed to fully
    explain this node's behavior, ignoring the rest of the graph.

    Use this to scope an investigation to just the metrics that
    actually matter for one incident node, instead of reasoning about
    the whole graph -- e.g. before running a targeted analysis, or to
    decide which upstream metrics are even worth pulling data for.

    Args:
        params (MarkovBlanketInput):
            - graph_id: the graph to search
            - node: the node to compute the blanket for (must exist in
              the graph; check with rca_graph_get)

    Returns:
        str: JSON {parents, children, co_parents, full_blanket}, or a
             not_found error if the node or graph doesn't exist
    """
    return await _client.call("graph/markov_blanket", params.model_dump())


@mcp.tool(
    name="rca_model_create",
    annotations={'title': 'Create RCA Model', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_model_create(params: ModelCreateInput) -> str:
    """
    Register a new RCA model spec in the registry, starting in "draft"
    status. This just stores the spec — it doesn't run anything.

    Plan limits on how many models you can hold: Free 5, Starter 20,
    Pro+ unlimited (call rca_admin_show_plan_info to check your own
    count/limit).

    Typical lifecycle: create (here) → rca_analysis_run to use it →
    rca_model_validate on hold-out data → rca_model_update_status to
    mark it "deployed" (or "deprecated"/"failed") → rca_model_delete
    when you're done with it entirely.

    Model families: bayesian_network | dowhy_causal_inference | granger_causality |
                    fault_tree_analysis | fishbone_ishikawa | fmea |
                    bayesian_structural_time_series | change_point_detection |
                    random_forest_importance | counterfactual_analysis

    Args:
        params (ModelCreateInput):
            - name: for your own reference only
            - family: which RCA algorithm this model will use
            - description, tags, version: optional, for your own organization
            - config: family-specific parameters (e.g. significance
              threshold), passed through to the model at run time

    Returns:
        str: JSON {model_id}, or a plan_required error if you're at
             your model-count limit
    """
    return await _client.call("model/create", params.model_dump())


@mcp.tool(
    name="rca_model_list",
    annotations={'title': 'List Registered RCA Models', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_model_list(params: ModelListInput) -> str:
    """
    List all of YOUR registered RCA models, with optional family/status
    filters. Use this to find a model_id for rca_analysis_run, or to
    check your usage against your plan's model-count limit (see
    rca_admin_show_plan_info for the limit itself).

    Args:
        params (ModelListInput):
            - family_filter: only this model family (omit for all)
            - status_filter: only this status (omit for all)

    Returns:
        str: JSON {total, models: [{model_id, name, family, status,
             version, tags, created_at}, ...]}
    """
    return await _client.call("model/list", params.model_dump())


@mcp.tool(
    name="rca_model_update_status",
    annotations={'title': 'Update Model Status', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_model_update_status(params: ModelStatusInput) -> str:
    """
    Set a model's lifecycle status directly to any of: draft, trained,
    validated, deployed, deprecated, failed. This is a direct field
    update, not a guarded state machine — there is no enforced order
    (e.g. nothing stops setting "deployed" on a model that was never
    validated); that discipline is on the caller, not the API.

    Use "deprecated" to retire a model without deleting it (its past
    results stay queryable via rca_analysis_get_result); use "failed"
    to flag one that shouldn't be used, e.g. after rca_model_validate
    reports poor hold-out performance. Use rca_model_delete instead if
    you want the model gone entirely, not just marked.

    Args:
        params (ModelStatusInput):
            - model_id: the model to update
            - new_status: one of draft | trained | validated |
              deployed | deprecated | failed

    Returns:
        str: JSON {model_id, status}, or a not_found error if the
             model doesn't exist or belongs to another user
    """
    return await _client.call("model/update_status", params.model_dump())


@mcp.tool(
    name="rca_model_validate",
    annotations={'title': 'Validate RCA Model on Hold-out Data', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_model_validate(params: ModelValidateInput) -> str:
    """
    Run a quick correlation-based sanity check of a model against
    hold-out data you supply (not automatically split from training
    data -- you provide a separate dataset). This is a lightweight
    coverage/confidence check, not full cross-validation or backtesting;
    use it to catch an obviously broken model, not to certify accuracy.

    Sets the model's status to "validated" on success -- you don't
    need to also call rca_model_update_status afterward, though you
    can still use that tool later to move it to "deployed",
    "deprecated", or "failed".

    Args:
        params (ModelValidateInput):
            - model_id: the model to validate (from rca_model_create)
            - validation_data: {variable: [values]}, same shape as an
              rca_analysis_run payload's "data" field
            - target: which variable in validation_data to validate against

    Returns:
        str: JSON validation metrics (coverage, mean_correlation,
             confidence), or a not_found/bad_input error
    """
    return await _client.call("model/validate", params.model_dump())


@mcp.tool(
    name="rca_model_delete",
    annotations={'title': 'Delete RCA Model', 'readOnlyHint': False, 'destructiveHint': True, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_model_delete(params: ModelDeleteInput) -> str:
    """
    Permanently delete a model from the registry and storage. Requires
    confirm=true. This action is IRREVERSIBLE -- any results already
    produced by this model (via rca_analysis_run etc.) are unaffected
    and stay retrievable via rca_analysis_get_result, but you can no
    longer run new analyses with this model_id.

    Use rca_model_update_status to mark a model "deprecated" instead
    if you just want to stop new usage while keeping it around for
    reference -- delete is for when you're certain you won't need the
    spec again.

    Args:
        params (ModelDeleteInput):
            - model_id: the model to delete
            - confirm: must be true, or this returns an "aborted" error
              without deleting anything

    Returns:
        str: JSON {deleted_model_id}, or a not_found error if the
             model doesn't exist or belongs to another user
    """
    return await _client.call("model/delete", params.model_dump())


@mcp.tool(
    name="rca_analysis_run",
    annotations={'title': 'Run RCA Analysis', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_analysis_run(params: RunAnalysisInput) -> str:
    """
    Execute an RCA analysis using a registered model and return ranked
    root causes. This is the primary, synchronous analysis entry point
    -- it blocks until the model finishes. For a model that might take
    a while, use rca_analysis_run_async + rca_analysis_poll_task instead
    (Pro+); for multiple incidents through the same model in one call,
    use rca_analysis_batch instead (Starter+).

    Args:
        params (RunAnalysisInput):
            - model_id: an existing model from rca_model_create
            - payload: family-specific dict -- shape depends on the
              model's family (see the payload field's own description
              for the exact keys each family expects)
            - save: persist the result for later retrieval via
              rca_analysis_get_result (default true; set false for a
              throwaway check you don't want cluttering your result list)
            - tags: optional labels for filtering later with
              rca_analysis_query_results
            - ai_summary: also generate a short NL executive summary
              (Starter+, quota-limited -- see field description)

    Returns:
        str: JSON RCAResult with root_causes, confidence_overall,
             explanation, raw model output, _saved_as (the result_id)
             if save=true, and ai_summary/ai_summary_error if
             ai_summary=true was requested
    """
    return await _client.call("analysis/run", params.model_dump())


@mcp.tool(
    name="rca_analysis_get_result",
    annotations={'title': 'Get Stored Analysis Result', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_analysis_get_result(params: GetResultInput) -> str:
    """
    Retrieve a previously saved RCA result by result_id.

    Use this after rca_analysis_run (or rca_analysis_run_async +
    rca_analysis_poll_task) to re-fetch a result you already have the
    ID for — e.g. to hand it to rca_report_generate or
    rca_analysis_compare later. If you don't have a result_id yet, use
    rca_analysis_list_results to find one first.

    Args:
        params (GetResultInput):
            - result_id: from a prior analysis call's response

    Returns:
        str: JSON of the full stored RCAResult, or a not_found error
             if the ID doesn't exist or belongs to another user
    """
    return await _client.call("analysis/get_result", params.model_dump())


@mcp.tool(
    name="rca_analysis_list_results",
    annotations={'title': 'List Stored Analysis Results', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_analysis_list_results(params: ListResultsInput) -> str:
    """
    List all of YOUR stored RCA result IDs, newest first, with
    pagination. Returns IDs and a count only — not the results
    themselves; follow up with rca_analysis_get_result for the full
    content of any one of them.

    Args:
        params (ListResultsInput): limit (1-100, default 20), offset
            (skip this many from the newest, for paging past `limit`)

    Returns:
        str: JSON {total, count, offset, result_ids: [...], has_more}
    """
    return await _client.call("analysis/list_results", params.model_dump())


@mcp.tool(
    name="rca_analysis_query_results",
    annotations={'title': 'Query RCA Results', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_analysis_query_results(params: QueryResultsInput) -> str:
    """
    Query stored RCA results by model family, confidence threshold, time
    range, or tags — without loading every full result record. Use this
    instead of rca_analysis_list_results whenever you need to filter
    (e.g. "only high-confidence Granger results from this week"); use
    rca_analysis_list_results for a plain unfiltered listing instead.
    Returns lightweight index entries, not full result bodies -- follow
    up with rca_analysis_get_result for the complete content of any one.

    Args:
        params (QueryResultsInput):
            - model_family: exact family name, e.g. "granger_causality"
              (omit for all families)
            - min_confidence: 0.0-1.0, only results at or above this
            - after_ts: ISO timestamp, only results executed at or after this
            - tags: only results matching any of these tags
            - limit, offset: pagination, 1-100 per page

    Returns:
        str: JSON {total, results: [index entries], has_more}
    """
    return await _client.call("analysis/query_results", params.model_dump())


@mcp.tool(
    name="rca_analysis_compare",
    annotations={'title': 'Compare RCA Results', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_analysis_compare(params: CompareResultsInput) -> str:
    """
    Compare multiple RCA results: surface overlapping root causes,
    confidence agreement, and model disagreements. Returns raw
    comparison JSON for programmatic use -- use rca_report_compare
    instead if you want the same comparison rendered as a shareable
    markdown/HTML document.

    Args:
        params (CompareResultsInput): result_ids -- 2-10 result_ids to
            compare (from rca_analysis_run or rca_analysis_list_results)

    Returns:
        str: JSON comparison with consensus_causes and
             model_disagreements, or a not_found error if any result_id
             doesn't exist or belongs to another user
    """
    return await _client.call("analysis/compare", params.model_dump())


@mcp.tool(
    name="rca_analysis_explain",
    annotations={'title': 'Explain RCA Result', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_analysis_explain(params: ExplainInput) -> str:
    """
    Turn a stored RCA result into a human-readable explanation with
    heuristic recommended actions (IMMEDIATE/MONITOR/TRACK, based on
    each cause's score) -- useful for a chat response or incident
    writeup, as opposed to rca_analysis_get_result's raw JSON.

    Args:
        params (ExplainInput):
            - result_id: from a prior analysis call
            - detail_level: "brief" (summary + top 3 causes +
              recommended actions), "standard" (default -- adds all
              root causes, contributing factors, warnings), or
              "verbose" (adds the raw model output, timestamp, duration)

    Returns:
        str: JSON narrative explanation, ranked causes, recommended
             actions (shape varies by detail_level -- see above), or a
             not_found error if result_id doesn't exist or belongs to
             another user
    """
    return await _client.call("analysis/explain", params.model_dump())


@mcp.tool(
    name="rca_analysis_batch",
    annotations={'title': 'Batch RCA Analysis', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_analysis_batch(params: BatchAnalysisInput) -> str:
    """
    Run the same RCA model over multiple incidents in one call, then
    rank which root causes recur most often across all of them — use
    this to spot a systemic cause behind several similar incidents,
    not just one.

    Requires Starter+ (Free plan cannot batch at all; Starter allows
    up to 5 incidents per call, Pro+ up to 20 — call
    rca_admin_show_plan_info to check your own limit). For a single
    incident, use rca_analysis_run instead — it's simpler and doesn't
    need the plan tier.

    Args:
        params (BatchAnalysisInput):
            - model_id: an existing model, applied identically to
              every incident
            - incidents: 1-20 payload dicts (capped by your plan),
              each matching the same shape rca_analysis_run expects
              for this model family

    Returns:
        str: JSON {per_incident: [{incident_index, result_id,
             top_cause, confidence}, ...], cross_incident_ranking}
    """
    return await _client.call("analysis/batch", params.model_dump())


@mcp.tool(
    name="rca_analysis_ensemble",
    annotations={'title': 'Ensemble RCA Analysis', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_analysis_ensemble(params: EnsembleInput) -> str:
    """
    Run 2-5 different RCA models on the SAME payload and combine their
    root-cause scores via weighted voting. Requires the ensemble
    feature (Pro+). Use this when you're unsure which single model
    family fits the data best and want cross-validation across
    families -- for the SAME model run over multiple different
    incidents instead, use rca_analysis_batch.

    Algorithm:
      1. Run each model_id via dispatch_rca()
      2. Collect all root_cause {node, score} pairs
      3. For each unique node: ensemble_score = sum(weight_i * score_i * confidence_i)
      4. Normalise to [0,1]
      5. Return ranked ensemble result

    Args:
        params (EnsembleInput):
            - model_ids: 2-5 existing models, all run against the same payload
            - payload: shared input, shape depends on the models' families
            - weights: optional per-model weights, same length as
              model_ids (default: equal weighting)
            - save: persist the ensembled result (default true)

    Returns:
        str: JSON with ensemble_root_causes (ranked), model_contributions,
             agreement_matrix (which models agree on which root causes),
             or a bad_input/not_found error
    """
    return await _client.call("analysis/ensemble", params.model_dump())


@mcp.tool(
    name="rca_pyrca_epsilon_diagnosis",
    annotations={'title': 'PyRCA ε-Diagnosis (Anomalous Metric Identification)', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_pyrca_epsilon_diagnosis(params: EpsilonDiagnosisInput) -> str:
    """
    [Adapted from Salesforce PyRCA — BSD-3-Clause]
    Identify anomalous metrics contributing to a Service Level Indicator (SLI)
    anomaly by comparing metric distributions in normal vs. incident windows.

    Uses z-score thresholding: metrics with |z| > epsilon in the incident
    window relative to the normal baseline are flagged as root cause candidates.

    Best used as a FIRST STEP in RCA to narrow down candidate metrics
    before applying more compute-intensive causal methods like
    rca_pyrca_ht_diagnosis or rca_pyrca_random_walk -- this one needs
    no causal graph at all, just two data windows. Requires the pyrca
    feature (Starter+).

    Args:
        params (EpsilonDiagnosisInput):
            - normal_data: baseline {metric: [values]} (min 3 per metric)
            - anomaly_data: incident window {metric: [values]}
            - sli_metric: the observed anomaly metric
            - epsilon: z-score threshold (default 3.0 = 3σ)

    Returns:
        str: JSON with root_causes (anomalous metrics ranked by |z_score|),
             all_metrics, sli_z_score, epsilon_threshold

    Attribution: Adapted from PyRCA EpsilonDiagnosis (Salesforce, BSD-3-Clause)
                 Zhen et al. (2022) ε-Diagnosis
    """
    return await _client.call("pyrca/epsilon_diagnosis", params.model_dump())


@mcp.tool(
    name="rca_pyrca_random_walk",
    annotations={'title': 'PyRCA Random Walk RCA', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_pyrca_random_walk(params: RandomWalkInput) -> str:
    """
    [Adapted from Salesforce PyRCA — BSD-3-Clause]
    Graph-based root cause localisation via personalised PageRank random walk.
    Propagates backward through a causal adjacency graph from the SLI node,
    weighting transitions by anomaly scores to compute root cause probabilities.
    Requires the pyrca feature (Starter+) and, unlike
    rca_pyrca_epsilon_diagnosis, needs an adjacency graph you already
    have (from rca_graph_get's "adjacency" format, or hand-built) plus
    precomputed anomaly scores per metric -- it doesn't compute those
    scores itself.

    Args:
        params (RandomWalkInput):
            - adjacency: {source: {target: weight}} causal graph
            - anomaly_scores: {metric: score} anomaly magnitudes
            - sli_metric: starting node
            - restart_prob: personalisation (higher = proximity-weighted)

    Returns:
        str: JSON with root_causes ranked by composite_score, converged, iterations

    Attribution: Adapted from PyRCA random walk concept (Salesforce, BSD-3-Clause)
    """
    return await _client.call("pyrca/random_walk", params.model_dump())


@mcp.tool(
    name="rca_pyrca_ht_diagnosis",
    annotations={'title': 'PyRCA HT-ADJ Hypothesis Testing Diagnosis', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_pyrca_ht_diagnosis(params: HTDiagnosisInput) -> str:
    """
    [Adapted from Salesforce PyRCA — BSD-3-Clause]
    Hypothesis-testing RCA with descendant adjustment (HT-ADJ / CIRCA).
    Tests whether the SLI anomaly can be statistically explained by causal
    propagation from each ancestor node. Applies descendant adjustment to
    reduce indirect cause scores and surface true root causes.

    This is the most statistically rigorous PyRCA algorithm and is
    recommended when you have a well-validated causal graph and
    sufficient pre-anomaly data -- reach for
    rca_pyrca_epsilon_diagnosis instead if you don't have a graph yet,
    or rca_pyrca_random_walk if you have a graph but not enough
    pre-anomaly history for a hypothesis test. Requires the pyrca
    feature (Starter+).

    Args:
        params (HTDiagnosisInput):
            - data: {metric: [values]} full time series
            - adjacency: causal graph
            - sli_metric: observed anomaly metric
            - anomaly_start_idx: index where anomaly starts
            - significance: p-value threshold (default 0.05)
            - use_descendant_adjustment: enable HT-ADJ (default True)

    Returns:
        str: JSON with root_causes (is_root_cause=true), all_results, method (HT or HT-ADJ)

    Attribution: Adapted from PyRCA HT/CIRCA concept (Salesforce, BSD-3-Clause)
                 Shen et al. (2022) CIRCA; Zheng et al. (2023) arXiv:2306.11417
    """
    return await _client.call("pyrca/ht_diagnosis", params.model_dump())


@mcp.tool(
    name="rca_report_generate",
    annotations={'title': 'Generate RCA Report', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_report_generate(params: ReportGenerateInput) -> str:
    """
    Generate a styled, professional report from a SINGLE RCA analysis
    result -- use rca_report_compare instead if you want a report
    covering multiple results together.

    Supported formats (plan-gated -- Free: markdown only, Starter+:
    adds html/pdf, Pro+: adds excel; requesting an ungated format
    returns a security_violation error, not a silent downgrade):
      pdf      — Professional PDF with tables, score bars, and styled sections
                 (requires reportlab; falls back to plaintext if not installed)
      html     — Styled HTML with CSS — embeddable in dashboards or emails
                 (requires jinja2; falls back to minimal HTML)
      excel    — 4-sheet Excel workbook: Summary, Root Causes, Actions, Metadata
                 (requires openpyxl)
      markdown — Plain Markdown; always available; good for GitHub/Slack/Notion

    All formats include:
      - Executive summary with metric cards
      - Root cause ranking table with priority badges
      - Recommended actions (IMMEDIATE / MONITOR / TRACK)
      - Analysis metadata
      - Optional raw output appendix

    Args:
        params (ReportGenerateInput):
            - result_id: source RCA result
            - format: pdf | html | excel | markdown
            - title: custom report title
            - include_raw: include model output appendix
            - save: persist report to storage

    Returns:
        str: JSON with content_b64 (bytes formats), content_text (text formats),
             byte_size, format, report_id (if saved), storage_path (if saved)
    """
    return await _client.call("report/generate", params.model_dump())


@mcp.tool(
    name="rca_report_compare",
    annotations={'title': 'Generate Comparative RCA Report', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_report_compare(params: ReportCompareInput) -> str:
    """
    Generate a comparative report across 2–10 RCA results, showing consensus
    root causes, model agreement percentages, and per-model summaries. Use
    this instead of rca_analysis_compare when you want a shareable
    formatted document rather than raw comparison JSON.

    `format: "html"` requires Starter+ (Free plan gets a plan_required
    error and should use the default "markdown" instead).

    Args:
        params (ReportCompareInput):
            - result_ids: 2–10 result IDs to compare (from
              rca_analysis_run or rca_analysis_list_results)
            - format: "markdown" (default, all plans) or "html" (Starter+)
            - title: report title, up to 200 chars
            - save: persist the report server-side for later retrieval
              (default true)

    Returns:
        str: Comparative report (text/html) with consensus_root_causes table
    """
    return await _client.call("report/compare", params.model_dump())


@mcp.tool(
    name="rca_provider_list_configs",
    annotations={'title': 'Get Provider Configuration', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_provider_list_configs(params: ProviderConfigInput) -> str:
    """
    Get MCP client configuration and setup instructions for a specific
    provider or list all supported providers. Use this when a user
    asks "how do I connect RCA-MCP to X" -- it's documentation lookup,
    not something that affects RCA-MCP's own behavior.

    Supported providers:
      claude_desktop     — Claude Desktop app (macOS/Windows)
      claude_code        — Claude Code VS Code extension
      cursor             — Cursor AI code editor
      ollama_mcphost     — Ollama local models via MCPHost bridge
      groq_mcphost       — Groq cloud via MCPHost bridge
      openai_agents      — OpenAI GPT via openai-agents SDK
      gemini_mcphost     — Google Gemini via MCPHost bridge
      langchain_langgraph — LangChain/LangGraph via mcp-adapters
      openrouter         — OpenRouter (200+ models) via MCPHost
      remote_http        — Any client via Railway/cloud HTTP deployment

    Args:
        params (ProviderConfigInput):
            - provider: specific provider key, or omit to list all

    Returns:
        str: JSON config dict with setup instructions, run commands, and notes
    """
    return await _client.call("provider/list_configs", params.model_dump())


@mcp.tool(
    name="rca_pyrca_validate_setup",
    annotations={'title': 'Validate PyRCA Setup', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_pyrca_validate_setup(params: PyRCASetupInput) -> str:
    """
    Validate the PyRCA integration setup and report which strategy is
    active — a read-only diagnostic, not an action. Takes no
    parameters beyond authentication (token/client_id); there is
    nothing else to configure on this call.

    Run this once before your first rca_pyrca_epsilon_diagnosis,
    rca_pyrca_ht_diagnosis, or rca_pyrca_random_walk call if you're
    unsure which strategy is active, or if a PyRCA call errors
    unexpectedly — the response's "recommendations" field will say
    what to fix.

    Checks:
      - Strategy B (pure Python): always available, no extra setup
      - Strategy A (subprocess): requires sfr-pyrca in .venv_pyrca
      - sklearn version in host env vs PyRCA's requirement
      - Attribution compliance (BSD-3-Clause notice present)

    Returns:
        str: JSON with strategy_active, sklearn_version, sfr_pyrca_available,
             compliance, recommendations
    """
    return await _client.call("pyrca/validate_setup", params.model_dump())


@mcp.tool(
    name="rca_analysis_run_async",
    annotations={'title': 'Run RCA Analysis Asynchronously', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_analysis_run_async(params: RunAnalysisAsyncInput) -> str:
    """
    Submit a long-running RCA analysis (bayesian_network,
    dowhy_causal_inference, or any model against a large dataset) as a
    background task instead of blocking. Requires the async_tasks
    feature (Pro+); for most models on typical data sizes, the
    synchronous rca_analysis_run is simpler and doesn't need this or
    the plan tier. Returns a task_id immediately -- use
    rca_analysis_poll_task repeatedly to check progress and retrieve
    the result once it completes.

    Args:
        params (RunAnalysisAsyncInput):
            - model_id: an existing model from rca_model_create
            - payload: same shape as rca_analysis_run expects for that
              model's family
            - save: persist the result once the task completes (default true)
            - tags: optional labels for filtering later with
              rca_analysis_query_results

    Returns:
        str: JSON {task_id} -- pass this to rca_analysis_poll_task
    """
    return await _client.call("analysis/run_async", params.model_dump())


@mcp.tool(
    name="rca_analysis_poll_task",
    annotations={'title': 'Poll Async Analysis Task', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_analysis_poll_task(params: PollTaskInput) -> str:
    """
    Poll the status of an async RCA task submitted via
    rca_analysis_run_async. Requires the async_tasks feature (Pro+ --
    same gate as submitting the task in the first place).

    Call this repeatedly (e.g. every few seconds) until status is
    "completed" or "failed" -- there's no push notification, only
    polling. status progresses pending → running → completed/failed;
    `result` is only populated once completed, `error` only once failed.

    Args:
        params (PollTaskInput):
            - task_id: from rca_analysis_run_async's response

    Returns:
        str: JSON {task_id, status, progress, result (if completed),
             error (if failed)}, or a not_found error if the task_id
             doesn't exist or belongs to another user
    """
    return await _client.call("analysis/poll_task", params.model_dump())


@mcp.tool(
    name="rca_admin_show_plan_info",
    annotations={"title": "Show Current Plan & Limits", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def rca_admin_show_plan_info(params: PlanInfoInput) -> str:
    """
    Show your current plan, every feature limit, and which locked
    features an upgrade would unlock. Takes no parameters beyond
    authentication -- there's nothing else to configure here.

    Call this proactively before something like rca_analysis_batch,
    rca_model_create, rca_report_compare, rca_guide_generate_report, or
    rca_dtree_start to check your limits up front, rather than
    discovering a plan_required error mid-workflow -- several of those
    tools' docstrings point back to this one for exactly that reason.

    Returns:
        str: JSON {plan, display_name, limits: {...}, features: {...},
             locked_features: [...], upgrade_url (null on Enterprise)}
    """
    return await _client.call("admin/show_plan_info", params.model_dump())


@mcp.tool(
    name="rca_guide_ingest",
    annotations={'title': 'Ingest Equipment Troubleshooting Guide', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_guide_ingest(params: GuideIngestInput) -> str:
    """
    🌟 Starter+ — Upload and index an equipment troubleshooting guide into the
    knowledge base, as plain text content. Use rca_guide_ingest_pdf
    instead if you're starting from an actual PDF file.

    Supports three formats:
      markdown   — Structured Markdown with ## headings (recommended);
                   fault codes (F-###, ERR-###) are auto-extracted
      plain      — Raw text; split into sections on double newlines
      json_dtree — JSON decision tree for interactive diagnostics via rca_dtree_start

    Guide is immediately searchable via rca_guide_search after ingestion.

    Plan limits: Starter up to 10 guides, Pro up to 100, Enterprise unlimited.

    Args:
        params (GuideIngestInput): equipment_id, equipment_type, name, content,
            format, tags, version

    Returns:
        str: JSON with guide_id, section_count, symptom_count, fault_code_count
    """
    return await _client.call("guide/ingest", params.model_dump())


@mcp.tool(
    name="rca_guide_search",
    annotations={'title': 'Search Troubleshooting Guides by Symptom', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_guide_search(params: GuideSearchInput) -> str:
    """
    ✅ All plans — Search the equipment knowledge base by symptom description
    using TF-IDF relevance ranking. Free plan capped at 3 results.
    Searches both your own ingested guides and the 4 built-in shared
    sample guides (visible to every account).

    Args:
        params (GuideSearchInput): symptom, equipment_type, tags, top_k (1-20)

    Returns:
        str: JSON list of matching guide sections with relevance_score,
             excerpt, fault_codes, and page_ref
    """
    return await _client.call("guide/search", params.model_dump())


@mcp.tool(
    name="rca_guide_get",
    annotations={'title': 'Retrieve Troubleshooting Guide', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_guide_get(params: GuideGetInput) -> str:
    """
    ✅ All plans — Retrieve a full troubleshooting guide, or one specific
    section by ID. Includes the 4 built-in shared sample guides
    (visible and readable by every account, though only
    rca_guide_ingest/rca_guide_ingest_pdf can add your own, and only
    your own can be deleted via rca_guide_delete).

    Args:
        params (GuideGetInput):
            - guide_id: from rca_guide_ingest, rca_guide_ingest_pdf, or
              rca_guide_search/rca_guide_list results
            - section_id: optional, to retrieve one section instead of
              the whole guide (section IDs come from rca_guide_search
              results or a prior full rca_guide_get call)

    Returns:
        str: JSON {guide_id, metadata, sections} (whole guide) or
             {guide_id, metadata, section} (single section), or a
             not_found error if the guide/section doesn't exist or
             isn't yours
    """
    return await _client.call("guide/get", params.model_dump())


@mcp.tool(
    name="rca_guide_list",
    annotations={'title': 'List Ingested Troubleshooting Guides', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_guide_list(params: GuideListInput) -> str:
    """
    ✅ All plans — List your ingested troubleshooting guides (plus the 4
    built-in shared samples visible to every account), with optional
    equipment_type/tag filters. Use the returned guide_id with
    rca_guide_get, rca_guide_delete, or rca_dtree_start.

    Args:
        params (GuideListInput):
            - equipment_type: only guides for this type (omit for all)
            - tags: only guides matching any of these tags (omit for all)

    Returns:
        str: JSON {total, guides: [{guide_id, equipment_id,
             equipment_type, name, version, tags, section_count,
             created_at}, ...]}
    """
    return await _client.call("guide/list", params.model_dump())


@mcp.tool(
    name="rca_guide_delete",
    annotations={'title': 'Delete Equipment Guide', 'readOnlyHint': False, 'destructiveHint': True, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_guide_delete(params: GuideDeleteInput) -> str:
    """
    Permanently delete an equipment guide you ingested. Requires
    confirm=true. This action is IRREVERSIBLE -- re-ingest via
    rca_guide_ingest or rca_guide_ingest_pdf if you need it back.

    Scoped to your own guides only -- the 4 built-in sample guides
    (shared, visible to every account) can never be deleted this way,
    since delete_guide() requires an exact ownership match; deleting a
    guide already referenced by an active decision-tree session doesn't
    affect that session's in-progress state.

    Args:
        params (GuideDeleteInput):
            - guide_id: the guide to delete (from rca_guide_list or
              rca_guide_search)
            - confirm: must be true, or this returns an "aborted" error

    Returns:
        str: JSON confirmation with the deleted guide_id, or a
             not_found error if it doesn't exist or belongs to another
             user (including the 4 shared built-in samples)
    """
    return await _client.call("guide/delete", params.model_dump())


@mcp.tool(
    name="rca_dtree_start",
    annotations={'title': 'Start Equipment Diagnostic Session', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_dtree_start(params: DTreeStartInput) -> str:
    """
    🌟 Starter+ — Begin an interactive diagnostic session using a decision
    tree guide. Returns a question — answer with rca_dtree_answer, one
    call per question, until the session resolves to a diagnosis.

    Two modes:
      1. guide_id = <uuid>  → Use a specific json_dtree guide
      2. guide_id = "auto"  → Auto-generate tree from FMEA results
         (requires fmea_result_id pointing to a completed FMEA analysis)

    session_id resume behavior (non-obvious): if you pass a session_id
    that's yours and not yet resolved, this returns its CURRENT
    question — guide_id/equipment_id/symptom are ignored entirely in
    that case. If the session_id is missing, already resolved, or
    belongs to someone else, it's silently treated as if you'd omitted
    it: a brand-new session starts fresh under that same session_id
    (or a fresh UUID if you didn't supply one) — you won't get an
    error, so a typo'd ID quietly starts over rather than resuming.

    Args:
        params (DTreeStartInput):
            - guide_id: guide UUID or "auto"
            - equipment_id: equipment being diagnosed
            - symptom: initial fault description
            - session_id: optional; see resume behavior above
            - fmea_result_id: required when guide_id="auto"

    Returns:
        str: JSON with session_id, question, options (yes/no/unknown), progress_pct
    """
    return await _client.call("dtree/start", params.model_dump())


@mcp.tool(
    name="rca_dtree_answer",
    annotations={'title': 'Answer Diagnostic Question', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_dtree_answer(params: DTreeAnswerInput) -> str:
    """
    🌟 Starter+ — Answer the current diagnostic question to advance the
    decision tree. Call repeatedly until status == "resolved".

    Once resolved, use rca_guide_generate_report to turn the session
    into a shareable report.

    Args:
        params (DTreeAnswerInput): session_id, answer (yes|no|unknown), measurement
            - ai_summary: also generate a short NL executive summary if
              this answer resolves the session (Starter+, quota-limited --
              see field description)

    Returns:
        str: JSON with status, question OR diagnosis, progress_pct, and
             ai_summary/ai_summary_error if ai_summary=true was requested
             and the session resolved.
             Diagnosis fields (when resolved): diagnosis, confidence, actions,
             parts_to_check, estimated_repair_time, escalate_to_specialist,
             fault_codes, references, diagnostic_path
    """
    return await _client.call("dtree/answer", params.model_dump())


@mcp.tool(
    name="rca_dtree_list_sessions",
    annotations={'title': 'List Diagnostic Sessions', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_dtree_list_sessions(params: DTreeListInput) -> str:
    """
    🌟 Starter+ — List your equipment diagnostic sessions (started via
    rca_dtree_start), each with its status and diagnosis if resolved.
    Free-plan keys get a plan_required error instead of results.

    Use this to find a session_id for rca_guide_generate_report, check
    whether a session is already resolved before continuing it with
    rca_dtree_answer, or review diagnostic history for one piece of
    equipment.

    Args:
        params (DTreeListInput): equipment_id (optional filter),
            resolved_only (default false — includes in-progress
            sessions too)

    Returns:
        str: JSON {total, sessions: [{session_id, equipment_id,
             status, diagnosis, ...}, ...]}
    """
    return await _client.call("dtree/list_sessions", params.model_dump())


@mcp.tool(
    name="rca_guide_generate_report",
    annotations={'title': 'Generate Equipment Diagnostic Report', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_guide_generate_report(params: GuideReportInput) -> str:
    """
    🌟 Starter+ (markdown) / 💎 Pro+ (PDF/HTML) — Generate a maintenance/
    troubleshooting report from a completed diagnostic session. The
    session must already be resolved (finished via rca_dtree_answer)
    — an in-progress session returns an error telling you to keep
    answering questions first.

    Report includes equipment/symptom summary, full diagnostic path,
    root cause with confidence score, recommended actions and parts list,
    measurements recorded, guide section references, and escalation flag.

    Args:
        params (GuideReportInput):
            - session_id: must be a session already marked "resolved"
              (check via rca_dtree_list_sessions)
            - format: "markdown" (default, Starter+), "pdf" or "html"
              (Pro+ only — Starter requesting these gets plan_required,
              not a silent downgrade)
            - include_guide_refs, custom_title
    """
    return await _client.call("guide/generate_report", params.model_dump())


@mcp.tool(
    name="rca_dtree_generate_from_fmea",
    annotations={'title': 'Generate Decision Tree from FMEA Results', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_dtree_generate_from_fmea(params: DTreeGenerateFromFmeaInput) -> str:
    """
    🌟 Starter+ — Auto-generate a diagnostic decision tree from a completed
    FMEA analysis, converting HIGH-priority failure modes into a sequential
    yes/no diagnostic tree. Get fmea_result_id first by running
    rca_analysis_run against a model created with family="fmea".

    When save_as_guide=True (default), the tree is ingested as a
    json_dtree guide and the returned guide_id can be passed to
    rca_dtree_start -- or skip this tool entirely and pass
    guide_id="auto" directly to rca_dtree_start, which generates the
    tree on the fly without saving it.

    Args:
        params (DTreeGenerateFromFmeaInput): fmea_result_id, equipment_id,
            equipment_type, save_as_guide

    Returns:
        str: JSON with the generated tree, and guide_id if save_as_guide=True
    """
    return await _client.call("dtree/generate_from_fmea", params.model_dump())


@mcp.tool(
    name="rca_guide_pdf_preview",
    annotations={'title': 'Preview PDF Before Ingestion', 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False},
)
async def rca_guide_pdf_preview(params: GuidePDFPreviewInput) -> str:
    """
    🌟 Starter+ — Preview a PDF document before full ingestion to verify
    parsing quality. Always call this BEFORE rca_guide_ingest_pdf.

    Strategies: text_native (born-digital, fastest), ocr (scanned, needs
    Tesseract), table (parts lists/spec tables), mixed (combination),
    auto (recommended default).

    Args:
        params (GuidePDFPreviewInput): pdf_base64, n_pages, strategy

    Returns:
        str: JSON with detected_strategy, page_count, scanned_page_ratio,
             estimated_quality, sample_text, fault_codes_preview,
             part_numbers_preview, tables_found, recommendations, dependencies
    """
    return await _client.call("guide/pdf_preview", params.model_dump())


@mcp.tool(
    name="rca_guide_ingest_pdf",
    annotations={'title': 'Ingest PDF Equipment Manual into Knowledge Base', 'readOnlyHint': False, 'destructiveHint': False, 'idempotentHint': False, 'openWorldHint': False},
)
async def rca_guide_ingest_pdf(params: GuidePDFIngestInput) -> str:
    """
    🌟 Starter+ — Parse a PDF equipment manual and ingest it into the RCA
    knowledge base. Rejects non-PDF input (checked via file signature,
    not just the base64 wrapper) and files over 50MB.

    A quality gate runs automatically: if the parsed quality score
    falls below min_quality_threshold (default 0.3), ingestion is
    refused with suggestions -- set skip_preview_check=true to bypass
    it, or lower min_quality_threshold, if you've already reviewed the
    content via rca_guide_pdf_preview and are OK with a rougher parse.

    Recommended workflow: 1) rca_guide_pdf_preview to check quality,
    2) rca_guide_ingest_pdf if quality >= 0.5, 3) rca_guide_search to verify.

    Plan limits: Starter up to 10 guides total, Pro up to 100, Enterprise
    unlimited. Max PDF size: 50MB.

    Args:
        params (GuidePDFIngestInput): pdf_base64, equipment_id, equipment_type,
            name, tags, version, strategy, ocr_dpi, ocr_language, max_pages,
            skip_preview_check, min_quality_threshold

    Returns:
        str: JSON with guide_id, section_count, fault_codes, part_numbers,
             parse_quality, strategy_used, page_count, word_count
    """
    return await _client.call("guide/ingest_pdf", params.model_dump())


if __name__ == "__main__":
    mcp.run()  # stdio — the connector always runs stdio; the private
               # API it forwards to is what's deployed over HTTP.
