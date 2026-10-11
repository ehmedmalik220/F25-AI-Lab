"""CAI601400 Artificial Intelligence Lab 3.

Uninformed search on the supplied emergency-exit graph:
BFS, DFS, DLS, IDDFS, and UCS.
"""
from collections import deque
import heapq

# Successor order is fixed to make every trace reproducible.
GRAPH = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": [],
}

# Weighted extension from the manual: C -> G is an alternative corridor.
WEIGHTED_GRAPH = {node: list(neighbours) for node, neighbours in GRAPH.items()}
WEIGHTED_GRAPH["C"] = ["F", "G"]
WEIGHTS = {
    ("A", "B"): 1,
    ("B", "D"): 1,
    ("B", "E"): 1,
    ("E", "G"): 1,
    ("A", "C"): 5,
    ("C", "F"): 1,
    ("C", "G"): 7,
}


def bfs(start, goal, graph=GRAPH):
    """Return (path, expansion_order), using a FIFO frontier."""
    queue = deque([(start, [start])])
    seen = {start}
    order = []
    while queue:
        node, path = queue.popleft()
        order.append(node)
        if node == goal:
            return path, order
        for nxt in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None, order


def dfs(start, goal, graph=GRAPH):
    """Return (path, expansion_order), preserving left-to-right DFS order."""
    stack = [(start, [start])]
    seen = set()
    order = []
    while stack:
        node, path = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        if node == goal:
            return path, order
        for nxt in reversed(graph.get(node, [])):
            if nxt not in seen:
                stack.append((nxt, path + [nxt]))
    return None, order


def dls(start, goal, limit, graph=GRAPH):
    """Depth-limited DFS; return (status, path, expansion_order)."""
    order = []

    def visit(node, path, depth):
        order.append(node)
        if node == goal:
            return "FOUND", path
        if depth == limit:
            return "CUTOFF", None
        cutoff_seen = False
        for nxt in graph.get(node, []):
            if nxt in path:  # local path check prevents cycles without hiding routes
                continue
            status, result = visit(nxt, path + [nxt], depth + 1)
            if status == "FOUND":
                return status, result
            cutoff_seen = cutoff_seen or status == "CUTOFF"
        return ("CUTOFF" if cutoff_seen else "FAILURE"), None

    status, path = visit(start, [start], 0)
    return status, path, order


def iddfs(start, goal, max_depth, graph=GRAPH):
    """Run fresh DLS passes from depth 0 through max_depth."""
    passes = []
    for limit in range(max_depth + 1):
        status, path, order = dls(start, goal, limit, graph)
        passes.append((limit, status, path, order))
        if status == "FOUND":
            return path, limit, passes
    return None, max_depth, passes


def ucs(start, goal, graph=WEIGHTED_GRAPH, weights=WEIGHTS):
    """Return (path, cost, expansion_order), using a min-priority queue."""
    frontier = [(0, 0, start, [start])]
    best_cost = {start: 0}
    counter = 1
    order = []
    while frontier:
        cost, _, node, path = heapq.heappop(frontier)
        if cost != best_cost.get(node):
            continue
        order.append((node, cost))
        if node == goal:
            return path, cost, order
        for nxt in graph.get(node, []):
            new_cost = cost + weights[(node, nxt)]
            if new_cost < best_cost.get(nxt, float("inf")):
                best_cost[nxt] = new_cost
                heapq.heappush(frontier, (new_cost, counter, nxt, path + [nxt]))
                counter += 1
    return None, None, order


def run_experiments():
    """Print reproducible evidence required by the lab manual."""
    print("=== State-space formulation ===")
    print("initial=A | goal=G | actions=successor edges | goal_test=node == G")
    print("unweighted graph:", GRAPH)
    print("weighted graph:", WEIGHTED_GRAPH)

    print("\n=== BFS and DFS on supplied A-G graph ===")
    for name, search in (("BFS", bfs), ("DFS", dfs)):
        path, order = search("A", "G")
        print(f"{name}: path={path}; expansions={order}; edges={len(path)-1 if path else None}")

    print("\n=== DLS limits 1, 2, 3, 4 ===")
    for limit in (1, 2, 3, 4):
        status, path, order = dls("A", "G", limit)
        print(f"DLS limit={limit}: status={status}; path={path}; expansions={order}")

    print("\n=== IDDFS through depth 4 ===")
    path, depth, passes = iddfs("A", "G", 4)
    for limit, status, pass_path, order in passes:
        print(f"IDDFS limit={limit}: status={status}; path={pass_path}; expansions={order}")
    print(f"IDDFS result: path={path}; depth={depth}")

    print("\n=== BFS versus UCS on weighted extension ===")
    bfs_path, bfs_order = bfs("A", "G", WEIGHTED_GRAPH)
    ucs_path, ucs_cost, ucs_order = ucs("A", "G")
    print(f"BFS weighted: path={bfs_path}; edges={len(bfs_path)-1}; cost={path_cost(bfs_path)}; expansions={bfs_order}")
    print(f"UCS weighted: path={ucs_path}; edges={len(ucs_path)-1}; cost={ucs_cost}; expansions={ucs_order}")
    print("comparison: BFS minimizes edge count; UCS minimizes positive accumulated cost")

    print("\n=== Edge-case tests ===")
    print("unreachable BFS:", bfs("A", "Z"))
    print("unreachable DLS:", dls("A", "Z", 4))
    cyclic = {"A": ["B"], "B": ["A", "G"], "G": []}
    print("cycle-safe DFS:", dfs("A", "G", cyclic))


def path_cost(path):
    if not path:
        return None
    return sum(WEIGHTS[(a, b)] for a, b in zip(path, path[1:]))


if __name__ == "__main__":
    run_experiments()
