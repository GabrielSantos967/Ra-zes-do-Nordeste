
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.database.supabase import supabase

from app.routers.unidades import router as unidades_router
from app.routers.produtos import router as produtos_router
from app.routers.cardapio import router as cardapio_router
from app.routers.auth import router as auth_router
from app.routers import pedidos
from app.routers import pagamentos
from app.routers import estoque
app = FastAPI(
    title="Raízes do Nordeste API",
    description=(
        "API para gerenciamento de pedidos e operações "
        "de uma rede de restaurantes."
    ),
    version="1.0.0",
)

@app.exception_handler(HTTPException)
async def tratar_erro_http(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": {
                "codigo": exc.status_code,
                "mensagem": exc.detail
            }
        },
        headers=exc.headers
    )


@app.exception_handler(RequestValidationError)
async def tratar_erro_validacao(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "erro": {
                "codigo": 422,
                "mensagem": "Dados inválidos na requisição."
            }
        }
    )


@app.exception_handler(Exception)
async def tratar_erro_inesperado(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "erro": {
                "codigo": 500,
                "mensagem": "Erro interno do servidor."
            }
        }
    )


app.include_router(unidades_router)
app.include_router(produtos_router)
app.include_router(cardapio_router)
app.include_router(auth_router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)
app.include_router(estoque.router)
@app.get("/")
def home():
    return {
        "mensagem": "API Raízes do Nordeste funcionando!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/health/supabase")
def supabase_health_check():
    try:
        supabase.table("unidades").select("id").limit(1).execute()

        return {
            "status": "ok",
            "banco": "Supabase conectado"
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível consultar o Supabase."
        )
