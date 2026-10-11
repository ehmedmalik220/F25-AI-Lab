"""BFS and DFS paths plus processing traces for the manual graph."""
from collections import deque

GRAPH = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}


def bfs(start, goal):
    queue = deque([(start, [start])])
    seen = {start}
    trace = []
    while queue:
        node, path = queue.popleft()
        trace.append((node, [item[0] for item in queue]))
        if node == goal:
            return path, trace
        for nxt in GRAPH[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None, trace


def dfs(start, goal):
    stack = [(start, [start])]
    seen = set()
    trace = []
    while stack:
        node, path = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        trace.append((node, [item[0] for item in stack]))
        if node == goal:
            return path, trace
        for nxt in reversed(GRAPH[node]):
            if nxt not in seen:
                stack.append((nxt, path + [nxt]))
    return None, trace


for label, search in (("BFS", bfs), ("DFS", dfs)):
    path, trace = search("A", "G")
    print(label, "path:", path)
    print(label, "visit order:", [node for node, _ in trace])
    for step, (node, frontier) in enumerate(trace, 1):
        print(step, "processed", node, "frontier", frontier)
