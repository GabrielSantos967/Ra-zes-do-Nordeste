
from app.database.supabase import supabase


def listar_cardapio_unidade(unidade_id: int):
    resposta = (
        supabase.table("cardapio_unidade")
        .select(
            "unidade_id, produto_id, preco, disponivel, atualizado_em, "
            "produtos(nome, descricao, categoria)"
        )
        .eq("unidade_id", unidade_id)
        .order("produto_id")
        .execute()
    )

    itens = []

    for registro in resposta.data:
        produto = registro.pop("produtos", None) or {}

        itens.append({
            **registro,
            "nome": produto.get("nome"),
            "descricao": produto.get("descricao"),
            "categoria": produto.get("categoria"),
        })

    return itens
