"""Small checks for the stateful classroom policy."""
from lab2_model import StatefulClassroomAgent


def run_check(percepts):
    agent = StatefulClassroomAgent()
    rows = []
    for percept in percepts:
        previous, target, send = agent.act(*percept)
        rows.append((previous, percept, target, send))
    return rows


checks = {
    "repeated_cool": [(29, True), (29, True)],
    "boundaries": [(20, True), (26, True)],
    "transition": [(29, True), (19, True)],
    "empty_priority": [(29, False)],
}

for name, percepts in checks.items():
    print(name)
    for row in run_check(percepts):
        print(row)
