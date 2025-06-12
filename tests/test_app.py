# tests/test_app.py

import os
import builtins
import pytest

from app import (
    exibir_nome_app,
    exibir_opcoes,
    exibir_subtitulo,
    cadastrar_restaurante,
    listar_restaurantes,
    alternar_estado_restaurante,
    avaliar_restaurante,
    main,
)
from modelos.restaurante import Restaurante


@pytest.fixture(autouse=True)
def no_clear(monkeypatch):
    # impede clear real
    monkeypatch.setenv('TERM', 'dumb')
    monkeypatch.setattr(os, 'system', lambda cmd: None)


@pytest.fixture(autouse=True)
def clean_restaurantes():
    # limpa lista antes e depois de cada teste
    Restaurante.restaurantes.clear()
    yield
    Restaurante.restaurantes.clear()


def test_exibir_nome_app(capsys):
    exibir_nome_app()
    out = capsys.readouterr().out
    assert '🇸' in out


def test_exibir_opcoes(capsys):
    exibir_opcoes()
    out = capsys.readouterr().out
    assert '1. Cadastrar restaurante' in out
    assert '5. Sair' in out


def test_exibir_subtitulo(capsys):
    exibir_subtitulo('Teste X')
    lines = capsys.readouterr().out.splitlines()
    assert lines[1] == 'Teste X'
    assert set(lines[0]) == {'*'} and set(lines[2]) == {'*'}


def test_cadastrar_restaurante(monkeypatch, capsys):
    nome, cat = 'NovoBoteco', 'Boteco'
    inputs = iter([nome, cat])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

    cadastrar_restaurante()
    out = capsys.readouterr().out.lower()
    assert nome.lower() in out
    assert 'foi cadastrado com sucesso' in out


def test_alternar_estado_restaurante_existente(monkeypatch, capsys):
    r = Restaurante('Teste', 'Cat')
    assert not r._ativo
    monkeypatch.setattr(builtins, 'input', lambda prompt='': 'Teste')

    alternar_estado_restaurante()
    out = capsys.readouterr().out.lower()
    assert 'ativado' in out
    assert r._ativo is True


def test_alternar_estado_restaurante_nao_existente(monkeypatch, capsys):
    monkeypatch.setattr(builtins, 'input', lambda prompt='': 'Inexistente')
    alternar_estado_restaurante()
    out = capsys.readouterr().out.lower()
    assert 'inexistente' in out and 'não está cadastrado' in out


def test_listar_restaurantes(capsys):
    Restaurante('Praça', 'Categoria')
    Restaurante('Pizza Suprema', 'Pizza')

    listar_restaurantes()
    out = capsys.readouterr().out
    assert 'Nome' in out
    assert 'Categoria' in out
    assert 'Situação' in out
    assert 'Praça' in out
    assert 'Pizza Suprema' in out


def test_avaliar_restaurante_sucesso(monkeypatch, capsys):
    r = Restaurante('X', 'Y')
    inputs = iter(['X', '4.5', 'Alice'])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

    avaliar_restaurante()
    out = capsys.readouterr().out.lower()
    assert 'avaliação registrada para' in out
    assert r.media_avaliacoes == 4.5


def test_avaliar_restaurante_invalida(monkeypatch, capsys):
    r = Restaurante('X', 'Y')  # noqa: F841
    inputs = iter(['X', '6', ''])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

    avaliar_restaurante()
    out = capsys.readouterr().out.lower()
    assert 'erro' in out


def test_avaliar_restaurante_nao_existente(monkeypatch, capsys):
    inputs = iter(['Foo'])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

    avaliar_restaurante()
    out = capsys.readouterr().out.lower()
    assert 'não está cadastrado' in out


def test_main_finalizar(monkeypatch):
    chamadas = {}
    # stub clear
    monkeypatch.setattr(
        os, 'system', lambda cmd: chamadas.setdefault('clear', True)
    )
    import app
    monkeypatch.setattr(
        app, 'exibir_nome_app', lambda: chamadas.setdefault('nome_app', True)
    )
    monkeypatch.setattr(
        app, 'exibir_opcoes', lambda: chamadas.setdefault('opcoes', True)
    )
    # primeira chamada de input: menu; retorna '5' para sair
    monkeypatch.setattr(builtins, 'input', lambda prompt='': '5')
    # captura o sub-título de finalização
    monkeypatch.setattr(
        app,
        'exibir_subtitulo',
        lambda txt: chamadas.setdefault('finalizando', txt)
    )

    main()
    assert chamadas == {
        'clear': True,
        'nome_app': True,
        'opcoes': True,
        'finalizando': 'Finalizando app'
    }


@pytest.mark.parametrize('entrada, stub_attr, key', [
    ('1', 'cadastrar_restaurante', 'cadastrar'),
    ('2', 'listar_restaurantes', 'listar'),
    ('3', 'alternar_estado_restaurante', 'alternar'),
    ('4', 'avaliar_restaurante', 'avaliar'),
    ('5', 'exibir_subtitulo', 'finalizando'),
])
def test_main_opcoes(monkeypatch, entrada, stub_attr, key):
    chamadas = {}
    # stub clear
    monkeypatch.setattr(
        os, 'system', lambda cmd: chamadas.setdefault('clear', True)
    )
    import app
    monkeypatch.setattr(
        app, 'exibir_nome_app', lambda: chamadas.setdefault('nome_app', True)
    )
    monkeypatch.setattr(
        app, 'exibir_opcoes', lambda: chamadas.setdefault('opcoes', True)
    )
    # Prepara inputs: escolha a opção e depois sai
    inputs = iter([entrada, '', '5'])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))
    # stub da operação escolhida
    monkeypatch.setattr(app, stub_attr, lambda: chamadas.setdefault(key, True))
    # stub finalizacao para sair sem erro
    monkeypatch.setattr(
        app,
        'exibir_subtitulo', lambda
        txt: chamadas.setdefault('finalizando', txt)
    )

    main()
    expected = {
        'clear': True,
        'nome_app': True,
        'opcoes': True,
        key: True,
        'finalizando': 'Finalizando app'
    }
    assert chamadas == expected
