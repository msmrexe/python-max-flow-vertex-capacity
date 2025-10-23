# Max Flow with Vertex Capacities

This project is a Python implementation of the Maximum Flow problem, specifically designed to handle graphs that have capacities on both **edges** and **nodes (vertices)**. This was developed for an Algorithms & Data Structures course and demonstrates the "vertex-splitting" transformation required to solve this problem.

The program uses the **Edmonds-Karp** algorithm to find the maximum flow and reports the total flow as well as the flow distribution across all original nodes and edges.

## The Problem: Data Flow with Two Bottlenecks

Imagine a computer network where you want to send a continuous stream of data from a **source** computer to a **sink** (destination) computer at the maximum possible speed. To do this, you can split the data into packets and send them along multiple paths.

This network has two types of bottlenecks:

1.  **Line Capacity (Edge Capacity):** Each physical connection *between* two computers (an edge) has a maximum bandwidth (e.g., 100 MB/s).
2.  **Router Capacity (Node Capacity):** Each *computer* or router in the network (a node) can only process a certain amount of data per second (e.g., 500 MB/s).

**The Goal:** Find the absolute maximum flow of data (in data per second) that can be sent from the source to the sink, respecting *both* the edge capacities and the node capacities.

## The Solution: Vertex-Splitting Transformation

The core challenge of this problem is that standard max-flow algorithms (like Edmonds-Karp) only support capacities on *edges*. They cannot enforce a capacity limit on a *node*.

To solve this, we perform a graph transformation to create an equivalent graph that *only* has edge capacities.

1.  **Split Nodes:** Every node `v` in the original graph (with capacity `C_v`) is split into two new nodes: an "in-node" `v_in` and an "out-node" `v_out`.

2.  **Add Internal Edge:** A new *internal* edge is created from `v_in` to `v_out`. The capacity of this new edge is set to the capacity of the original node: `capacity(v_in, v_out) = C_v`. This new edge now correctly models the capacity of the node.

3.  **Redirect Edges:** Every original edge `(u, v)` (with capacity `C_uv`) is re-routed in the new graph to connect the *out-node* of `u` to the *in-node* of `v`. The capacity remains the same: `capacity(u_out, v_in) = C_uv`.

4.  **New Source & Sink:**

      * The **new source** becomes the **out-node** of the original source (`source_out`).
      * The **new sink** becomes the **in-node** of the original sink (`sink_in`).

This new, larger graph now perfectly represents the original problem using *only* edge capacities. We can run the standard Edmonds-Karp algorithm on it to find the max flow from `source_out` to `sink_in`.

## Features

  * **Solves Node Capacities:** Correctly finds the max flow in a graph with both node and edge capacities.
  * **Edmonds-Karp Algorithm:** Uses a clean, standard implementation of Edmonds-Karp (BFS on a residual graph).
  * **Modular Package Structure:** All logic is contained within the `maxflow/` Python package.
      * `transformer.py`: Handles the vertex-splitting transformation.
      * `edmonds_karp.py`: Contains the pure max-flow algorithm.
  * **Data-Driven:** The graph is loaded from a flexible `JSON` file instead of being hard-coded.
  * **Clear Results:** The output shows the total max flow and a detailed breakdown of the flow used on every node and edge.

## Project Structure

```
python-max-flow-vertex-capacity/
├── .gitignore               # Git ignore file
├── LICENSE                  # MIT license file
├── README.md                # This documentation
├── main.py                  # Main runnable script (CLI)
├── sample_graph.json        # An example graph input file
└── maxflow/
    ├── __init__.py          # Makes 'maxflow' a Python package
    ├── edmonds_karp.py      # The pure max-flow algorithm
    └── transformer.py       # The vertex-splitting transformation logic
```

## Usage

### 1. Define Your Graph

Create a `.json` file to define your graph, nodes, and edges. See `sample_graph.json` for an example.

**`my_graph.json`:**
```json
{
  "nodes": {
    "s": 100,
    "a": 20,
    "b": 30,
    "t": 100
  },
  "edges": [
    ["s", "a", 15],
    ["s", "b", 20],
    ["a", "t", 25],
    ["b", "t", 10]
  ],
  "source": "s",
  "sink": "t"
}
```
*Note: Node capacities for the source and sink can be set to `Infinity` (or just a very large number) if they are uncapacitated.*

### 2. Run the Program

Run `main.py` and pass your JSON file as an argument.

```bash
python main.py sample_graph.json
```

### Example Output

```
$ python main.py sample_graph.json
Loading graph from 'sample_graph.json'...
Calculating max flow using Edmonds-Karp...

--- Results ---
TOTAL MAXIMUM FLOW: 29

Flow through NODES:
  - Node 0: 15 / 20
  - Node 1: 14 / 15
  - Node 2: 15 / 17
  - Node 3: 25 / 25

Flow through EDGES:
  - Edge 0->1: 15 / 15
  - Edge 1->2: 14 / 14
  - Edge 2->3: 15 / 30
  - Edge 3->1: 0 / 18
  - Edge 3->2: 0 / 15
```
*(Note: The exact flow distribution may vary, but the Total Max Flow will be the same.)*

---

## Author

Feel free to connect or reach out if you have any questions!

* **Maryam Rezaee**
* **GitHub:** [@msmrexe](https://github.com/msmrexe)
* **Email:** [ms.maryamrezaee@gmail.com](mailto:ms.maryamrezaee@gmail.com)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
