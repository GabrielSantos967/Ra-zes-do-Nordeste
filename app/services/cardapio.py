
from app.repositories.cardapio import listar_cardapio_unidade


def obter_cardapio_unidade(unidade_id: int):
    return listar_cardapio_unidade(unidade_id)
