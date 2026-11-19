
from app.database.supabase import supabase


def processar_pagamento_mock(pedido_id: int, cliente_id: str, aprovado: bool):
    resposta = supabase.rpc("processar_pagamento_mock", {
        "p_pedido_id": pedido_id,
        "p_cliente_id": cliente_id,
        "p_aprovado": aprovado
    }).execute()

    return resposta.data
