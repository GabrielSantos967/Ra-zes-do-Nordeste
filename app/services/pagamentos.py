
from fastapi import HTTPException
from postgrest.exceptions import APIError

from app.schemas.pagamentos import PagamentoMockRequest
from app.repositories.pagamentos import processar_pagamento_mock


def realizar_pagamento_mock(dados: PagamentoMockRequest, cliente_id: str):
    try:
        resultado = processar_pagamento_mock(
            pedido_id=dados.pedido_id,
            cliente_id=cliente_id,
            aprovado=dados.aprovado
        )

        return resultado

    except APIError as erro:
        mensagem = erro.message

        if mensagem == "Pedido não encontrado.":
            raise HTTPException(status_code=404, detail=mensagem)

        if mensagem == "Você não tem permissão para pagar este pedido.":
            raise HTTPException(status_code=403, detail=mensagem)

        if mensagem in (
            "Este pedido não está aguardando pagamento.",
            "Este pedido já possui um pagamento processado."
        ):
            raise HTTPException(status_code=409, detail=mensagem)

        raise HTTPException(status_code=500, detail="Não foi possível processar o pagamento.")
