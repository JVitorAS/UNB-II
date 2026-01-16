import json
import torch
import os

DATA_DIR = "data"
OUTPUT_DIR = "preprocessed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def salvar_json_como_tensor(json_file, tensor_file):
    """
    Lê JSON, transforma em tensor e salva como .pt
    """
    # 1️⃣ Carrega os dados do JSON
    with open(os.path.join(DATA_DIR, json_file), "r", encoding="utf8") as f:
        data = json.load(f)

    # 2️⃣ Transforma em lista de features
    # Aqui assumo que cada item do JSON é um dict com valores numéricos
    features = []
    for item in data:
        # Pega apenas valores numéricos, ignora strings
        feat = [v for v in item.values() if isinstance(v, (int, float))]
        features.append(feat)

    # 3️⃣ Converte para tensor PyTorch
    tensor = torch.tensor(features, dtype=torch.float32)

    # 4️⃣ Salva em .pt
    torch.save(tensor, os.path.join(OUTPUT_DIR, tensor_file))
    print(f"[PyTorch] Tensor salvo: {os.path.join(OUTPUT_DIR, tensor_file)}")
    print(f"[PyTorch] Forma do tensor: {tensor.shape}")

# Exemplo de uso
salvar_json_como_tensor("characters.json", "characters.pt")
