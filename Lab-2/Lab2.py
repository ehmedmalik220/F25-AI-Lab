"""Lab 2: a stateful smart-classroom agent."""

class ClassroomAgent:
    def __init__(self):
        self.previous_mode = None

    def target_mode(self, temperature, occupied):
        if not occupied:
            return "ECO"
        if temperature > 26:
            return "COOL"
        if temperature < 20:
            return "WARM"
        return "IDLE"

    def act(self, temperature, occupied):
        target = self.target_mode(temperature, occupied)
        send_command = target != self.previous_mode
        previous = self.previous_mode
        self.previous_mode = target
        return previous, target, send_command

agent = ClassroomAgent()
percepts = [(29, True), (29, True), (20, True), (26, True),
            (19, True), (29, False), (29, False)]
print("step | previous | percept | target | command")
for step, percept in enumerate(percepts, 1):
    previous, target, command = agent.act(*percept)
    print(step, previous, percept, target,
          "SEND" if command else "NO_COMMAND", sep=" | ")
