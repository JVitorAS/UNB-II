class StateMachine:
    def __init__(self):
        self.current = None
        self.last = None

    def update(self, new_state):
        self.last = self.current
        self.current = new_state

    def changed(self):
        return self.current != self.last
