# modelos/cardapio/prato.py

from modelos.cardapio.item_cardapio import ItemCardapio


class Prato(ItemCardapio):
    '''
    Representa um prato do cardápio, herdando funcionalidades de ItemCardapio.

    Attributes:
        _nome (str): Nome do prato.
        _preco (float): Preço do prato.
        descricao (str): Descrição detalhada do prato.
    '''

    def __init__(self, nome: str, preco: float, descricao: str):
        '''
        Inicializa uma instância de Prato.

        Inputs:
        - nome (str): Nome do prato.
        - preco (float): Preço do prato.
        - descricao (str): Descrição do prato.
        '''
        super().__init__(nome, preco)
        self.descricao: str = descricao


    def __str__(self):
        return self._nome

    def aplicar_desconto(self):
        self._preco -= (self._preco * 0.05)
        self._preco = round(self._preco, 2)

    def _campos_adicionais(self) -> dict:
        return {'descricao': self.descricao}

    @classmethod
    def from_dict(cls, data: dict) -> 'Prato':
        return cls(
            nome     = data['nome'],
            preco    = data['preco'],
            descricao= data['descricao']
    )