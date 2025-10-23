# maxflow/edmonds_karp.py

"""
Contains the Edmonds-Karp algorithm for finding the max flow.

This implementation is a generic max-flow solver that operates
on a given graph (adjacency matrix) and does not know
anything about vertex-capacity transformations.
"""

def _bfs(graph: list[list[int]], source: int, sink: int, parent: list[int]) -> bool:
    """
    Performs a Breadth-First Search on the residual graph to find
    an augmenting path.

    Args:
        graph: The residual graph (adjacency matrix).
        source: The source node index.
        sink: The sink node index.
        parent: A list to store the path (filled by this function).

    Returns:
        True if a path from source to sink exists, False otherwise.
    """
    num_vertices = len(graph)
    visited = [False] * num_vertices
    queue = []

    # Start BFS from the source
    queue.append(source)
    visited[source] = True
    parent[source] = -1  # Source has no parent

    while queue:
        u = queue.pop(0)
        
        for v in range(num_vertices):
            # If not visited and there is capacity
            if not visited[v] and graph[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                
                # If we've reached the sink, a path is found
                if v == sink:
                    return True

    # No path found to the sink
    return False

def find_max_flow(graph: list[list[int]], source: int, sink: int) -> tuple[int, list[list[int]]]:
    """
    Finds the maximum flow in a graph using the Edmonds-Karp algorithm.

    Args:
        graph: The graph's adjacency matrix (edge capacities).
        source: The source node index.
        sink: The sink node index.

    Returns:
        A tuple containing:
        (max_flow_value, residual_graph)
    """
    num_vertices = len(graph)
    
    # Create a deep copy of the graph to use as the residual graph
    # This avoids modifying the original graph.
    residual_graph = [row[:] for row in graph]
    
    # This list is filled by the BFS to store the augmenting path
    parent = [0] * num_vertices
    
    max_flow = 0

    # While an augmenting path exists in the residual graph
    while _bfs(residual_graph, source, sink, parent):
        
        # Find the path's bottleneck capacity (path_flow)
        path_flow = float('Inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]

        # Add this path's flow to the total max flow
        max_flow += path_flow

        # Update the residual capacities of the edges and reverse edges
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow  # Forward edge
            residual_graph[v][u] += path_flow  # Backward edge (for re-routing)
            v = parent[v]
            
    return max_flow, residual_graph
