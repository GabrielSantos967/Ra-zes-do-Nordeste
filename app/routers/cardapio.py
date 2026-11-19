
from fastapi import APIRouter, HTTPException

from app.schemas.cardapio import ItemCardapioResponse
from app.services.cardapio import obter_cardapio_unidade


router = APIRouter(
    prefix="/unidades",
    tags=["Cardápio"],
)


@router.get(
    "/{unidade_id}/cardapio",
    response_model=list[ItemCardapioResponse],
)
def listar_cardapio(unidade_id: int):
    try:
        return obter_cardapio_unidade(unidade_id)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível consultar o cardápio da unidade.",
        )
