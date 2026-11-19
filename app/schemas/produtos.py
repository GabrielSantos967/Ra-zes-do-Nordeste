
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None = None
    categoria: str | None = None
    ativo: bool
    criado_em: datetime

    model_config = ConfigDict(extra="ignore")
