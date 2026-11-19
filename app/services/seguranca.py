
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import AuthApiError

from app.database.supabase import supabase
from app.database.supabase import criar_cliente_auth

esquema_autenticacao = HTTPBearer(auto_error=False)


def obter_usuario_atual(credenciais: HTTPAuthorizationCredentials | None = Depends(esquema_autenticacao)):
    if credenciais is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não informado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        cliente_auth = criar_cliente_auth()
        resposta = cliente_auth.auth.get_user(credenciais.credentials)

        if resposta.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return resposta.user

    except AuthApiError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def obter_perfil_usuario(usuario = Depends(obter_usuario_atual)):
    resposta = supabase.table("perfis_usuario").select("id, nome, perfil, ativo").eq("id", str(usuario.id)).maybe_single().execute()

    if resposta.data is None:
        raise HTTPException(
            status_code=403,
            detail="Usuário não possui perfil de acesso cadastrado.",
        )

    if not resposta.data["ativo"]:
        raise HTTPException(
            status_code=403,
            detail="Usuário está inativo.",
        )

    return resposta.data


def exigir_perfil(*perfis_permitidos: str):
    def verificar_permissao(perfil = Depends(obter_perfil_usuario)):
        if perfil["perfil"] not in perfis_permitidos:
            raise HTTPException(
                status_code=403,
                detail="Você não possui permissão para acessar este recurso.",
            )

        return perfil

    return verificar_permissao

