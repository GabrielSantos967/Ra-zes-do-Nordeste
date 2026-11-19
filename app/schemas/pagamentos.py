
from decimal import Decimal
from pydantic import BaseModel, Field


class PagamentoMockRequest(BaseModel):
    pedido_id: int = Field(gt=0)
    aprovado: bool


class PagamentoMockResponse(BaseModel):
    pagamento_id: int
    pedido_id: int
    valor: Decimal
    status_pagamento: str
    status_pedido: str
