
from fastapi import HTTPException
from postgrest.exceptions import APIError

from app.schemas.estoque import MovimentacaoEstoqueRequest
from app.repositories.estoque import registrar_movimentacao_estoque


def movimentar_estoque(dados: MovimentacaoEstoqueRequest, usuario_id: str):
    try:
        return registrar_movimentacao_estoque(
            unidade_id=dados.unidade_id,
            produto_id=dados.produto_id,
            tipo=dados.tipo.value,
            quantidade=dados.quantidade,
            motivo=dados.motivo.strip(),
            usuario_id=usuario_id
        )

    except APIError as erro:
        mensagem = erro.message or ""

        if mensagem == "Usuário não possui permissão para movimentar estoque.":
            raise HTTPException(status_code=403, detail=mensagem)

        if mensagem == "Estoque não encontrado para a unidade e produto informados.":
            raise HTTPException(status_code=404, detail=mensagem)

        if mensagem == "Estoque insuficiente para realizar a saída.":
            raise HTTPException(status_code=409, detail=mensagem)

        if mensagem in (
            "Tipo de movimentação inválido.",
            "A quantidade deve ser maior que zero.",
            "O motivo da movimentação é obrigatório."
        ):
            raise HTTPException(status_code=400, detail=mensagem)

        raise HTTPException(
            status_code=500,
            detail="Não foi possível realizar a movimentação de estoque."
        )
