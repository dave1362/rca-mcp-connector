"""
RCA-MCP Public Connector — Pydantic Input Schemas
====================================================
Thin, standalone input models mirroring the private API's tool
signatures. Contains ONLY schema definitions — no business logic,
no security internals, no storage/model implementations. Model
family/status fields use plain str + regex pattern rather than
importing the private core's enums, so this package has zero
dependency on private modules.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AuthSetupInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    roles: List[str] = Field(
        default_factory=lambda: ["analyst"],
        description="Roles recorded against this API key for audit purposes. "
                     "Does NOT grant authorization — the API key's actual roles "
                     "and feature limits are always Free plan for self-service keys.",
        max_length=5,
    )
    key_id: Optional[str] = Field(
        default=None, max_length=64,
        description="Accepted for backward compatibility, ignored — DB-issued "
                     "keys use their own server-generated ID, not a caller-chosen one.",
    )
    key_label: str = Field(
        default="", max_length=64,
        description="Optional human-readable label for this API key",
    )


class ListKeysInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")


class RotateKeyInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    key_id: str = Field(..., description="Existing key ID to rotate")


class RevokeTokenInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    key_id_to_revoke: str = Field(
        ..., description="UUID of one of your own keys to deactivate (can be the same key presented in 'token')"
    )


class HealthInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key from rca_auth_generate_token")
    client_id: str = Field(default="default", description="Client identifier for rate limiting")


class AuditInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key")
    client_id: str = Field(default="default", description="Client namespace ID")
    hour_key: Optional[str] = Field(
        default=None,
        description="Hour bucket YYYYMMDD_HH (default: current hour)",
    )


class PurgeInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key")
    client_id: str = Field(default="default", description="Client namespace ID")
    namespace: str = Field(
        ..., description="One of: graphs, models, results", pattern="^(graphs|models|results)$"
    )
    confirm: bool = Field(..., description="Must be true to proceed with purge")


class GraphCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key")
    client_id: str = Field(default="default", description="Client namespace ID")
    name: str = Field(..., min_length=1, max_length=128, description="Graph name")
    description: str = Field(default="", max_length=512, description="Optional free-text notes on this graph's purpose")


class GraphGetInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph ID returned by rca_graph_create")
    format: str = Field(
        default="json",
        description="Output format: json | dot | adjacency",
        pattern="^(json|dot|adjacency)$",
    )


class GraphScoreInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph to score")


class GraphDiscoverInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    name: str = Field(..., min_length=1, max_length=128, description="Name for the discovered graph")
    data: Dict[str, List[float]] = Field(
        ..., description="Dict of {variable_name: [values]}. Min 30 samples, max 50 variables."
    )
    significance: float = Field(
        default=0.05, ge=0.001, le=0.5,
        description="P-value threshold for the discovery algorithm's independence tests, 0.001-0.5 (default 0.05, standard); lower = stricter, fewer edges found",
    )


class GraphDeleteInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph ID to delete")
    confirm: bool = Field(..., description="Must be true to delete")


class GraphListVersionsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph ID to list versions for")


class GraphRestoreVersionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph ID to restore")
    version_id: str = Field(..., description="Version ID to restore to (see rca_graph_list_versions)")
    confirm: bool = Field(..., description="Must be true to proceed")


class GraphMergeInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id_a: str = Field(..., description="First graph")
    graph_id_b: str = Field(..., description="Second graph")
    merged_name: str = Field(..., min_length=1, max_length=128, description="Name for the merged graph")
    conflict_resolution: str = Field(
        default="union", pattern="^(union|intersection)$",
        description="'union' (all nodes from both) or 'intersection' (only shared nodes)",
    )


class NodeOpInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph to add the node to")
    name: str = Field(..., min_length=1, max_length=128, description="Unique node name within the graph")
    node_type: str = Field(
        default="metric",
        pattern="^(metric|incident|symptom|root_cause|intermediate)$",
        description="One of: metric | incident | symptom | root_cause | intermediate — used to color/classify nodes in reports and graph views",
    )
    description: str = Field(default="", max_length=256, description="Optional free-text notes on what this node represents")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Optional arbitrary key-value metadata attached to the node")


class RemoveNodeInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph to modify")
    name: str = Field(
        ..., min_length=1, max_length=128,
        description="Exact node name as it appears in the graph (case-sensitive)",
    )


class EdgeOpInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph to add the edge to")
    source: str = Field(..., min_length=1, max_length=128, description="Cause node name (must already exist in the graph)")
    target: str = Field(..., min_length=1, max_length=128, description="Effect node name (must already exist in the graph)")
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Causal strength, 0.0-1.0 (default 1.0 = full strength)")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="How confident you are in this edge, 0.0-1.0 (default 1.0)")
    method: str = Field(default="manual", max_length=64, description="How this edge was determined, e.g. 'manual', 'granger_causality', 'domain_expert' — free text, used for provenance display only")


class RemoveEdgeInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph to modify")
    source: str = Field(
        ..., min_length=1, max_length=128,
        description="Exact source node name (case-sensitive); the edge source→target must currently exist",
    )
    target: str = Field(
        ..., min_length=1, max_length=128,
        description="Exact target node name (case-sensitive)",
    )


class PathScoreInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph to search")
    target_node: str = Field(..., description="Incident or effect node to trace causes for")
    top_k: int = Field(default=10, ge=1, le=50, description="Number of top paths to return")


class MarkovBlanketInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    graph_id: str = Field(..., description="Graph containing the node")
    node: str = Field(..., description="Node to compute Markov blanket for")


class ModelCreateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    name: str = Field(..., min_length=1, max_length=128, description="Model name (for your own reference — doesn't affect behavior)")
    family: str = Field(..., pattern=r"^(bayesian_network|dowhy_causal_inference|granger_causality|fault_tree_analysis|fishbone_ishikawa|fmea|bayesian_structural_time_series|change_point_detection|random_forest_importance|counterfactual_analysis)$", description="RCA model family (see rca_admin_health for list)")
    description: str = Field(default="", max_length=512, description="Optional free-text notes on what this model is for")
    config: Dict[str, Any] = Field(
        default_factory=dict, description="Family-specific configuration parameters"
    )
    tags: List[str] = Field(default_factory=list, max_length=10, description="Up to 10 free-text labels for filtering with rca_model_list")
    version: str = Field(default="1.0.0", max_length=32, description="Your own version label for this model (not validated or auto-incremented)")


class ModelListInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    family_filter: Optional[str] = Field(default=None, pattern=r"^(bayesian_network|dowhy_causal_inference|granger_causality|fault_tree_analysis|fishbone_ishikawa|fmea|bayesian_structural_time_series|change_point_detection|random_forest_importance|counterfactual_analysis)$", description="Only return models of this family (omit for all families)")
    status_filter: Optional[str] = Field(default=None, pattern=r"^(draft|trained|validated|deployed|deprecated|failed)$", description="Only return models with this status: draft | trained | validated | deployed | deprecated | failed (omit for all statuses)")


class ModelStatusInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    model_id: str = Field(..., description="Model ID to update")
    new_status: str = Field(..., pattern=r"^(draft|trained|validated|deployed|deprecated|failed)$", description="Target status")


class ModelValidateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    model_id: str = Field(..., description="Model to validate (from rca_model_create)")
    validation_data: Dict[str, List[Any]] = Field(
        ..., description="Hold-out dataset for validation: {variable: [values]}"
    )
    target: str = Field(..., description="Target variable name for validation metrics")


class ModelDeleteInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    model_id: str = Field(..., description="Model to permanently delete")
    confirm: bool = Field(..., description="Must be true to proceed with the deletion")


class RunAnalysisInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    model_id: str = Field(..., description="Model to run (must exist in registry)")
    payload: Dict[str, Any] = Field(
        ...,
        description=(
            "Analysis payload. Required keys vary by model family:\n"
            "  bayesian_network/granger/random_forest/counterfactual: {data, target}\n"
            "  fault_tree: {tree, basic_event_probs}\n"
            "  fishbone: {effect, causes, framework}\n"
            "  fmea: {failure_modes, rpn_threshold}\n"
            "  change_point: {series, timestamps}\n"
            "  counterfactual: {data, target, interventions}"
        ),
    )
    save: bool = Field(default=True, description="Persist the result to disk")
    tags: List[str] = Field(
        default_factory=list, max_length=10,
        description="Tags for retrieval via rca_analysis_query_results",
    )
    ai_summary: bool = Field(
        default=False,
        description=(
            "Also generate a short plain-English executive summary via "
            "Claude Haiku (platform-provided key). Starter+ only, subject "
            "to a monthly quota (Starter 100, Pro 1000, Enterprise "
            "unlimited) -- see ai_summary/ai_summary_error in the response. "
            "Free plan or a used-up quota returns ai_summary_error instead "
            "of failing the analysis itself."
        ),
    )


class GetResultInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    result_id: str = Field(
        ..., description="A result_id returned by a prior analysis call (not a model_id or graph_id)"
    )


class ListResultsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    limit: int = Field(default=20, ge=1, le=100, description="Page size, 1-100")
    offset: int = Field(
        default=0, ge=0, description="Number of results to skip from the newest, for paging"
    )


class QueryResultsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    model_family: Optional[str] = Field(default=None, description="Filter by model family")
    min_confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Only return results with confidence_overall at or above this, 0.0-1.0 (default 0.0 = no filter)")
    after_ts: Optional[str] = Field(
        default=None, description="ISO timestamp — only results executed at or after this"
    )
    tags: Optional[List[str]] = Field(default=None, description="Match results with any of these tags")
    limit: int = Field(default=20, ge=1, le=100, description="Page size, 1-100")
    offset: int = Field(default=0, ge=0, description="Number of matching results to skip, for paging")


class CompareResultsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    result_ids: List[str] = Field(..., min_length=2, max_length=10, description="2-10 result_ids to compare side by side (from rca_analysis_run or rca_analysis_list_results)")


class ExplainInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    result_id: str = Field(..., description="Result to explain")
    detail_level: str = Field(
        default="standard",
        pattern="^(brief|standard|verbose)$",
        description="Explanation verbosity: brief | standard | verbose",
    )


class BatchAnalysisInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    model_id: str = Field(..., description="Model to apply to all incidents")
    incidents: List[Dict[str, Any]] = Field(
        ...,
        min_length=1,
        max_length=20,
        description=(
            "1-20 payload dicts (capped by your plan's max_batch_size), "
            "one per incident. Each must match the shape rca_analysis_run "
            "expects for this model family, e.g. for time-series families: "
            '{"data": {var: [values, ...], ...}, "target": "var_name"}'
        ),
    )


class EnsembleInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    model_ids: List[str] = Field(
        ..., min_length=2, max_length=5, description="2-5 model IDs to ensemble"
    )
    payload: Dict[str, Any] = Field(..., description="Shared payload passed to all models")
    weights: Optional[List[float]] = Field(
        default=None, description="Per-model weights (default: equal weighting)"
    )
    save: bool = Field(default=True, description="Persist the ensembled result server-side for later retrieval (default true)")


class EpsilonDiagnosisInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    normal_data: Dict[str, List[float]] = Field(
        ..., description="Baseline metric data {metric: [values]}. Min 3 values per metric.")
    anomaly_data: Dict[str, List[float]] = Field(
        ..., description="Incident window metric data. Min 1 value per metric.")
    sli_metric: str = Field(
        ..., description="Service Level Indicator — the metric where anomaly was observed")
    epsilon: float = Field(
        default=3.0, ge=1.0, le=10.0,
        description="Anomaly threshold in standard deviations (default 3.0)")


class RandomWalkInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    adjacency: Dict[str, Dict[str, float]] = Field(
        ..., description="{source: {target: edge_weight}} directed adjacency dict")
    anomaly_scores: Dict[str, float] = Field(
        ..., description="{metric: anomaly_score} — higher = more anomalous")
    sli_metric: str = Field(..., description="SLI node to start random walk from")
    restart_prob: float = Field(
        default=0.15, ge=0.05, le=0.5,
        description="Personalised restart probability (default 0.15)")


class HTDiagnosisInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    data: Dict[str, List[float]] = Field(
        ..., description="{metric: [time_series_values]} full time series")
    adjacency: Dict[str, Dict[str, float]] = Field(
        ..., description="{source: {target: weight}} causal graph")
    sli_metric: str = Field(..., description="SLI metric where anomaly was observed")
    anomaly_start_idx: int = Field(
        ..., ge=5, description="Index where anomaly begins (min 5 pre-period points)")
    significance: float = Field(
        default=0.05, ge=0.001, le=0.2,
        description="P-value threshold for the hypothesis test, 0.001-0.2 (default 0.05); lower = stricter, fewer nodes flagged as anomalous",
    )
    use_descendant_adjustment: bool = Field(
        default=True, description="Apply HT-ADJ descendant adjustment (recommended)")


class ReportGenerateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    result_id: str = Field(..., description="Result ID to generate report from")
    format: str = Field(
        ..., description="Output format: pdf | html | excel | markdown",
        pattern="^(pdf|html|excel|markdown)$"
    )
    title: str = Field(
        default="RCA Analysis Report",
        max_length=200,
        description="Custom report title"
    )
    include_raw: bool = Field(
        default=False,
        description="Include raw model output appendix (increases report size)"
    )
    save: bool = Field(
        default=True,
        description="Save report to storage and return report_id"
    )


class ReportCompareInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    result_ids: List[str] = Field(..., min_length=2, max_length=10, description="2-10 result_ids to compare in one report")
    format: str = Field(default="markdown", pattern="^(markdown|html)$", description="Output format: markdown (default) or html")
    title: str = Field(default="RCA Comparative Analysis Report", max_length=200, description="Report title, up to 200 chars")
    save: bool = Field(default=True, description="Persist the report server-side for later retrieval (default true)")


class ProviderConfigInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    provider: Optional[str] = Field(
        default=None,
        description=(
            "Provider key. Available: claude_desktop, claude_code, cursor, "
            "ollama_mcphost, groq_mcphost, openai_agents, gemini_mcphost, "
            "langchain_langgraph, openrouter, remote_http. "
            "Omit to list all providers."
        )
    )


class PyRCASetupInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")


class RunAnalysisAsyncInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    model_id: str = Field(..., description="Model to run (must exist in registry)")
    payload: Dict[str, Any] = Field(..., description="Analysis payload — same shape as rca_analysis_run")
    save: bool = Field(default=True, description="Persist the result server-side once the task completes (default true)")
    tags: List[str] = Field(default_factory=list, max_length=10, description="Up to 10 free-text labels attached to the saved result, for filtering with rca_analysis_query_results")


class PollTaskInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    task_id: str = Field(..., description="Task ID returned by rca_analysis_run_async")




class PlanInfoInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")


# ── Group H — Equipment Knowledge (Phase 9) ─────────────────────────────────────

class GuideIngestInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    equipment_id: str = Field(..., min_length=1, max_length=128,
        description="Unique equipment identifier e.g. 'pump_XR200_unit3'")
    equipment_type: str = Field(...,
        description="Equipment type e.g. pump, motor, compressor, conveyor, valve, "
                     "sensor, hvac, plc, vacuum_pump, interface_valve, ml_pipeline, "
                     "cfd_solver, custom")
    name: str = Field(..., min_length=1, max_length=256,
        description="Human-readable guide name")
    content: str = Field(..., min_length=10,
        description="Guide content as plain text, Markdown, or JSON decision tree")
    format: str = Field(default="markdown",
        pattern="^(markdown|plain|json_dtree)$",
        description="Guide format: markdown | plain | json_dtree")
    tags: List[str] = Field(default_factory=list,
        description="Domain tags e.g. ['pump', 'hydraulic', 'water-treatment']",
        max_length=20)
    version: str = Field(default="1.0", max_length=20, description="Your own version label for this guide (not validated or auto-incremented)")


class GuideSearchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    symptom: str = Field(..., min_length=3, max_length=512,
        description="Symptom or fault description to search for")
    equipment_type: Optional[str] = Field(default=None,
        description="Filter to specific equipment type")
    tags: Optional[List[str]] = Field(default=None,
        description="Filter by tags e.g. ['pump', 'hydraulic']")
    top_k: int = Field(default=5, ge=1, le=20,
        description="Maximum results to return (Free: max 3, Starter+: max 20)")


class GuideGetInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    guide_id: str = Field(..., description="Guide ID from rca_guide_ingest")
    section_id: Optional[str] = Field(default=None,
        description="Optional: retrieve specific section only")


class GuideListInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    equipment_type: Optional[str] = Field(default=None, description="Only return guides for this equipment type (omit for all types)")
    tags: Optional[List[str]] = Field(default=None, description="Only return guides matching any of these tags (omit for all guides)")


class GuideDeleteInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    guide_id: str = Field(..., description="Guide ID to delete")
    confirm: bool = Field(..., description="Must be true to actually delete")


class DTreeStartInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    guide_id: str = Field(...,
        description="Guide ID of a json_dtree guide, OR 'auto' to generate from FMEA")
    equipment_id: str = Field(..., min_length=1, max_length=128, description="Equipment this diagnostic session is for, e.g. 'pump_XR200_unit3'")
    symptom: str = Field(..., min_length=3, max_length=512,
        description="Initial observed symptom or fault description")
    session_id: Optional[str] = Field(default=None,
        description="Provide to resume an existing session")
    fmea_result_id: Optional[str] = Field(default=None,
        description="When guide_id='auto': result_id of a completed FMEA analysis")


class DTreeAnswerInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    session_id: str = Field(..., description="Active session ID from rca_dtree_start")
    answer: str = Field(..., pattern="^(yes|no|unknown)$",
        description="Answer to current diagnostic question: yes | no | unknown")
    measurement: Optional[str] = Field(default=None, max_length=256,
        description="Optional actual reading e.g. 'bearing temp: 92C, vibration: 8.5mm/s'")


class DTreeListInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    equipment_id: Optional[str] = Field(
        default=None, description="Filter to only this equipment's sessions (omit for all equipment)"
    )
    resolved_only: bool = Field(
        default=False,
        description="If true, only return sessions that reached a final diagnosis (default: include in-progress too)",
    )


class GuideReportInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    session_id: str = Field(
        ..., description="A session_id already marked 'resolved' (check via rca_dtree_list_sessions)"
    )
    format: str = Field(
        default="markdown",
        pattern="^(pdf|html|markdown)$",
        description="'markdown' (default, Starter+) or 'pdf'/'html' (Pro+ only — Starter requesting these gets plan_required, not a silent downgrade)",
    )
    include_guide_refs: bool = Field(default=True,
        description="Include relevant guide section references")
    custom_title: Optional[str] = Field(
        default=None, max_length=200,
        description="Custom report title, up to 200 chars (default: auto-generated from equipment/symptom)",
    )


class DTreeGenerateFromFmeaInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    fmea_result_id: str = Field(..., description="result_id of a completed FMEA analysis")
    equipment_id: str = Field(..., min_length=1, max_length=128, description="Equipment this decision tree is generated for, e.g. 'pump_XR200_unit3'")
    equipment_type: str = Field(default="custom", description="Equipment type; see rca_guide_ingest's schema for supported values (default 'custom' for anything not on that list)")
    save_as_guide: bool = Field(default=True,
        description="If true, ingest the generated tree as a json_dtree guide")


class GuidePDFPreviewInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    pdf_base64: str = Field(
        ...,
        description="Base64-encoded PDF file bytes. "
                     "In Python: base64.b64encode(open('manual.pdf','rb').read()).decode()"
    )
    n_pages: int = Field(default=5, ge=1, le=20,
        description="Number of pages to preview (default 5, max 20)")
    strategy: str = Field(default="auto",
        pattern="^(auto|text_native|ocr|table|mixed)$",
        description="Parsing strategy: auto | text_native | ocr | table | mixed")


class GuidePDFIngestInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(..., description="API key to authenticate this request")
    client_id: str = Field(default="default", description="Client namespace ID")
    pdf_base64: str = Field(..., description="Base64-encoded PDF file bytes")
    equipment_id: str = Field(..., min_length=1, max_length=128,
        description="Unique equipment identifier e.g. 'pump_grundfos_cr32'")
    equipment_type: str = Field(...,
        description="Equipment type: pump | motor | compressor | valve | hvac | "
                     "plc | membrane | vacuum_pump | interface_valve | "
                     "cfd_solver | ml_pipeline | custom | ...")
    name: str = Field(..., min_length=1, max_length=256,
        description="Guide display name e.g. 'Grundfos CR32 Service Manual v4.2'")
    tags: List[str] = Field(default_factory=list,
        description="Domain tags e.g. ['pump', 'hydraulic', 'aquatreat', 'preventive']",
        max_length=20)
    version: str = Field(default="1.0", max_length=20, description="Your own version label for this guide (not validated or auto-incremented)")
    strategy: str = Field(default="auto",
        pattern="^(auto|text_native|ocr|table|mixed)$",
        description="Parsing strategy (default: auto — recommended)")
    ocr_dpi: int = Field(default=300, ge=150, le=600,
        description="OCR resolution in DPI (default 300; use 600 for fine print)")
    ocr_language: str = Field(default="eng", max_length=20,
        description="Tesseract language code (default 'eng'). Multi-language: 'eng+fra', 'eng+deu'.")
    max_pages: Optional[int] = Field(default=None, ge=1, le=2000,
        description="Limit pages parsed (default: all pages)")
    skip_preview_check: bool = Field(default=False,
        description="Skip quality check and ingest regardless of parse_quality score. "
                     "Not recommended — run rca_guide_pdf_preview first.")
    min_quality_threshold: float = Field(default=0.3, ge=0.0, le=1.0,
        description="Minimum parse_quality score required to proceed with ingestion. "
                     "Set to 0.0 to always ingest. Default: 0.3")
