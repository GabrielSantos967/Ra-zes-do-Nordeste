import logging

from fastapi import HTTPException
from supabase import AuthApiError

from app.database.supabase import criar_cliente_auth, supabase


logger = logging.getLogger(__name__)


def cadastrar_usuario(email: str, senha: str):
    cliente_auth = criar_cliente_auth()

    try:
        resposta = cliente_auth.auth.sign_up({
            "email": email,
            "password": senha,
        })

        if resposta.user is None:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível cadastrar o usuário.",
            )

        return {
            "mensagem": (
                "Cadastro realizado. Verifique seu e-mail "
                "se a confirmação estiver habilitada."
            ),
            "usuario_id": str(resposta.user.id),
            "email": resposta.user.email,
        }

    except AuthApiError:
        logger.warning("Falha no cadastro de usuário no Supabase Auth.")

        raise HTTPException(
            status_code=400,
            detail="Não foi possível cadastrar o usuário.",
        )


def fazer_login(email: str, senha: str):
    try:
        cliente_auth = criar_cliente_auth()

        resposta = cliente_auth.auth.sign_in_with_password({
            "email": email,
            "password": senha,
        })

        if resposta.session is None or resposta.user is None:
            raise HTTPException(
                status_code=401,
                detail=(
                    "Não foi possível autenticar. "
                    "Verifique suas credenciais e a confirmação do e-mail."
                ),
            )

    except AuthApiError:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos, ou usuário ainda não confirmado.",
        )

    usuario_id = str(resposta.user.id)

    try:
        supabase.table("logs_auditoria").insert({
            "usuario_id": usuario_id,
            "acao": "LOGIN_SUCESSO",
            "entidade": "USUARIO",
            "entidade_id": usuario_id,
            "descricao": "Usuário autenticado com sucesso.",
        }).execute()

    except Exception:
        logger.exception(
            "Falha ao registrar auditoria de login para o usuário %s.",
            usuario_id,
        )

    return {
        "access_token": resposta.session.access_token,
        "token_type": "bearer",
    }