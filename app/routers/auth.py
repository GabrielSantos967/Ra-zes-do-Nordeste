
from fastapi import APIRouter, Depends

from app.schemas.auth import CadastroRequest, LoginRequest
from app.services.auth import cadastrar_usuario, fazer_login
from app.services.seguranca import obter_usuario_atual
from app.services.seguranca import obter_usuario_atual, exigir_perfil


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post("/cadastro", status_code=201)
def cadastro(dados: CadastroRequest):
    return cadastrar_usuario(
        email=dados.email,
        senha=dados.senha,
    )


@router.post("/login")
def login(dados: LoginRequest):
    return fazer_login(
        email=dados.email,
        senha=dados.senha,
    )


@router.get("/me")
def meu_perfil(usuario = Depends(obter_usuario_atual)):
    return {
        "id": str(usuario.id),
        "email": usuario.email,
        "mensagem": "Usuário autenticado com sucesso.",
    }



@router.get("/admin",responses={401: {"description": "Token ausente, inválido ou expirado."},403: {"description": "Usuário sem permissão ou perfil inativo."},},)

def area_administrativa(perfil = Depends(exigir_perfil("ADMINISTRADOR"))):
    return {
        "mensagem": "Acesso administrativo autorizado.",
        "usuario": perfil["nome"],
        "perfil": perfil["perfil"],
    }
