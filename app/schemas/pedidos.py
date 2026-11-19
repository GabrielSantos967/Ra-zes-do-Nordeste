
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class CanalPedido(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"


class StatusPedido(str, Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGAMENTO_APROVADO = "PAGAMENTO_APROVADO"
    EM_PREPARACAO = "EM_PREPARACAO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"
    PAGAMENTO_REJEITADO = "PAGAMENTO_REJEITADO"


class ItemPedidoRequest(BaseModel):
    produto_id: int = Field(gt=0)
    quantidade: int = Field(gt=0)


class CriarPedidoRequest(BaseModel):
    unidade_id: int = Field(gt=0)
    canal_pedido: CanalPedido
    itens: list[ItemPedidoRequest] = Field(min_length=1)
    observacoes: str | None = None


class ItemPedidoResponse(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    unidade_id: int
    canal_pedido: CanalPedido
    status: StatusPedido
    valor_total: Decimal
    itens: list[ItemPedidoResponse]


class AtualizarStatusPedidoRequest(BaseModel):
    status: StatusPedido


class AtualizarStatusPedidoResponse(BaseModel):
    pedido_id: int
    status_anterior: str
    status_atual: str
    mensagem: str
