# ia/dataset/live_dataset_builder.py

import os
import time
import json
from pathlib import Path


class LiveDatasetBuilder:
    """
    Builder para dataset YOLO em tempo real sem salvar frames.
    Apenas salva labels e metadados para posterior reconstrução.
    """

    def __init__(self, base_dir="dataset", classes=None, autosplit=True):
        self.base_dir = Path(base_dir)
        self.autosplit = autosplit

        self.classes = classes or [
            "fighter_1",
            "fighter_2",
            "projectile"
        ]

        self.index_file = self.base_dir / "index.json"
        self._dataset_index = []
        self.frame_idx = 0

        self._setup_structure()


    def _setup_structure(self):
        (self.base_dir / "labels" / "train").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "labels" / "val").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "labels" / "test").mkdir(parents=True, exist_ok=True)

        if not self.index_file.exists():
            with open(self.index_file, "w") as f:
                json.dump([], f)


    def _write_index(self):
        with open(self.index_file, "w") as f:
            json.dump(self._dataset_index, f, indent=2)


    def add_frame(self, detections, split=None):
        """
        Recebe deteções no formato:
        [
          { "cls": 0, "bbox": [cx, cy, w, h] }, ...
        ]
        Normalizado para YOLO (0..1)
        """

        if split is None and self.autosplit:
            # split simples: 85% train, 10% val, 5% test
            r = self.frame_idx % 100
            if r < 85: split = "train"
            elif r < 95: split = "val"
            else: split = "test"
        elif split is None:
            split = "train"

        label_path = self.base_dir / "labels" / split / f"{self.frame_idx:06d}.txt"

        with open(label_path, "w") as f:
            for d in detections:
                cls = d["cls"]
                x, y, w, h = d["bbox"]
                f.write(f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

        self._dataset_index.append({
            "id": self.frame_idx,
            "split": split,
            "timestamp": time.time(),
            "detections": detections
        })

        self.frame_idx += 1
        self._write_index()


    def get_classes_yaml(self):
        """
        Cria conteúdo do dataset.yaml para treinar YOLO
        """
        return {
            "path": str(self.base_dir),
            "train": "labels/train",
            "val": "labels/val",
            "test": "labels/test",
            "names": self.classes
        }
