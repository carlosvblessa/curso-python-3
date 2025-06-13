# modelos/restaurante.py

import json
import os
from typing import List, Optional, Union

from modelos.avaliacao import Avaliacao
from modelos.cardapio.item_cardapio import ItemCardapio
from modelos.cardapio.prato import Prato
from modelos.cardapio.bebida import Bebida
from modelos.cardapio.sobremesa import Sobremesa


class Restaurante:
    """
    Representa um restaurante e suas características.

    Attributes:
        _nome (str): Nome do restaurante.
        _categoria (str): Categoria à qual o restaurante pertence.
        _ativo (bool): Estado do restaurante (ativo/inativo).
        _avaliacao (List[Avaliacao]): Lista de avaliações atribuídas
                      ao restaurante.
        restaurantes (List[Restaurante]): Lista de todos os restaurantes
                      cadastrados.
        ARQUIVO_DADOS (str): Caminho do arquivo onde os dados dos
                      restaurantes são salvos.
    """

    restaurantes: List["Restaurante"] = []
    ARQUIVO_DADOS = os.getenv(
        "ARQUIVO_DADOS",
        os.path.join(os.getcwd(), "dados", "restaurantes.json"),
    )

    def __init__(
        self,
        nome: str,
        categoria: str,
        ativo: bool = False,
        avaliacoes: Optional[List[Avaliacao]] = None,
        cardapio: Optional[List[ItemCardapio]] = None,
    ):
        """
        Inicializa uma instância de Restaurante.

        Inputs:
        - nome (str): O nome do restaurante.
        - categoria (str): A categoria do restaurante.
        - ativo (bool): Indica se o restaurante está ativo.
        - avaliacoes (List[Avaliacao] | None): Lista de avaliações existentes.
        - cardapio (List[ItemCardapio] | None): Lista de itens do cardápio.
        """
        self._nome = nome
        self._categoria = categoria
        self._ativo = ativo
        self._avaliacao = avaliacoes or []
        self._cardapio = cardapio or []
        Restaurante.restaurantes.append(self)

    @classmethod
    def carregar_dados(cls):
        """
        Carrega os dados dos restaurantes a partir do arquivo JSON.
        Se o arquivo não existir, a lista permanece vazia.
        """
        cls.restaurantes.clear()
        if not os.path.exists(cls.ARQUIVO_DADOS):
            return

        try:
            with open(cls.ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)

            for item in dados:
                avals = [
                    Avaliacao(a["cliente"], a["nota"])
                    for a in item.get("avaliacoes", [])
                ]
                items = []
                for c in item.get("cardapio", []):
                    tipo = c.get("__type__")
                    cls_item = {
                        "Prato": Prato,
                        "Bebida": Bebida,
                        "Sobremesa": Sobremesa,
                    }.get(tipo, ItemCardapio)
                    items.append(cls_item.from_dict(c))
                cls(
                    nome=item["nome"],
                    categoria=item["categoria"],
                    ativo=item.get("ativo", False),
                    avaliacoes=avals,
                    cardapio=items,
                )
        except json.JSONDecodeError:
            # Arquivo vazio ou inválido — ignora carregamento
            cls.restaurantes.clear()

    @classmethod
    def salvar_dados(cls):
        """
        Salva todos os restaurantes em um arquivo JSON.
        Inclui nome, categoria, status, avaliações e cardápio
        (bebidas, pratos e sobremesas).
        """
        try:
            diretorio = os.path.dirname(cls.ARQUIVO_DADOS)
            os.makedirs(diretorio, exist_ok=True)

            dados = []
            for r in cls.restaurantes:
                dados.append(
                    {
                        "nome": r._nome,
                        "categoria": r._categoria,
                        "ativo": r._ativo,
                        "avaliacoes": [
                            {"cliente": a._cliente, "nota": a._nota}
                            for a in r._avaliacao
                        ],
                        "cardapio": [item.to_dict() for item in r._cardapio],
                    }
                )

            with open(cls.ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[Erro ao salvar dados] {e}")
            raise

    def alternar_estado(self) -> str:
        """
        Alterna o estado ativo/inativo e salva os dados.
        """
        self._ativo = not self._ativo
        Restaurante.salvar_dados()
        return (f"O restaurante '{self._nome}' foi "
                f"{'ativado' if self._ativo else 'inativado'}")

    def receber_avaliacao(self, cliente: str, nota: float) -> None:
        """
        Adiciona uma avaliação ou propaga ValueError.
        """
        avaliacao = Avaliacao(cliente, nota)
        self._avaliacao.append(avaliacao)
        Restaurante.salvar_dados()

    @property
    def media_avaliacoes(self) -> Union[float, str]:
        """
        Calcula e retorna a média das avaliações, ou '-' se não houver.
        """
        if not self._avaliacao:
            return "-"
        return round(
            sum(a._nota for a in self._avaliacao) / len(self._avaliacao), 1
        )

    def adicionar_ao_cardapio(self, item: ItemCardapio) -> None:
        """
        Adiciona um item (Prato, Bebida ou Sobremesa) ao cardápio do
        restaurante.

        Inputs:
        - item (ItemCardapio): Instância de Prato, Bebida ou Sobremesa.
        """
        self._cardapio.append(item)
        Restaurante.salvar_dados()

    @property
    def cardapio(self) -> List[ItemCardapio]:
        """
        Lista de itens do cardápio.
        """
        return list(self._cardapio)

    @property
    def ativo(self) -> bool:
        """
        Indica se o restaurante está ativo.
        """
        return self._ativo
