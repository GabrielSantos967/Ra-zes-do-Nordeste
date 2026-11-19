
from app.database.supabase import supabase


def registrar_movimentacao_estoque(
    unidade_id: int,
    produto_id: int,
    tipo: str,
    quantidade: int,
    motivo: str,
    usuario_id: str
):
    resposta = supabase.rpc(
        "movimentar_estoque",
        {
            "p_unidade_id": unidade_id,
            "p_produto_id": produto_id,
            "p_tipo": tipo,
            "p_quantidade": quantidade,
            "p_motivo": motivo,
            "p_usuario_id": usuario_id
        }
    ).execute()

    return resposta.data
