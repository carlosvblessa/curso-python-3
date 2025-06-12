# modelos/restaurante.py

import json
import os
from colorama import Fore, Style
from typing import List, Optional, Union

from modelos.avaliacao import Avaliacao
from modelos.cardapio.item_cardapio import ItemCardapio
from modelos.cardapio.bebida import Bebida
from modelos.cardapio.prato import Prato
from modelos.cardapio.sobremesa import Sobremesa


class Restaurante:
    '''
    Representa um restaurante e suas características.

    Attributes:
        _nome (str): Nome do restaurante.
        _categoria (str): Categoria à qual o restaurante pertence.
        _ativo (bool): Estado do restaurante (ativo/inativo).
        _avaliacao (List[Avaliacao]): Lista de avaliações atribuídas ao restaurante.
        restaurantes (List[Restaurante]): Lista de todos os restaurantes cadastrados.
        ARQUIVO_DADOS (str): Caminho do arquivo onde os dados dos restaurantes são salvos.
    '''

    restaurantes: List['Restaurante'] = []
    cardapio: List['Restaurante'] = []
    ARQUIVO_DADOS = os.path.join(os.getcwd(), 'dados', 'restaurantes.json')

    def __init__(
        self,
        nome: str,
        categoria: str,
        ativo: bool = False,
        avaliacoes: Optional[List[Avaliacao]] = None,
        cardapio: Optional[List[ItemCardapio]] = None
    ):
        '''
        Inicializa uma instância de Restaurante.

        Inputs:
        - nome (str): O nome do restaurante.
        - categoria (str): A categoria do restaurante.
        - ativo (bool): Indica se o restaurante está ativo.
        - avaliacoes (List[Avaliacao] | None): Lista de avaliações existentes.
        - cardapio (List[ItemCardapio] | None): Lista de itens do cardápio.
        '''
        self._nome = nome
        self._categoria = categoria
        self._ativo = ativo
        self._avaliacao = avaliacoes or []
        self._cardapio = cardapio or []

        Restaurante.restaurantes.append(self)
    

    def __str__(self):
        return self._nome

    @classmethod
    def carregar_dados(cls):
        '''
        Carrega os dados dos restaurantes a partir do arquivo JSON.
        Se o arquivo não existir, a lista permanece vazia.
        '''
        cls.restaurantes.clear()
        if not os.path.exists(cls.ARQUIVO_DADOS):
            return

        with open(cls.ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

        for item in dados:
            avals = [
                Avaliacao(a['cliente'], a['nota'])
                for a in item.get('avaliacoes', [])
            ]

            items_cardapio = []
            for c in item.get('cardapio', []):
                tipo = c.get('__type__')
                # pega a classe pelo nome; cai em ItemCardapio se não existir
                cls_item = {
                    'Prato':     Prato,
                    'Bebida':    Bebida,
                    'Sobremesa': Sobremesa
                }.get(tipo, ItemCardapio)
                items_cardapio.append(cls_item.from_dict(c))

            cls(
                nome=item['nome'],
                categoria=item['categoria'],
                ativo=item.get('ativo', False),
                avaliacoes=avals,
                cardapio=items_cardapio
            )

    @classmethod
    def salvar_dados(cls):
        '''
        Salva todos os restaurantes em um arquivo JSON.
        Inclui nome, categoria, status, avaliações e cardápio (bebidas, pratos e sobremesas).
        '''
        os.makedirs(os.path.dirname(cls.ARQUIVO_DADOS), exist_ok=True)
        dados = []
        for r in cls.restaurantes:
            dados.append({
                'nome':       r._nome,
                'categoria':  r._categoria,
                'ativo':      r._ativo,
                'avaliacoes': [
                    {'cliente': a._cliente, 'nota': a._nota}
                    for a in r._avaliacao
                ],
                'cardapio': [item.to_dict() for item in r._cardapio]
            })

        with open(cls.ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    @classmethod
    def listar_restaurantes(cls):
        '''
        Lista os restaurantes cadastrados de forma formatada.
        '''
        if not cls.restaurantes:
            print('Nenhum restaurante cadastrado.')
            return

        dados = [
            {
                'Nome': r.nome,
                'Categoria': r.categoria,
                'Avaliação': r.media_avaliacoes,
                'Situação': r.ativo
            }
            for r in cls.restaurantes
        ]
        colunas = ['Nome', 'Categoria', 'Avaliação', 'Situação']
        larguras = {
            c: max(len(c), max(len(str(d[c])) for d in dados))
            for c in colunas
        }
        header = ' | '.join(c.ljust(larguras[c]) for c in colunas)
        print(header)
        print('-' * len(header))
        for d in dados:
            print(' | '.join(str(d[c]).ljust(larguras[c]) for c in colunas))

    @property
    def ativo(self) -> str:
        '''
        Retorna o símbolo de atividade do restaurante: 🟢 ativo, 🔴 inativo.
        '''
        return '🟢' if self._ativo else '🔴'

    @property
    def nome(self) -> str:
        '''
        Nome formatado do restaurante.
        '''
        return self.__formatar_personalizado(self._nome)

    @property
    def categoria(self) -> str:
        '''
        Categoria formatada do restaurante.
        '''
        return self.__formatar_personalizado(self._categoria)

    def __formatar_personalizado(self, texto: str) -> str:
        '''
        Aplica capitalização customizada, ignorando preposições e conjunções.
        '''
        excecoes = {'do', 'da', 'dos', 'das', 'de', 'e'}
        palavras = texto.lower().split()
        resultado = []
        for i, palavra in enumerate(palavras):
            if i == 0 or palavra not in excecoes:
                resultado.append(palavra.capitalize())
            else:
                resultado.append(palavra)
        return ' '.join(resultado)

    def alternar_estado(self) -> str:
        '''
        Alterna o estado ativo/inativo e salva os dados.
        '''
        self._ativo = not self._ativo
        Restaurante.salvar_dados()
        ativo = f'{Style.BRIGHT}{Fore.GREEN}ativado{Style.RESET_ALL}'
        inativo = f'{Style.BRIGHT}{Fore.RED}inativado{Style.RESET_ALL}'
        status = ativo if self._ativo else inativo
        return f'O restaurante {self._nome} foi {status}'

    def receber_avaliacao(self, cliente: str, nota: float) -> None:
        '''
        Registra uma avaliação e salva os dados.
        '''
        try:
            avaliacao = Avaliacao(cliente, nota)
            self._avaliacao.append(avaliacao)
            Restaurante.salvar_dados()
        except ValueError as e:
            print(f'Erro ao adicionar avaliação: {e}')

    @property
    def media_avaliacoes(self) -> Union[float, str]:
        '''
        Calcula a média das avaliações, ou '-' se não houver.
        '''
        if not self._avaliacao:
            return '-'
        soma = sum(a._nota for a in self._avaliacao)
        media = round(soma / len(self._avaliacao), 1)
        return media

    def adicionar_ao_cardapio(self, item: ItemCardapio) -> None:
        '''
        Adiciona um item (Prato ou Bebida) ao cardápio do restaurante.

        Inputs:
        - item (ItemCardapio): Instância de Prato, Bebida ou outra subclasse de ItemCardapio.
        '''
        self._cardapio.append(item)
        Restaurante.salvar_dados()

    @property
    def cardapio(self) -> List[ItemCardapio]:
        '''
        Retorna uma cópia protegida do cardápio do restaurante.
        '''
        return list(self._cardapio)

    def exibir_cardapio(self):
        '''
        Exibe o cardápio do restaurante no terminal, diferenciando bebidas, pratos e sobremesas.
        Mostra nome, preço e informações extras como descrição, tamanho ou tipo.
        '''
        print(f'\n{"=" * 40}')
        print(f'{Style.BRIGHT}Cardápio do {self._nome}{Style.RESET_ALL}')
        print(f'{"=" * 40}\n')

        if not self._cardapio:
            print('O cardápio está vazio.')
            return

        for i, item in enumerate(self._cardapio, start=1):
            tipo = (
                'Prato' if isinstance(item, Prato) else
                'Bebida' if isinstance(item, Bebida) else
                'Sobremesa' if isinstance(item, Sobremesa) else
                'Item desconhecido'
            )
            preco = f'R$ {item._preco:.2f}'

            print(f'{i}. {item._nome} ({tipo}) - {preco}')

            if isinstance(item, Prato):
                print(f'   📝 Descrição: {item.descricao}')
            elif isinstance(item, Bebida):
                print(f'   🥤 Tamanho: {item.tamanho} ml')
            elif isinstance(item, Sobremesa):
                print(f'   🍰 Tipo: {item.tipo}')
                print(f'   📝 Descrição: {item.descricao}')
                print(f'   📏 Tamanho: {item.tamanho}')

            print()