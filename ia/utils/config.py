import json
import os

CONFIG_PATH = "mk11_config.json"

# Valores default adequados para Mortal Kombat 11
DEFAULT_CONFIG = {
    "monitor": None,  # ID do monitor (caso use multi-display)
    
    # Regiões de leitura do HUD (x, y, w, h)
    "hp_player_rect": [180, 78, 340, 28],
    "hp_enemy_rect": [1320, 78, 340, 28],

    # HSV padrão para barras de HP no MK11 (amarelo-esverdeado)
    "hp_hsv_lower": [22, 140, 140],
    "hp_hsv_upper": [80, 255, 255],

    # Futuro: adicionáveis
    "track_stamina": True,
    "track_fatal_blow": True,

    # Mostra prints e overlays se o modo estiver ligado
    "debug": True
}


def ensure_config_exists():
    """
    Cria o arquivo de configuração se não existir.
    """
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print(f"[MK11 CONFIG] Arquivo criado com padrão em {CONFIG_PATH}")
        return DEFAULT_CONFIG
    return None


def load_config():
    """
    Carrega mk11_config.json e preenche valores faltantes.
    """
    ensure_config_exists()

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception as e:
        print(f"[MK11 CONFIG] Erro ao carregar config: {e}")
        cfg = DEFAULT_CONFIG.copy()

    # Preenche possíveis chaves ausentes
    for key, value in DEFAULT_CONFIG.items():
        cfg.setdefault(key, value)

    return cfg


def save_config(cfg):
    """
    Salva configurações de volta para o arquivo.
    """
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
        print("[MK11 CONFIG] Configurações salvas.")
    except Exception as e:
        print(f"[MK11 CONFIG] Erro ao salvar config: {e}")


if __name__ == "__main__":
    cfg = load_config()
    print(json.dumps(cfg, indent=4))
