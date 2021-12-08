# Pármenas Haniel 2021

from typing import Optional


class Id:
    @property
    def id(self) -> int:
        return self._id


class Loja(Id):
    def __init__(self, id: int, porcentagem_frete: float) -> None:
        self._id = id
        self.porcentagem_frete = porcentagem_frete


class Motoboy(Id):
    def __init__(self, id: int, custo: float, exclusividades: Optional[list[Loja]] = []) -> None:
        self._id = id
        self._custo = custo
        self._exclusividades = exclusividades
        self._entregas = []

    def add_entrega(self, entrega: "Entrega"):
        "Vincula uma entrega ao motoboy"
        self._entregas.append(entrega)

    @property
    def custo(self) -> float:
        return self._custo

    @property
    def exclusividades(self) -> tuple[Loja]:
        return tuple(self._exclusividades)  # Retorna tupla pra evitar mutabilidade

    @property
    def tem_exclusividade(self) -> bool:
        return True if self._exclusividades else False

    @property
    def entregas(self) -> tuple["Entrega"]:
        return tuple(self._entregas)  # Retorna tupla pra evitar mutabilidade

    @property
    def valor_ganho_fretes(self) -> float:
        valor = 0.0
        for e in self._entregas:
            valor += e.valor_frete
        return valor


class Pedido(Id):
    def __init__(self, loja: Loja, valor_pedido: float) -> None:
        self._id = None
        self._loja = loja
        self._valor_pedido = valor_pedido

    @property
    def valor_pedido(self) -> float:
        return self._valor_pedido

    @property
    def loja(self) -> Loja:
        return self._loja


class Entrega(Id):
    def __init__(self, id: int, pedido: Pedido, motoboy: Motoboy) -> None:
        self._id = id
        self._pedido = pedido
        self._motoboy = motoboy

    @property
    def motoboy(self) -> Motoboy:
        return self._motoboy

    @property
    def pedido(self) -> Pedido:
        return self._pedido

    @property
    def loja(self) -> Loja:
        return self.pedido.loja

    @property
    def valor_frete(self) -> float:
        return self._motoboy.custo + (self._pedido.valor_pedido * self._pedido.loja.porcentagem_frete)

    @property
    def valor_total(self) -> float:
        return self.valor_frete + self._pedido.valor_pedido
