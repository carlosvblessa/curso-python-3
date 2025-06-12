# modelos/cardapio/item_cardapio.py

from abc import ABC, abstractmethod

class ItemCardapio(ABC):
    '''
    Representa um item do cardápio de um restaurante.

    Attributes:
        _nome (str): Nome do item do cardápio.
        _preco (float): Preço do item.
    '''

    def __init__(self, nome: str, preco: float):
        '''
        Inicializa uma instância de ItemCardapio.

        Inputs:
        - nome (str): Nome do item.
        - preco (float): Preço do item.
        '''
        self._nome: str = nome
        self._preco: float = preco

    @abstractmethod
    def aplicar_desconto(self):
        pass

    @abstractmethod
    def _campos_adicionais(self) -> dict:
        '''
        Deve retornar um dict com TODOS os atributos específicos da subclasse.
        Ex: {'descricao': self.descricao}
        '''
        pass

    def to_dict(self) -> dict:
        base = {
            '__type__': self.__class__.__name__,
            'nome':     self._nome,
            'preco':    self._preco,
        }
        base.update(self._campos_adicionais())
        return base

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'ItemCardapio':
        '''
        Deve reconstruir uma instância de cls a partir do dict serializado.
        Ex.: Prato.from_dict({'nome':..., 'preco':..., 'descricao':...})
        '''
        ...