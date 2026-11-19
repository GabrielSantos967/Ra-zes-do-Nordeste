
from fastapi import APIRouter, Depends

from app.schemas.estoque import (
    MovimentacaoEstoqueRequest,
    MovimentacaoEstoqueResponse
)
from app.services.estoque import movimentar_estoque
from app.services.seguranca import exigir_perfil


router = APIRouter(prefix="/estoque", tags=["Estoque"])


@router.post(
    "/movimentacoes",
    response_model=MovimentacaoEstoqueResponse,
    status_code=201
)
def criar_movimentacao_estoque(
    dados: MovimentacaoEstoqueRequest,
    perfil=Depends(exigir_perfil("ADMINISTRADOR", "GERENTE", "FUNCIONARIO"))
):
    return movimentar_estoque(
        dados=dados,
        usuario_id=str(perfil["id"])
    )
