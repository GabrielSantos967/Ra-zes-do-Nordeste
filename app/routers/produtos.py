
from fastapi import APIRouter, HTTPException

from app.schemas.produtos import ProdutoResponse
from app.services.produtos import obter_produtos


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
)


@router.get("/", response_model=list[ProdutoResponse])
def listar():
    try:
        return obter_produtos()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível consultar os produtos.",
        )
