# ia/rl/dataset_mk11.py

import os
import json
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image

class MK11Dataset(Dataset):
    def __init__(self, data_dir="data/samples", cache_path="data/cache/processed.pt", use_cache=True):
        self.data_dir = data_dir
        self.cache_path = cache_path
        self.use_cache = use_cache

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])

        # se cache existe, carrega direto
        if use_cache and os.path.exists(cache_path):
            print("[DATASET] Carregando cache pré-processado...")
            cache = torch.load(cache_path)
            self.samples = cache["samples"]
            self.images = cache["images"]
            return

        # senão processa JSON
        print("[DATASET] Lendo JSONs...")
        self.samples = []
        self.images = []

        for fname in os.listdir(data_dir):
            if not fname.endswith(".json"):
                continue

            with open(os.path.join(data_dir, fname), "r") as f:
                data = json.load(f)

            frame = Image.open(data["frame_path"]).convert("RGB")
            tensor = self.transform(frame)

            self.samples.append({
                "state": data.get("state", "UNKNOWN"),
                "hp_player": data.get("hp_player", 1.0),
                "hp_enemy": data.get("hp_enemy", 1.0)
            })

            self.images.append(tensor)

        self.images = torch.stack(self.images)

        # salva cache
        if use_cache:
            print("[DATASET] Salvando cache para acelerar futuras execuções...")
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            torch.save({
                "samples": self.samples,
                "images": self.images
            }, cache_path)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        meta = self.samples[idx]
        img = self.images[idx]

        # transforma state → tensor numérico
        state_map = {
            "UNKNOWN": 0,
            "CHARACTER_SELECT": 1,
            "VERSUS": 2,
            "PRE_FIGHT": 3,
            "FIGHTING": 4,
            "ROUND_END": 5,
            "MATCH_END": 6
        }

        label = torch.tensor(state_map.get(meta["state"], 0), dtype=torch.long)

        extra = torch.tensor([
            meta["hp_player"],
            meta["hp_enemy"]
        ], dtype=torch.float32)

        return img, extra, label
