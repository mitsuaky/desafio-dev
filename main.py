# Pármenas Haniel 2021

from operator import attrgetter
from typing import Optional

from classes.classes import Entrega, Loja, Motoboy, Pedido


class App():

    def __init__(self) -> None:
        "Inicializa um \"protótipo\" simples de um app de entregas"
        self._lojas: Optional[list[Loja]] = []
        self._motoboys: Optional[list[Motoboy]] = []
        self._pedidos: Optional[list[Pedido]] = []
        self._entregas: Optional[list[Entrega]] = []

    def add_loja(self, loja: Loja):
        "Adiciona uma loja"
        self._lojas.append(loja)

    def get_loja(self, id: int):
        "Retorna a loja com o ID passado nos argumentos"
        for loja in self._lojas:
            if loja.id == id:
                return loja

    def add_motoboy(self, motoboy: Motoboy):
        "Adiciona um motoboy"
        self._motoboys.append(motoboy)

    def add_pedido(self, pedido: Pedido):
        "Adiciona um pedido"
        if pedido.id == None:
            pedido.id == len(self._pedidos)  # Pseudo gerador de ID
        self._pedidos.append(pedido)

    def _add_entrega(self, pedido: Pedido, motoboy: Motoboy):
        n = len(self._entregas)  # Pseudo gerador de ID
        entrega = Entrega(n, pedido, motoboy)
        self._entregas.append(entrega)
        motoboy.add_entrega(entrega)

    def _gerar_entregas_prioridade(self, motoboy: Motoboy, pedidos: list[Pedido], limite):
        pedidos_priorizados = [x for x in pedidos if x.loja in motoboy.exclusividades]
        # "Limita" a quantidade de entregas por motoboy para tentar deixar uniforme entre todos eles.
        for pedido in pedidos_priorizados[:limite]:
            self._add_entrega(pedido, motoboy)
            pedidos.remove(pedido)  # Remove o pedido da lista `pedidos_nao_processados`

    def _gerar_entregas_normais(self, motoboy: Motoboy, pedidos: list[Pedido], limite):
        for pedido in pedidos[:limite]:
            self._add_entrega(pedido, motoboy)
            pedidos.remove(pedido)

    def gerar_entregas(self):
        "Gera as ordens de entrega vinculando os pedidos aos motoboys."
        avarage = round(len(self._pedidos) / len(self._motoboys))  # Média de entregas por motoboy
        pedidos_nao_processados = list(self._pedidos)  # Retorna uma nova lista pra não modificar a da classe

        while pedidos_nao_processados:

            # Sorted retorna a lista de motoboys colocando quem tem exclusividade na frente.
            for motoboy in sorted(self._motoboys, key=attrgetter('tem_exclusividade'), reverse=True):
                if motoboy.tem_exclusividade:
                    self._gerar_entregas_prioridade(motoboy, pedidos_nao_processados, avarage)
                else:
                    self._gerar_entregas_normais(motoboy, pedidos_nao_processados, avarage)

    def get_motoboys(self) -> tuple[Motoboy]:
        "Retorna todos os motoboys em uma tupla"
        return tuple(self._motoboys)

    def get_motoboy(self, motoboy_id: Optional[int] = None) -> Optional[Motoboy]:
        "Retorna o motoboy com o ID passado nos argumentos"
        for motoboy in self._motoboys:
            if motoboy.id == motoboy_id:
                return motoboy


def print_motoboy_stats(motoboy: Motoboy):
    print('ID Motoboy:', motoboy.id)
    print(' ∟ Num Entregas:', len(motoboy.entregas))
    print(' ∟ Entregas:')
    for entrega in motoboy.entregas:
        print(f"   ∟ ID Loja: {entrega.loja.id}, Valor frete: {entrega.valor_frete}")
    print(' ∟ Total ganho:', motoboy.valor_ganho_fretes)


if __name__ == "__main__":

    app = App()

    app.add_loja(Loja(1, 0.05))
    app.add_loja(Loja(2, 0.05))
    app.add_loja(Loja(3, 0.15))

    app.add_motoboy(Motoboy(1, 2.0))
    app.add_motoboy(Motoboy(2, 2.0))
    app.add_motoboy(Motoboy(3, 2.0))
    app.add_motoboy(Motoboy(4, 2.0, [app.get_loja(1)]))
    app.add_motoboy(Motoboy(5, 3.0))

    app.add_pedido(Pedido(app.get_loja(1), 50.0))
    app.add_pedido(Pedido(app.get_loja(1), 50.0))
    app.add_pedido(Pedido(app.get_loja(1), 50.0))

    app.add_pedido(Pedido(app.get_loja(2), 50.0))
    app.add_pedido(Pedido(app.get_loja(2), 50.0))
    app.add_pedido(Pedido(app.get_loja(2), 50.0))
    app.add_pedido(Pedido(app.get_loja(2), 50.0))

    app.add_pedido(Pedido(app.get_loja(3), 50.0))
    app.add_pedido(Pedido(app.get_loja(3), 50.0))
    app.add_pedido(Pedido(app.get_loja(3), 100.0))

    app.gerar_entregas()

    try:
        id = input("Qual o ID do motoboy no qual deseja verificar as entregas? (não especificar mostra de todos): ")

        if id:
            motoboy = app.get_motoboy(int(id))
            print_motoboy_stats(motoboy)
        else:
            motoboys = app.get_motoboys()
            for motoboy in motoboys:
                print_motoboy_stats(motoboy)

    except (EOFError, KeyboardInterrupt):  # Usuário encerrou o script
        print("\nPrograma encerrado.")
