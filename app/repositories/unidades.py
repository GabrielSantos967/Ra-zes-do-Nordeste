
from app.database.supabase import supabase


def listar_unidades():
    resposta = (
        supabase.table("unidades")
        .select("*")
        .order("nome")
        .execute()
    )

    return resposta.data
