# Saborexpress API (curso Python 3)

API RESTful em FastAPI para gerenciar restaurantes, cardápios e avaliações, com persistência de dados em JSON. Desenvolvida como exercício no terceiro módulo do curso de Python, esta aplicação demonstra práticas de **Orientação a Objetos**, **herança**, **polimorfismo**, uso de **classes abstratas**, integração com **FastAPI**, validação com **Pydantic**, **testes automatizados** e **documentação interativa**.

## Sumário

- [Saborexpress API (curso Python 3)](#saborexpress-api-curso-python-3)
  - [Sumário](#sumário)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
  - [Uso](#uso)
  - [Endpoints da API](#endpoints-da-api)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Descrição dos Componentes](#descrição-dos-componentes)
    - [`main.py`](#mainpy)
    - [`modelos/restaurante.py`](#modelosrestaurantepy)
    - [`modelos/cardapio/`](#modeloscardapio)
      - [`item_cardapio.py`](#item_cardapiopy)
      - [`prato.py`, `bebida.py`, `sobremesa.py`](#pratopy-bebidapy-sobremesapy)
    - [`schemas/schemas.py`](#schemasschemaspy)
  - [Conceitos Abordados no Curso](#conceitos-abordados-no-curso)
  - [Boas Práticas de Código](#boas-práticas-de-código)
  - [Testes Automatizados](#testes-automatizados)
  - [Dependências](#dependências)
  - [TODO](#todo)

## Pré-requisitos

* Python 3.10 ou superior
* `pip` e `venv` para gerenciamento de dependências
* Ambiente virtual configurado

## Instalação

1. **Clone** este repositório:

   ```bash
   git clone https://github.com/carlosvblessa/curso-python-3
   cd curso-python-3
   ```

2. **Crie** e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instale** as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie o servidor:

   ```bash
   uvicorn main:app --reload
   ```

Acesse `http://127.0.0.1:8000/docs` para visualizar a documentação interativa da API.

## Uso

A API permite:

- Cadastrar, listar, ativar/inativar restaurantes
- Avaliar restaurantes por clientes
- Adicionar/remover itens ao cardápio (pratos, bebidas, sobremesas)
- Aplicar descontos específicos por tipo de item (5% para pratos, 8% para bebidas, 15% para sobremesas)
- Visualizar resumos e detalhes completos de restaurantes

Todos os dados são persistidos em `dados/restaurantes.json`.

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/restaurants` | Cadastra novo restaurante |
| `GET` | `/restaurants` | Lista todos os restaurantes com detalhes |
| `GET` | `/restaurants/summary` | Lista resumo (nome, categoria, média e status) |
| `PATCH` | `/restaurants/{nome}/toggle` | Ativa/inativa restaurante |
| `POST` | `/restaurants/{nome}/rating` | Registra avaliação |
| `POST` | `/restaurants/{nome}/menu` | Adiciona item ao cardápio |
| `GET` | `/restaurants/{nome}/menu` | Lista o cardápio de um restaurante |
| `PATCH` | `/restaurants/{nome}/menu/{item_nome}/discount` | Aplica desconto ao item |

Documentação interativa disponível em:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Estrutura do Projeto

```
curso-python-3/
├── dados/                        
│   └── restaurantes.json        # Armazenamento persistente
├── modelos/
│   ├── restaurante.py           # Classe Restaurante e lógica de persistência
│   ├── avaliacao.py             # Classe Avaliacao
│   └── cardapio/
│       ├── item_cardapio.py     # Classe abstrata ItemCardapio
│       ├── prato.py             # Classe Prato
│       ├── bebida.py            # Classe Bebida
│       └── sobremesa.py         # Classe Sobremesa
├── schemas/
│   └── schemas.py               # Modelos Pydantic para validação de dados
├── tests/
│   └── test_main.py             # Testes unitários com pytest
├── main.py                      # Servidor FastAPI
└── requirements.txt             # Dependências do projeto
```

## Descrição dos Componentes

### `main.py`

- Configuração do servidor FastAPI com ciclo de vida (`lifespan`) para carregar/salvar dados automaticamente.
- Definição dos endpoints com tratamento de requisições HTTP.
- Validação de entrada com `Pydantic`.
- Tratamento de erros customizado.

### `modelos/restaurante.py`

- Representa um restaurante com nome, categoria, estado ativo/inativo, lista de avaliações e cardápio.
- Métodos:
  - `carregar_dados()` e `salvar_dados()` — persistência via JSON
  - `alternar_estado()` — inverte status do restaurante
  - `receber_avaliacao()` — adiciona nova avaliação
  - `adicionar_ao_cardapio()` — inclui item ao cardápio
- Propriedades calculadas:
  - `media_avaliacoes`: média das notas
  - `ativo`: retorna emoji de status

### `modelos/cardapio/`

#### `item_cardapio.py`

- Classe abstrata base com método abstrato `aplicar_desconto()`.
- Atributos: `_nome`, `_preco`.

#### `prato.py`, `bebida.py`, `sobremesa.py`

- Herdam de `ItemCardapio`.
- Implementam `aplicar_desconto()` com percentuais específicos:
  - Prato: 5%
  - Bebida: 8%
  - Sobremesa: 15%

### `schemas/schemas.py`

- Modelos Pydantic para validação de dados nas requisições/respostas da API.
- Tipos definidos:
  - `CreateRestaurant`: cadastro de restaurante
  - `Rating`: avaliação
  - `MenuItem`: item do cardápio
  - `RestaurantSummary`: resumo de restaurante
  - `RestaurantDetail`: detalhes completos
  - `AvaliacaoSchema`, `CardapioItemSchema`: tipos internos

## Conceitos Abordados no Curso

- **Orientação a Objetos Avançada**
  - Herança, polimorfismo e classes abstratas
  - Encapsulamento com propriedades (`@property`)
  - Métodos especiais e construtores personalizados

- **Persistência de Dados**
  - Manipulação de JSON com `json`
  - Caminhos dinâmicos com `os.path`

- **Desenvolvimento Web com FastAPI**
  - Criação de APIs RESTful
  - Documentação automática (Swagger e ReDoc)
  - Validação de entrada com Pydantic

- **Tratamento de Exceções**
  - Validação de dados com mensagens claras
  - Tratamento de recursos inexistentes

- **Boas Práticas**
  - Separação de responsabilidades
  - Uso de ambientes virtuais
  - Modularização do código

## Boas Práticas de Código

- **PEP 8**: formatação padronizada verificada com `flake8`.
- **Type Hints**: anotações de tipo em todas as funções e métodos.
- **Clean Architecture**: separação clara entre domínio, infraestrutura e interface.

## Testes Automatizados

Os testes estão localizados em `tests/test_main.py` e cobrem:

- Criação, listagem, alternância de estado e avaliação de restaurantes
- Adição e consulta de itens no cardápio
- Aplicação correta de descontos
- Tratamento de casos inválidos (ex.: duplicados, restaurante inexistente)

A cobertura dos testes está em **94%**, garantindo robustez e confiabilidade no funcionamento da API.

Para executar os testes:

```bash
pytest --cov=. --cov-report html
```

## Dependências

Listadas em `requirements.txt`:

```
fastapi==0.115.12
uvicorn==0.34.3
requests==2.32.4
httpx==0.28.1
pydantic==2.9.2
pytest==8.4.0
pytest-cov==6.1.1
pytest-mock==3.14.1
flake8==7.2.0
mypy==1.16.0
mypy_extensions==1.1.0
pre_commit==4.2.0
```

## TODO

Futuramente, planeja-se implementar:

- **Novos endpoints para CRUD completo de itens do cardápio**
  - `PUT /restaurants/{nome}/menu/{item_nome}` – Atualizar item do cardápio
  - `DELETE /restaurants/{nome}/menu/{item_nome}` – Remover item do cardápio

- **Controle de desconto nos itens do cardápio**
  - Garantir que o desconto só possa ser aplicado uma única vez por item
  - Adicionar atributo `_desconto_aplicado` às classes filhas de `ItemCardapio`
  - Validar antes de aplicar desconto se ele já foi aplicado previamente
