import json
import os

class MemoryJSON:
    def __init__(self, path="ia/memory/data.json"):
        self.path = path
        self.data = {
            "stats": {
                "wins": 0,
                "losses": 0
            },
            "strategy": {},
            "history": []
        }

        self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                try:
                    self.data = json.load(f)
                except:
                    pass  # mantém default

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)

    def record_event(self, event):
        self.data["history"].append(event)
        self.save()

    def update_strategy(self, rule, value):
        self.data["strategy"][rule] = value
        self.save()
