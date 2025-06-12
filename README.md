# Gerenciador de Restaurantes (curso Python 2)

Aplicação de linha de comando em Python para cadastro, listagem, ativação/inativação e avaliação de restaurantes, com **persistência de dados** em JSON, desenvolvida como exercício no segundo módulo do curso de Python. A aplicação evidencia práticas de **POO**, **tratamento de arquivos**, uso de **bibliotecas externas** e **testes automatizados**.

## Sumário

- [Gerenciador de Restaurantes (curso Python 2)](#gerenciador-de-restaurantes-curso-python-2)
  - [Sumário](#sumário)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
  - [Uso](#uso)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Descrição das Funções](#descrição-das-funções)
    - [`app.py`](#apppy)
    - [`modelos/restaurante.py`](#modelosrestaurantepy)
    - [`modelos/avaliacao.py`](#modelosavaliacaopy)
  - [Conceitos Abordados no Curso](#conceitos-abordados-no-curso)
  - [Boas Práticas de Código](#boas-práticas-de-código)
  - [Testes](#testes)
  - [Dependências](#dependências)

## Pré-requisitos

* Python 3.10 ou superior
* `pip` (para instalar dependências de desenvolvimento)

## Instalação

1. **Clone** este repositório e entre na pasta:

   ```bash
   git clone https://github.com/carlosvblessa/curso-python-2
   cd curso-python-2
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

## Uso

Para executar a aplicação:

```bash
python app.py
```

Ao iniciar, o menu exibe as opções:

1. **Cadastrar restaurante** — registra nome e categoria (por padrão inativo)
2. **Listar restaurantes** — exibe todos os restaurantes com média de avaliações e status
3. **Alternar estado do restaurante** — ativa ou inativa um restaurante existente
4. **Avaliar restaurante** — registra nota (1–5) de um cliente para um restaurante
5. **Sair** — finaliza a aplicação

Os dados são carregados de `dados/restaurantes.json` ao iniciar e salvos automaticamente a cada alteração.

## Estrutura do Projeto

```
curso-python-2/
├── dados/                        
│   └── restaurantes.json        # Armazenamento persistente (criado em tempo de execução)
├── modelos/
│   ├── avaliacao.py             # Classe Avaliacao
│   └── restaurante.py           # Classe Restaurante e lógica de persistência
├── tests/
│   └── test_app.py              # Testes unitários com pytest
├── app.py                       # Interface de linha de comando
└── requirements.txt             # Dependências do projeto
```

## Descrição das Funções

### `app.py`

* **`exibir_nome_app()`**
  Exibe o título estilizado da aplicação.

* **`exibir_opcoes()`**
  Lista as opções de menu (inclusão da opção de avaliação).

* **`exibir_subtitulo(texto: str)`**
  Limpa a tela e imprime um subtítulo com bordas de `*`.

* **`cadastrar_restaurante()`**
  Coleta nome e categoria; verifica duplicatas; instancia `Restaurante`; persiste dados.

* **`listar_restaurantes()`**
  Carrega subtítulo e delega a exibição formatada ao método de classe `Restaurante.listar_restaurantes()`.

* **`alternar_estado_restaurante()`**
  Busca restaurante por nome; chama `Restaurante.alternar_estado()`; persiste dados.

* **`avaliar_restaurante()`**
  Recebe nome, nota e cliente; chama `Restaurante.receber_avaliacao()`; trata `ValueError`.

* **`main()`**
  Loop principal: carrega dados via `Restaurante.carregar_dados()`, exibe menu, roteia opções com `match/case` e pausa entre operações.

### `modelos/restaurante.py`

* **`Restaurante.carregar_dados()`** + **`Restaurante.salvar_dados()`**
  Leitura e escrita de JSON em `dados/restaurantes.json`.

* **`Restaurante.listar_restaurantes()`**
  Exibe tabela alinhada de Nome, Categoria, Avaliação média e Situação (🟢/🔴).

* **Propriedades**

  * `.nome` e `.categoria`: formatação personalizada de texto (capitalização inteligente).
  * `.ativo`: retorna emoji de status.

* **Métodos de instância**

  * `alternar_estado()`: inverte `_ativo`, salva e retorna mensagem colorida com `colorama`.
  * `receber_avaliacao(cliente, nota)`: cria instância `Avaliacao`, adiciona à lista e salva.

* **Propriedade**

  * `media_avaliacoes`: calcula média de `_nota`, arredonda uma casa decimal ou retorna `'-'`.

### `modelos/avaliacao.py`

Classe simples com validação de `nota` (1 a 5) em `__init__`, lançando `ValueError` para valores inválidos.

## Conceitos Abordados no Curso

* **Orientação a Objetos Avançada**

  * Métodos de classe (`@classmethod`) vs. métodos de instância
  * Propriedades (`@property`) para encapsular lógica de atributos
  * Construtor (`__init__`) e métodos especiais (`__str__`, não usado aqui porém explorado anteriormente)

* **Persistência de Dados**

  * Módulo `json` para serialização/deserialização
  * Manipulação de arquivos e diretórios com `os.path` e `os.makedirs`

* **Formatação e Estilização**

  * `colorama` para cores em terminal
  * Capitalização inteligente de strings (ignorando preposições)

* **Tratamento de Exceções**

  * Validação de entradas (nota fora de faixa)
  * Mensagens de erro informativas sem quebrar o fluxo

* **Entrada e Saída em Terminal**

  * Limpeza de tela com `os.system('clear')`
  * Pausa entre operações para melhor usabilidade

* **Testes Automatizados**

  * `pytest` com fixtures para isolamento e monkeypatch
  * Cobertura de fluxo de cadastro, listagem, avaliação, alternância e finalização

## Boas Práticas de Código

* **PEP 8**: formatação de código padronizada, verificada via Flake8 com hook de pre-commit.
* **Type Hints**: todas as funções e métodos declaram tipos de parâmetros e retorno para maior clareza e suporte a ferramentas de análise (mypy, IDEs).
  
## Testes

Os testes estão em `tests/test_app.py` e cobrem:

* Exibição de título, opções e subtítulos
* Fluxos de cadastro, listagem e alternância de estado (caso existente e não existente)
* Funcionalidade de avaliação (sucesso, erro e restaurante não cadastrado)
* Comportamento do loop principal (`main`), incluindo rota de finalização e roteamento de opções

Para executar:

```bash
pytest --cov=. --cov-report html
```

## Dependências

Listadas em `requirements.txt`:

```
colorama==0.4.6
types-colorama==0.4.15.20240311
pytest==8.4.0
pytest-cov==6.1.1
pytest-mock==3.14.1
flake8==7.2.0
mypy==1.16.0
mypy_extensions==1.1.0
pre_commit==4.2.0
```
