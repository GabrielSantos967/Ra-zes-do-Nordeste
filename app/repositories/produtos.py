
from app.database.supabase import supabase


def listar_produtos():
    resposta = (
        supabase.table("produtos")
        .select("*")
        .order("nome")
        .execute()
    )

    return resposta.data
