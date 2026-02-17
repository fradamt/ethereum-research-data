"""SQLite graph sidecar: nodes, edges, dependency tracking."""

from erd_index.graph.edge_builder import build_edges_from_chunk
from erd_index.graph.node_builder import chunk_to_node
from erd_index.graph.store import (
    delete_nodes_by_file,
    get_connection,
    get_eip_context,
    get_neighbors,
    get_stats,
    init_graph_db,
    upsert_code_dep,
    upsert_cross_ref,
    upsert_eip_dep,
    upsert_node,
    upsert_spec_code_link,
)

__all__ = [
    "build_edges_from_chunk",
    "chunk_to_node",
    "delete_nodes_by_file",
    "get_connection",
    "get_eip_context",
    "get_neighbors",
    "get_stats",
    "init_graph_db",
    "upsert_code_dep",
    "upsert_cross_ref",
    "upsert_eip_dep",
    "upsert_node",
    "upsert_spec_code_link",
]
