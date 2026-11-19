
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ItemCardapioResponse(BaseModel):
    unidade_id: int
    produto_id: int
    preco: Decimal
    disponivel: bool
    atualizado_em: datetime

    nome: str
    descricao: str | None = None
    categoria: str | None = None

    model_config = ConfigDict(extra="ignore")
