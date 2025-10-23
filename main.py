# main.py

"""
Max Flow with Vertex Capacities - Command-Line Interface

This script finds the maximum flow in a directed graph that has
capacities on both its edges and its nodes (vertices).

It reads a graph definition from a JSON file, performs a
"vertex-splitting" transformation, solves the max-flow
problem using the Edmonds-Karp algorithm, and reports
the total flow and the flow through each original component.
"""

import json
import argparse
from maxflow.transformer import transform_graph
from maxflow.edmonds_karp import find_max_flow

def load_graph_from_json(file_path: str) -> dict:
    """Loads and validates the graph definition from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Basic validation
        if "nodes" not in data or "edges" not in data:
            raise ValueError("JSON must contain 'nodes' and 'edges' keys.")
        if "source" not in data or "sink" not in data:
            raise ValueError("JSON must contain 'source' and 'sink' keys.")
            
        return data
        
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{file_path}'")
        exit(1)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{file_path}'")
        exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

def get_flow_results(
    original_graph: dict, 
    residual_graph: list[list[int]], 
    node_names: list[str]
) -> tuple[dict, dict]:
    """
    Calculates the final flow used on each original node and edge.

    Args:
        original_graph: The original graph definition from JSON.
        residual_graph: The final residual graph from Edmonds-Karp.
        node_names: The ordered list of original node names.

    Returns:
        A tuple (node_flows, edge_flows)
    """
    node_map = {name: i for i, name in enumerate(node_names)}
    node_flows = {}
    edge_flows = {}

    # 1. Calculate flow through each original NODE
    for name, capacity in original_graph["nodes"].items():
        i = node_map[name]
        in_node_idx = 2 * i
        out_node_idx = 2 * i + 1
        
        # The flow used is the original capacity minus the
        # remaining capacity in the residual graph.
        flow_used = capacity - residual_graph[in_node_idx][out_node_idx]
        node_flows[name] = {"flow_used": flow_used, "capacity": capacity}

    # 2. Calculate flow through each original EDGE
    for u_name, v_name, capacity in original_graph["edges"]:
        u_idx = node_map[u_name]
        v_idx = node_map[v_name]
        
        u_out_idx = 2 * u_idx + 1
        v_in_idx = 2 * v_idx
        
        flow_used = capacity - residual_graph[u_out_idx][v_in_idx]
        edge_flows[f"{u_name}->{v_name}"] = {"flow_used": flow_used, "capacity": capacity}
        
    return node_flows, edge_flows

def main():
    """Main function to run the max-flow calculation."""
    
    parser = argparse.ArgumentParser(
        description="Find max flow in a graph with node and edge capacities."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the .json file defining the graph."
    )
    args = parser.parse_args()

    # 1. Load and transform the graph
    print(f"Loading graph from '{args.input_file}'...")
    original_graph = load_graph_from_json(args.input_file)
    
    new_matrix, new_source, new_sink, node_names = transform_graph(
        original_graph["nodes"],
        original_graph["edges"],
        original_graph["source"],
        original_graph["sink"]
    )

    # 2. Find the max flow
    print("Calculating max flow using Edmonds-Karp...")
    max_flow_value, residual_graph = find_max_flow(new_matrix, new_source, new_sink)

    print("\n--- 3. Results ---")
    print(f"TOTAL MAXIMUM FLOW: {max_flow_value}")

    # 3. Report the flow distribution
    node_flows, edge_flows = get_flow_results(
        original_graph, 
        residual_graph, 
        node_names
    )

    print("\nFlow through NODES:")
    for name, data in node_flows.items():
        print(f"  - Node {name}: {data['flow_used']} / {data['capacity']}")

    print("\nFlow through EDGES:")
    for name, data in edge_flows.items():
        if data['flow_used'] > 0: # Only show edges that are used
            print(f"  - Edge {name}: {data['flow_used']} / {data['capacity']}")

if __name__ == "__main__":
    main()
