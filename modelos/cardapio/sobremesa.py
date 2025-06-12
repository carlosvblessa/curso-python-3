# modelos/cardapio/sobremesa.py

from modelos.cardapio.item_cardapio import ItemCardapio


class Sobremesa(ItemCardapio):
    '''
    Representa uma bebida do cardápio, herdando funcionalidades de ItemCardapio.

    Attributes:
        _nome (str): Nome da sobremesa.
        _preco (float): Preço da sobremesa.
        descricao (str): Descrição da sobremesa.
        tipo (str): Tipo da sobremesa.
        tamanho (float): Tamanho da sobremesa.
    '''

    def __init__(self, nome: str, preco: float, descricao: str, tipo: str, tamanho: str):
        '''
        Inicializa uma instância de Sobremesa.

        Inputs:
        - nome (str): Nome da sobremesa.
        - preco (float): Preço da sobremesa.
        - descricao (str): Descrição da sobremesa.
        - tipo (str): Tipo da sobremesa.
        - tamanho (str): Tamanho da sobremesa.
        '''
        super().__init__(nome, preco)
        self.descricao = descricao
        self.tipo = tipo
        self.tamanho = tamanho

    def __str__(self):
        return self._nome

    def aplicar_desconto(self):
        self._preco -= (self._preco * 0.15)
        self._preco = round(self._preco, 2)

    def _campos_adicionais(self) -> dict:
        return {
            'descricao': self.descricao,
            'tipo': self.tipo,
            'tamanho': self.tamanho
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Sobremesa':
        return cls(
            nome     = data['nome'],
            preco    = data['preco'],
            descricao= data['descricao'],
            tipo     = data['tipo'],
            tamanho  = data['tamanho']
    )

