
from decimal import Decimal
from fastapi import HTTPException

from app.schemas.pedidos import CriarPedidoRequest
from app.repositories.pedidos import buscar_unidade, buscar_produto, buscar_produto_cardapio, buscar_estoque, criar_pedido_transacional

from postgrest.exceptions import APIError
from app.repositories.pedidos import atualizar_status_pedido
from app.repositories.pedidos import consultar_pedidos
from app.repositories.pedidos import cancelar_pedido_transacional

def preparar_pedido(dados: CriarPedidoRequest):
    unidade = buscar_unidade(dados.unidade_id)

    if unidade is None:
        raise HTTPException(status_code=404, detail="Unidade não encontrada.")

    quantidades = {}

    for item in dados.itens:
        quantidades[item.produto_id] = quantidades.get(item.produto_id, 0) + item.quantidade

    itens_preparados = []
    valor_total = Decimal("0.00")

    for produto_id, quantidade in quantidades.items():
        produto = buscar_produto(produto_id)

        if produto is None:
            raise HTTPException(status_code=404, detail=f"Produto {produto_id} não encontrado.")

        if not produto["ativo"]:
            raise HTTPException(status_code=400, detail=f"Produto {produto_id} está inativo.")

        cardapio = buscar_produto_cardapio(dados.unidade_id, produto_id)

        if cardapio is None or not cardapio["disponivel"]:
            raise HTTPException(status_code=400, detail=f"Produto {produto_id} não está disponível nesta unidade.")

        estoque = buscar_estoque(dados.unidade_id, produto_id)

        if estoque is None or estoque["quantidade"] < quantidade:
            raise HTTPException(status_code=409, detail=f"Estoque insuficiente para o produto {produto_id}.")

        preco_unitario = Decimal(str(cardapio["preco"]))
        subtotal = preco_unitario * quantidade
        valor_total += subtotal

        itens_preparados.append({
            "produto_id": produto_id,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
            "subtotal": subtotal
        })

    return {
        "unidade_id": dados.unidade_id,
        "canal_pedido": dados.canal_pedido.value,
        "status": "AGUARDANDO_PAGAMENTO",
        "valor_total": valor_total,
        "observacoes": dados.observacoes,
        "itens": itens_preparados
    }


def criar_pedido(dados: CriarPedidoRequest, cliente_id: str):
    pedido_preparado = preparar_pedido(dados)

    itens = [
        {
            "produto_id": item["produto_id"],
            "quantidade": item["quantidade"]
        }
        for item in pedido_preparado["itens"]
    ]

    pedido_id = criar_pedido_transacional(
        cliente_id=cliente_id,
        unidade_id=pedido_preparado["unidade_id"],
        canal_pedido=pedido_preparado["canal_pedido"],
        itens=itens,
        observacoes=pedido_preparado["observacoes"]
    )

    return {
        "id": pedido_id,
        "mensagem": "Pedido criado com sucesso.",
        "status": "AGUARDANDO_PAGAMENTO"
    }


def alterar_status_pedido(pedido_id: int, novo_status: str, usuario_id: str):
    try:
        return atualizar_status_pedido(
            pedido_id=pedido_id,
            usuario_id=usuario_id,
            novo_status=novo_status
        )

    except APIError as erro:
        mensagem = erro.message

        if mensagem == "Pedido não encontrado.":
            raise HTTPException(status_code=404, detail=mensagem)

        if mensagem in (
            "Usuário não encontrado ou inativo.",
            "Usuário não possui permissão para atualizar pedidos."
        ):
            raise HTTPException(status_code=403, detail=mensagem)

        if mensagem.startswith("Transição de status inválida:"):
            raise HTTPException(status_code=409, detail=mensagem)

        raise HTTPException(status_code=500, detail="Não foi possível atualizar o status do pedido.")



def listar_pedidos(
    perfil_usuario: dict,
    canal_pedido: str | None = None,
    status_pedido: str | None = None,
    pagina: int = 1,
    limite: int = 10
):
    perfil = perfil_usuario["perfil"]

    if perfil == "CLIENTE":
        cliente_id = str(perfil_usuario["id"])

    elif perfil in ("ADMINISTRADOR", "GERENTE", "FUNCIONARIO"):
        cliente_id = None

    else:
        raise HTTPException(
            status_code=403,
            detail="Você não possui permissão para consultar pedidos."
        )

    try:
        return consultar_pedidos(
            cliente_id=cliente_id,
            canal_pedido=canal_pedido,
            status_pedido=status_pedido,
            pagina=pagina,
            limite=limite
        )

    except APIError:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível consultar os pedidos."
        )


def cancelar_pedido_cliente(pedido_id: int, cliente_id: str):
    try:
        return cancelar_pedido_transacional(
            pedido_id=pedido_id,
            cliente_id=cliente_id
        )

    except APIError as erro:
        mensagem = erro.message

        if mensagem == "Pedido não encontrado.":
            raise HTTPException(status_code=404, detail=mensagem)

        if mensagem == "Você não tem permissão para cancelar este pedido.":
            raise HTTPException(status_code=403, detail=mensagem)

        if mensagem == "Este pedido não pode mais ser cancelado.":
            raise HTTPException(status_code=409, detail=mensagem)

        raise HTTPException(
            status_code=500,
            detail="Não foi possível cancelar o pedido."
        )
