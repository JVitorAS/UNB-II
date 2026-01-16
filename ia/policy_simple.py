import random
import time
import os
import json

LAST_ACTION_TIME = 0
ACTION_COOLDOWN = 0.18

DATA_DIR = "data"

class MKPolicyJSON:

    def __init__(self):
        self.character = None
        self.moves = {}
        self.combos = []

    def select_character(self, name=None):
        with open(os.path.join(DATA_DIR, "characters.json"), "r", encoding="utf8") as f:
            data = json.load(f)

        if name:
            chars = [c for c in data if c["name"].lower() == name.lower()]
            if not chars:
                raise Exception(f"Personagem '{name}' não encontrado.")
            chosen = chars[0]
        else:
            chosen = random.choice(data)

        self.character = chosen["name"]

        with open(os.path.join(DATA_DIR, chosen["file"]), "r", encoding="utf8") as f:
            pdata = json.load(f)

        self.moves = pdata.get("moves", {})
        self.combos = pdata.get("combos", [])

        print(f"[AI] Personagem escolhido: {self.character}")
        print(f"[DB] {len(self.combos)} combos carregados.")

    def choose_action(self, state):
        global LAST_ACTION_TIME

        if not self.character:
            self.select_character()

        hp_player = state.get("hp_player", 1.0)
        hp_enemy  = state.get("hp_enemy", 1.0)

        now = time.time()
        if now - LAST_ACTION_TIME < ACTION_COOLDOWN:
            return None
        LAST_ACTION_TIME = now

        normals = self.moves.get("normals", [])
        defense = self.moves.get("defense", ["block", "jump"])

        # finalização
        if hp_enemy < 0.25:
            finishers = [c for c in self.combos if c["damage"] >= 200]
            if finishers:
                combo = random.choice(finishers)
                return combo["inputs"]

        # defesa
        if hp_player < 0.25:
            return random.choice(defense)

        r = random.random()

        if r < 0.45 and normals:
            return random.choice(normals)

        if r < 0.70 and self.combos:
            combo = random.choice(self.combos)
            return combo["inputs"]

        return "jump"
