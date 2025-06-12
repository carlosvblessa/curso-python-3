# modelos/cardapio/bebida.py

from modelos.cardapio.item_cardapio import ItemCardapio


class Bebida(ItemCardapio):
    '''
    Representa uma bebida do cardápio, herdando funcionalidades de ItemCardapio.

    Attributes:
        _nome (str): Nome da bebida.
        _preco (float): Preço da bebida.
        tamanho (float): Tamanho bebida.
    '''

    def __init__(self, nome: str, preco: float, tamanho: str):
        '''
        Inicializa uma instância de Bebida.

        Inputs:
        - nome (str): Nome da bebida.
        - preco (float): Preço da bebida.
        - tamanho (str): Tamanho bebida.
        '''
        super().__init__(nome, preco)
        self.tamanho: float = tamanho

    def __str__(self):
        return self._nome

    def aplicar_desconto(self):
        self._preco -= (self._preco * 0.08)
        self._preco = round(self._preco, 2)

    def _campos_adicionais(self) -> dict:
        return {'tamanho': self.tamanho}

    @classmethod
    def from_dict(cls, data: dict) -> 'Bebida':
        return cls(
            nome   = data['nome'],
            preco  = data['preco'],
            tamanho= data['tamanho']
    )