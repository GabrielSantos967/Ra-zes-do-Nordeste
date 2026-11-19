
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UnidadeResponse(BaseModel):
    id: int
    nome: str
    codigo: str
    endereco: str | None = None
    cidade: str | None = None
    estado: str | None = None
    ativa: bool
    criada_em: datetime

    model_config = ConfigDict(extra="ignore")
