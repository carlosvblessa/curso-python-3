# app.py

import os

from modelos.restaurante import Restaurante


def exibir_nome_app():
    '''
    Exibe o nome estilizado da aplicação
    '''
    print(
        '''🇸​​​​​ 🇦​​​​​ 🇧​​​​​ 🇴​​​​​ 🇷 ​​​​​​​​ 🇪​​​​​ 🇽​​​​​ 🇵​​​​​ 🇷​​​​​ 🇪​​​​​ 🇸​​​​​ 🇸
        '''  # noqa: E122,E501
    )


def exibir_opcoes():
    '''
    Exibe as opções disponíveis no menu principal da app
    '''
    print('1. Cadastrar restaurante')
    print('2. Listar restaurantes')
    print('3. Alternar estado do restaurante')
    print('4. Avaliar restaurante')
    print('5. Sair\n')


def exibir_subtitulo(texto: str):
    '''
    Exibe um subtítulo estilizado na tela

    Inputs:
    - texto: str - O texto do subtítulo
    '''
    os.system('clear')
    linha = '*' * len(texto)
    print(linha)
    print(texto)
    print(f'{linha}\n')


def cadastrar_restaurante():
    '''
    Cadastra um novo restaurante

    Inputs:
    - Nome do restaurante
    - Categoria

    Outputs:
    - Adiciona um restaurante à lista de restaurantes
    '''
    exibir_subtitulo('Cadastro de restaurantes')
    nome = input('Digite o nome do restaurante: ').strip()
    categoria = input('Digite a categoria do restaurante: ').strip()

    if any(r._nome.lower() == nome.lower() for r in Restaurante.restaurantes):
        print(f'O restaurante "{nome}" já está cadastrado.')
    else:
        Restaurante(nome, categoria)
        Restaurante.salvar_dados()
        print(f'O restaurante "{nome}" foi cadastrado com sucesso!')


def listar_restaurantes():
    '''
    Lista os restaurantes constantes no dicionário

    Outputs:
    - Exibe a lista de restaurantes na tela
    '''
    exibir_subtitulo('Restaurantes cadastrados')
    Restaurante.listar_restaurantes()


def alternar_estado_restaurante():
    '''
    Altera o estado ativo/desativado de um restaurante

    Outputs:
    - Exibe mensagem indicando o sucesso da operação
    '''
    exibir_subtitulo('Alterando estado do restaurante')
    nome = input('Digite o nome do restaurante: ').strip()
    for r in Restaurante.restaurantes:
        if r._nome.lower() == nome.lower():
            mensagem = r.alternar_estado()
            print(mensagem)
            Restaurante.salvar_dados()
            return
    print(f'O restaurante "{nome}" não está cadastrado')


def avaliar_restaurante():
    '''
    Registra uma avaliação para um restaurante

    Inputs:
    - Nome do restaurante
    - Nota (entre 1 e 5)

    Outputs:
    - Mensagem de sucesso ou erro
    '''
    exibir_subtitulo('Avaliação de restaurante')
    nome = input('Digite o nome do restaurante: ').strip()
    for r in Restaurante.restaurantes:
        if r._nome.lower() == nome.lower():
            try:
                nota = float(input('Digite a nota (1 a 5): ').strip())
                cliente = input('Seu nome: ').strip()
                r.receber_avaliacao(cliente, nota)
                print(f'Avaliação registrada para {r.nome}')
            except ValueError as e:
                print(f'Erro: {e}')
            return
    print(f'O restaurante "{nome}" não está cadastrado')


def main():
    '''
    Loop principal da aplicação
    '''
    Restaurante.carregar_dados()
    while True:
        os.system('clear')
        exibir_nome_app()
        exibir_opcoes()
        opcao = input('Escolha uma opção: ').strip()

        match opcao:
            case '1':
                cadastrar_restaurante()
            case '2':
                listar_restaurantes()
            case '3':
                alternar_estado_restaurante()
            case '4':
                avaliar_restaurante()
            case '5':
                exibir_subtitulo('Finalizando app')
                break
            case _:
                exibir_subtitulo('Opção inválida')

        input('\nDigite uma tecla para voltar ao menu')


if __name__ == '__main__':
    main()
