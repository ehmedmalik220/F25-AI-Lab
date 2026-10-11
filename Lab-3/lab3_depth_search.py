"""Depth-limited search and iterative deepening on the supplied graph."""
from lab3_bfs_dfs import GRAPH


def dls(start, goal, limit):
    trace = []

    def visit(node, path, depth):
        trace.append((node, depth))
        if node == goal:
            return "FOUND", path
        if depth == limit:
            return "CUTOFF", None
        saw_cutoff = False
        for nxt in GRAPH[node]:
            if nxt in path:
                continue
            status, result = visit(nxt, path + [nxt], depth + 1)
            if status == "FOUND":
                return status, result
            if status == "CUTOFF":
                saw_cutoff = True
        return ("CUTOFF" if saw_cutoff else "FAILURE"), None

    status, path = visit(start, [start], 0)
    return status, path, trace


def iddfs(start, goal, max_depth):
    attempts = []
    for limit in range(max_depth + 1):
        status, path, trace = dls(start, goal, limit)
        attempts.append((limit, status, path, trace))
        if status == "FOUND":
            return path, attempts
    return None, attempts


for limit in (1, 2, 3, 4):
    status, path, trace = dls("A", "G", limit)
    print("DLS", limit, status, path, "visited", [node for node, _ in trace])

for max_depth in (1, 2, 3, 4):
    path, attempts = iddfs("A", "G", max_depth)
    print("IDDFS", max_depth, "path", path, "limits", [(limit, status) for limit, status, _, _ in attempts])
