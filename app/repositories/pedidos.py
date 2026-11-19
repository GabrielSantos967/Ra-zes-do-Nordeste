
from app.database.supabase import supabase


def buscar_unidade(unidade_id: int):
    resposta = supabase.table("unidades").select("*").eq("id", unidade_id).limit(1).execute()
    return resposta.data[0] if resposta.data else None


def buscar_produto(produto_id: int):
    resposta = supabase.table("produtos").select("id, nome, ativo").eq("id", produto_id).limit(1).execute()
    return resposta.data[0] if resposta.data else None


def buscar_produto_cardapio(unidade_id: int, produto_id: int):
    resposta = supabase.table("cardapio_unidade").select("unidade_id, produto_id, preco, disponivel").eq("unidade_id", unidade_id).eq("produto_id", produto_id).limit(1).execute()
    return resposta.data[0] if resposta.data else None


def buscar_estoque(unidade_id: int, produto_id: int):
    resposta = supabase.table("estoque_unidade").select("unidade_id, produto_id, quantidade").eq("unidade_id", unidade_id).eq("produto_id", produto_id).limit(1).execute()
    return resposta.data[0] if resposta.data else None


def criar_pedido_transacional(cliente_id: str, unidade_id: int, canal_pedido: str, itens: list, observacoes: str | None = None):
    resposta = supabase.rpc("criar_pedido_transacional", {
        "p_cliente_id": cliente_id,
        "p_unidade_id": unidade_id,
        "p_canal_pedido": canal_pedido,
        "p_itens": itens,
        "p_observacoes": observacoes
    }).execute()

    return resposta.data


def atualizar_status_pedido(pedido_id: int, usuario_id: str, novo_status: str):
    resposta = supabase.rpc("atualizar_status_pedido", {
        "p_pedido_id": pedido_id,
        "p_usuario_id": usuario_id,
        "p_novo_status": novo_status
    }).execute()

    return resposta.data



def consultar_pedidos(
    cliente_id: str | None = None,
    canal_pedido: str | None = None,
    status_pedido: str | None = None,
    pagina: int = 1,
    limite: int = 10
):
    inicio = (pagina - 1) * limite
    fim = inicio + limite - 1

    consulta = supabase.table("pedidos").select(
        "id, cliente_id, unidade_id, canal_pedido, status, valor_total, observacoes",
        count="exact"
    )

    if cliente_id is not None:
        consulta = consulta.eq("cliente_id", cliente_id)

    if canal_pedido is not None:
        consulta = consulta.eq("canal_pedido", canal_pedido)

    if status_pedido is not None:
        consulta = consulta.eq("status", status_pedido)

    resposta = (
        consulta
        .order("id", desc=True)
        .range(inicio, fim)
        .execute()
    )

    return {
        "pagina": pagina,
        "limite": limite,
        "total": resposta.count or 0,
        "pedidos": resposta.data or []
    }



def cancelar_pedido_transacional(pedido_id: int, cliente_id: str):
    resposta = supabase.rpc("cancelar_pedido", {
        "p_pedido_id": pedido_id,
        "p_cliente_id": cliente_id
    }).execute()

    return resposta.data
