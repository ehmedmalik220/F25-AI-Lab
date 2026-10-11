"""Lab 3: BFS, DFS, DLS, IDDFS and UCS."""
from collections import deque
import heapq

GRAPH = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"],
         "D": [], "E": ["G"], "F": [], "G": []}
WEIGHTS = {("A", "B"): 1, ("B", "D"): 1, ("B", "E"): 1,
           ("E", "G"): 1, ("A", "C"): 5, ("C", "F"): 1,
           ("C", "G"): 7}
WEIGHTED_GRAPH = {node: list(neighbours) for node, neighbours in GRAPH.items()}
WEIGHTED_GRAPH["C"] = ["F", "G"]

def bfs(start, goal, graph=GRAPH):
    queue = deque([(start, [start])])
    seen = {start}
    order = []
    while queue:
        node, path = queue.popleft()
        order.append(node)
        if node == goal:
            return path, order
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None, order

def dfs(start, goal):
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
        for nxt in reversed(GRAPH[node]):
            stack.append((nxt, path + [nxt]))
    return None, order

def dls(start, goal, limit):
    order = []
    def visit(node, path, depth):
        order.append(node)
        if node == goal:
            return "FOUND", path
        if depth == limit:
            return "CUTOFF", None
        cutoff = False
        for nxt in GRAPH[node]:
            if nxt in path:
                continue
            status, result = visit(nxt, path + [nxt], depth + 1)
            if status == "FOUND":
                return status, result
            cutoff = cutoff or status == "CUTOFF"
        return ("CUTOFF" if cutoff else "FAILURE"), None
    status, path = visit(start, [start], 0)
    return status, path, order

def iddfs(start, goal, max_depth):
    for limit in range(max_depth + 1):
        status, path, order = dls(start, goal, limit)
        if status == "FOUND":
            return path, limit, order
    return None, max_depth, []

def ucs(start, goal):
    frontier = [(0, 0, start, [start])]
    best = {start: 0}
    counter = 1
    order = []
    while frontier:
        cost, _, node, path = heapq.heappop(frontier)
        if cost != best.get(node):
            continue
        order.append((node, cost))
        if node == goal:
            return path, cost, order
        for nxt in WEIGHTED_GRAPH[node]:
            new_cost = cost + WEIGHTS[(node, nxt)]
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(frontier, (new_cost, counter, nxt, path + [nxt]))
                counter += 1
    return None, None, order

bfs_path, bfs_order = bfs("A", "G")
dfs_path, dfs_order = dfs("A", "G")
ucs_path, ucs_cost, ucs_order = ucs("A", "G")
print("BFS", bfs_path, bfs_order)
print("DFS", dfs_path, dfs_order)
print("DLS limit 2", dls("A", "G", 2))
print("IDDFS", iddfs("A", "G", 4)[:2])
print("UCS", ucs_path, ucs_cost, ucs_order)
