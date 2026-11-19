
from fastapi import APIRouter, Depends

from app.schemas.pagamentos import PagamentoMockRequest, PagamentoMockResponse
from app.services.pagamentos import realizar_pagamento_mock
from app.services.seguranca import obter_usuario_atual


router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.post("/mock", response_model=PagamentoMockResponse, status_code=201)
def pagar_pedido_mock(dados: PagamentoMockRequest, usuario=Depends(obter_usuario_atual)):
    return realizar_pagamento_mock(dados=dados, cliente_id=str(usuario.id))
