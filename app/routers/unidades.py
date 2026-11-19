
from fastapi import APIRouter, HTTPException

from app.schemas.unidades import UnidadeResponse
from app.services.unidades import obter_unidades


router = APIRouter(
    prefix="/unidades",
    tags=["Unidades"],
)


@router.get("/", response_model=list[UnidadeResponse])
def listar():
    try:
        return obter_unidades()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível consultar as unidades.",
        )
