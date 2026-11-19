
from enum import Enum
from pydantic import BaseModel, Field


class TipoMovimentacao(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class MovimentacaoEstoqueRequest(BaseModel):
    unidade_id: int = Field(gt=0)
    produto_id: int = Field(gt=0)
    tipo: TipoMovimentacao
    quantidade: int = Field(gt=0)
    motivo: str = Field(min_length=1, max_length=255)


class MovimentacaoEstoqueResponse(BaseModel):
    movimentacao_id: int
    unidade_id: int
    produto_id: int
    tipo: TipoMovimentacao
    quantidade_movimentada: int
    estoque_anterior: int
    estoque_atual: int
    mensagem: str
