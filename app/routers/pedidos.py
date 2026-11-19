
from fastapi import APIRouter, Depends

from app.schemas.pedidos import CriarPedidoRequest
from app.services.pedidos import criar_pedido
from app.services.seguranca import obter_usuario_atual
from app.schemas.pedidos import AtualizarStatusPedidoRequest, AtualizarStatusPedidoResponse
from app.services.pedidos import alterar_status_pedido
from app.services.seguranca import exigir_perfil
from fastapi import Query
from app.schemas.pedidos import CanalPedido, StatusPedido
from app.services.pedidos import listar_pedidos
from app.services.seguranca import obter_perfil_usuario
from app.services.pedidos import cancelar_pedido_cliente

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("", status_code=201)
def cadastrar_pedido(dados: CriarPedidoRequest, usuario = Depends(obter_usuario_atual)):
    return criar_pedido(dados=dados, cliente_id=str(usuario.id))


@router.patch("/{pedido_id}/status", response_model=AtualizarStatusPedidoResponse)
def atualizar_andamento_pedido(
    pedido_id: int,
    dados: AtualizarStatusPedidoRequest,
    perfil=Depends(exigir_perfil("FUNCIONARIO", "GERENTE", "ADMINISTRADOR"))
):
    return alterar_status_pedido(
        pedido_id=pedido_id,
        novo_status=dados.status.value,
        usuario_id=str(perfil["id"])
    )



@router.get("")
def consultar_lista_pedidos(
    canalPedido: CanalPedido | None = None,
    statusPedido: StatusPedido | None = None,
    pagina: int = Query(default=1, ge=1),
    limite: int = Query(default=10, ge=1, le=100),
    perfil=Depends(obter_perfil_usuario)
):
    return listar_pedidos(
        perfil_usuario=perfil,
        canal_pedido=canalPedido.value if canalPedido else None,
        status_pedido=statusPedido.value if statusPedido else None,
        pagina=pagina,
        limite=limite
    )


@router.post("/{pedido_id}/cancelar")
def cancelar_pedido(
    pedido_id: int,
    usuario=Depends(obter_usuario_atual)
):
    return cancelar_pedido_cliente(
        pedido_id=pedido_id,
        cliente_id=str(usuario.id)
    )
