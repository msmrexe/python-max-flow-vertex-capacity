# maxflow/transformer.py

"""
Handles the graph transformation for vertex capacities.

This module converts a graph with node capacities into an
equivalent graph with only edge capacities, which can then
be solved by a standard max-flow algorithm.
"""

def transform_graph(
    nodes: dict[str, int], 
    edges: list[tuple[str, str, int]], 
    source: str, 
    sink: str
) -> tuple[list[list[int]], int, int, list[str]]:
    """
    Transforms a graph with node capacities into one with only edge capacities.

    The "vertex-splitting" trick is used:
    1. Each node 'v' becomes two nodes: 'v_in' and 'v_out'.
    2. An internal edge ('v_in', 'v_out') is added with the
       capacity of the original node 'v'.
    3. Each original edge ('u', 'v') becomes ('u_out', 'v_in').
    
    Args:
        nodes: A dictionary mapping node names to their capacity.
               e.g., {"s": 100, "a": 20, "t": 100}
        edges: A list of tuples for each edge: (from, to, capacity).
               e.g., [("s", "a", 10), ("a", "t", 25)]
        source: The name of the original source node.
        sink: The name of the original sink node.

    Returns:
        A tuple containing:
        (new_matrix, new_source_idx, new_sink_idx, node_names)
        - new_matrix: The adjacency matrix of the transformed graph.
        - new_source_idx: The index of the *new* source.
        - new_sink_idx: The index of the *new* sink.
        - node_names: An ordered list of original node names for mapping.
    """
    
    # Create an ordered list of node names to map them to indices
    node_names = list(nodes.keys())
    node_map = {name: i for i, name in enumerate(node_names)}
    
    original_n = len(node_names)
    new_n = original_n * 2  # Each node is split in two
    
    # Initialize the new, larger adjacency matrix
    new_matrix = [[0] * new_n for _ in range(new_n)]

    # --- Step 1: Add internal edges for node capacities ---
    for name, capacity in nodes.items():
        i = node_map[name]
        
        # Get indices for the 'in' and 'out' nodes
        in_node_idx = 2 * i
        out_node_idx = 2 * i + 1
        
        # Add the internal edge with the node's capacity
        new_matrix[in_node_idx][out_node_idx] = capacity

    # --- Step 2: Add edges for original edge capacities ---
    for u_name, v_name, capacity in edges:
        u_idx = node_map[u_name]
        v_idx = node_map[v_name]
        
        # Get indices for 'u_out' and 'v_in'
        u_out_idx = 2 * u_idx + 1
        v_in_idx = 2 * v_idx
        
        # Add the re-routed edge
        new_matrix[u_out_idx][v_in_idx] = capacity

    # --- Step 3: Define new source and sink ---
    # The new source is the *out-node* of the original source.
    new_source_idx = 2 * node_map[source] + 1
    
    # The new sink is the *in-node* of the original sink.
    new_sink_idx = 2 * node_map[sink]
    
    return new_matrix, new_source_idx, new_sink_idx, node_names
