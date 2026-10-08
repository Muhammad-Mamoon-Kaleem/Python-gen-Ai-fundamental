class CurrentContextMemory:

    def __init__(self):
        self.context = {
            "project": None,
            "topic": None,
            "feature": None,
            "file": None,
            "bug": None,
            "goal": None,
            "framework": None,
            "language": None,
        }

    def set(self, key, value):
        if key in self.context:
            self.context[key] = value

    def get(self, key):
        return self.context.get(key)

    def get_all(self):
        return self.context

    def clear(self):
        for key in self.context:
            self.context[key] = None
