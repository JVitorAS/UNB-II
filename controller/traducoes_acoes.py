from enum import IntEnum


class Acao(IntEnum):
    DEFENDER = 0
    AVANCAR = 1
    RECUAR = 2
    ATAQUE_LEVE = 3
    ANTI_AIR = 4
    ATAQUE_MEDIO = 5
    ATAQUE_PESADO = 6
    AGACHAR = 7
    PULAR = 8


# Mapa de ações abstratas → descrição lógica
MAPA_ACOES = {
    Acao.DEFENDER: {
        "tipo": "segurar",
        "comandos": ["BLOCK"],
        "duracao_frames": 10
    },

    Acao.AVANCAR: {
        "tipo": "movimento",
        "comandos": ["RIGHT"],
        "duracao_frames": 5
    },

    Acao.RECUAR: {
        "tipo": "movimento",
        "comandos": ["LEFT"],
        "duracao_frames": 5
    },

    Acao.ATAQUE_LEVE: {
        "tipo": "ataque",
        "comandos": ["BTN_X"],
        "duracao_frames": 3
    },

    Acao.ANTI_AIR: {
        "tipo": "ataque",
        "comandos": ["DOWN", "BTN_Y"],
        "duracao_frames": 4
    },

    Acao.ATAQUE_MEDIO: {
        "tipo": "ataque",
        "comandos": ["BTN_Y"],
        "duracao_frames": 4
    },

    Acao.ATAQUE_PESADO: {
        "tipo": "ataque",
        "comandos": ["BTN_B"],
        "duracao_frames": 6
    },

    Acao.AGACHAR: {
        "tipo": "movimento",
        "comandos": ["DOWN"],
        "duracao_frames": 5
    },

    Acao.PULAR: {
        "tipo": "movimento",
        "comandos": ["UP"],
        "duracao_frames": 8
    }
}


def traduzir_acao(acao_id: int) -> dict:
    """
    Recebe a ação da IA (int)
    Retorna um dicionário descrevendo o comando
    """

    try:
        acao = Acao(acao_id)
    except ValueError:
        acao = Acao.DEFENDER  

    return MAPA_ACOES[acao]
