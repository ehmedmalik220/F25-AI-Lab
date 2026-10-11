"""Uniform-cost search on a weighted extension of the lab graph."""
import heapq
from lab3_bfs_dfs import GRAPH

WEIGHTS = {
    ("A", "B"): 1, ("B", "D"): 1, ("B", "E"): 1,
    ("C", "F"): 1, ("E", "G"): 1, ("A", "C"): 5,
    ("C", "G"): 7,
}

WEIGHTED_GRAPH = {
    node: list(neighbours) for node, neighbours in GRAPH.items()
}
WEIGHTED_GRAPH["C"] = ["F", "G"]


def bfs_weighted(start, goal):
    frontier = [(start, [start])]
    seen = {start}
    while frontier:
        node, path = frontier.pop(0)
        if node == goal:
            return path
        for nxt in WEIGHTED_GRAPH[node]:
            if nxt not in seen:
                seen.add(nxt)
                frontier.append((nxt, path + [nxt]))
    return None


def ucs(start, goal):
    frontier = [(0, 0, start, [start])]
    counter = 1
    best = {start: 0}
    processed = []
    while frontier:
        cost, _, node, path = heapq.heappop(frontier)
        if cost != best.get(node):
            continue
        processed.append((node, cost))
        if node == goal:
            return path, cost, processed
        for nxt in WEIGHTED_GRAPH[node]:
            new_cost = cost + WEIGHTS[(node, nxt)]
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(frontier, (new_cost, counter, nxt, path + [nxt]))
                counter += 1
    return None, None, processed


def path_cost(path):
    return sum(WEIGHTS[(a, b)] for a, b in zip(path, path[1:]))


ucs_path, ucs_cost, processed = ucs("A", "G")
bfs_path = bfs_weighted("A", "G")
print("weights", WEIGHTS)
print("BFS path", bfs_path, "hops", len(bfs_path) - 1, "cost", path_cost(bfs_path))
print("UCS path", ucs_path, "hops", len(ucs_path) - 1, "cost", ucs_cost)
print("UCS processed", processed)
print("UCS independently summed cost", path_cost(ucs_path))
