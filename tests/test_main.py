# tests/test_main.py

import pytest
from fastapi.testclient import TestClient

from main import app
from modelos.restaurante import Restaurante

# Cria o cliente de testes
client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_state(monkeypatch, tmp_path):
    # Limpa memória de restaurantes
    Restaurante.restaurantes.clear()
    # Prepara um JSON vazio num diretório temporário
    data_dir = tmp_path / "tmp"
    data_dir.mkdir()
    file = data_dir / "restaurantes.json"
    file.write_text("[]")
    # Faz o cwd apontar para tmp_path para ARQUIVO_DADOS
    monkeypatch.chdir(str(tmp_path))
    yield


def test_pega_raiz():
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Bem-vindo à Saborexpress API!</h1>" in response.text
    assert '<a href="/docs">Swagger UI' in response.text
    assert '<a href="/redoc">ReDoc' in response.text


def test_lista_de_restaurantes_vazia():
    resp = client.get("/restaurants")
    assert resp.status_code == 200
    assert resp.json() == []


def test_cria_restaurante_e_lista_resumo():
    # Cria um restaurante
    resp = client.post("/restaurants", json={"nome": "X", "categoria": "Y"})
    assert resp.status_code == 201

    # Lista resumo
    resp = client.get("/restaurants/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) == 1
    assert data[0]["nome"] == "X"
    assert data[0]["categoria"] == "Y"
    assert data[0]["ativo"] is False
    assert data[0]["media_avaliacoes"] == "-"


def test_cria_restaurante_com_nome_duplicado():
    """
    Testa se não é possível cadastrar dois restaurantes com o mesmo nome.
    """
    # Primeira tentativa: criar restaurante com sucesso
    first = client.post(
        "/restaurants", json={"nome": "Sabor & Cia", "categoria": "Brasileira"}
    )
    assert first.status_code == 201
    assert first.json() == {
        "message": "Restaurante 'Sabor & Cia' cadastrado com sucesso."
    }

    # Segunda tentativa: usar o mesmo nome novamente
    second = client.post(
        "/restaurants", json={"nome": "Sabor & Cia", "categoria": "Italiana"}
    )

    # Verifica que o status code é 400 (Bad Request)
    assert second.status_code == 400

    # Verifica que a mensagem de erro está correta
    assert second.json() == {
        "detail": "O restaurante 'Sabor & Cia' já existe."
    }


def test_muda_situacao_restaurante_adiciona_nota_e_lista_detalhada():
    # Cria e ativa
    client.post("/restaurants", json={"nome": "A", "categoria": "C"})
    resp = client.patch("/restaurants/A/toggle")
    assert resp.status_code == 200
    assert "ativado" in resp.json()["message"].lower()

    # Avalia
    resp = client.post(
        "/restaurants/A/rating", json={"cliente": "Jo", "nota": 5}
    )
    assert resp.status_code == 200

    # Verifica detalhe completo
    resp = client.get("/restaurants")
    assert resp.status_code == 200
    detail = resp.json()[0]
    assert detail["avaliacoes"][0]["nota"] == 5
    assert detail["ativo"] is True


def test_muda_situacao_restaurante_inexistente():
    resp = client.patch("/restaurants/RestauranteInexistente/toggle")
    assert resp.status_code == 404
    assert resp.json() == {
        "detail": "Restaurante 'RestauranteInexistente' não encontrado."
    }


def test_adiciona_nota_restaurante_inexistente():
    resp = client.post(
        "/restaurants/RestauranteInexistente/rating",
        json={"cliente": "Pedro", "nota": 3},
    )

    assert resp.status_code == 404
    assert resp.json() == {
        "detail": "Restaurante 'RestauranteInexistente' não encontrado."
    }


def test_adiciona_nota_fora_do_faixa():
    # Cria restaurante de teste
    client.post(
        "/restaurants",
        json={"nome": "Test Grill", "categoria": "Churrascaria"},
    )

    # Tenta avaliar com nota maior que 5
    resp_high = client.post(
        "/restaurants/Test Grill/rating", json={"cliente": "Ana", "nota": 6}
    )
    assert resp_high.status_code == 422
    assert (
        resp_high.json()["detail"][0]["msg"]
        == "Value error, a nota deve ser um número entre 1 e 5."
    )

    # Tenta avaliar com nota menor que 1
    resp_low = client.post(
        "/restaurants/Test Grill/rating", json={"cliente": "Bruno", "nota": 0}
    )
    assert resp_low.status_code == 422
    assert (
        resp_low.json()["detail"][0]["msg"]
        == "Value error, a nota deve ser um número entre 1 e 5."
    )


def test_adiciona_e_pega_cardapio():
    # Cria um restaurante com itens no cardápio
    resp = client.post(
        "/restaurants",
        json={"nome": "Restaurante Teste", "categoria": "Teste"},
    )
    assert resp.status_code == 201

    # Adiciona itens ao cardápio
    menu_items = [
        {"type": "Prato", "nome": "Feijoada", "preco": 39.90},
        {"type": "Bebida", "nome": "Suco de Laranja", "preco": 5.90},
    ]
    for item in menu_items:
        resp = client.post("/restaurants/Restaurante Teste/menu", json=item)
        assert resp.status_code == 201

    # Obtém o cardápio do restaurante
    resp = client.get("/restaurants/Restaurante Teste/menu")
    assert resp.status_code == 200
    menu = resp.json()
    assert len(menu) == 2
    assert menu[0]["nome"] == "Feijoada"
    assert menu[1]["nome"] == "Suco de Laranja"


def test_adiciona_e_pega_cardapio_restaurante_inexistente():
    # Adiciona itens ao cardápio
    menu_item = {
        "type": "Prato",
        "nome": "Feijoada",
        "descricao": "Tradicional feijoada com carnes nobres",
        "preco": 39.90,
    }

    resp = client.post("/restaurants/Inexistente/menu", json=menu_item)
    assert resp.status_code == 404
    assert resp.json() == {
        "detail": "Restaurante 'Inexistente' não encontrado."
    }

    # Obtém o cardápio do restaurante
    resp = client.get("/restaurants/Inexistente/menu")
    assert resp.status_code == 404
    assert resp.json() == {
        "detail": "Restaurante 'Inexistente' não encontrado."
    }


def test_aplica_desconto_em_sobremesa():
    # Cria um restaurante
    resp = client.post(
        "/restaurants",
        json={"nome": "Juicy Burger", "categoria": "Hamburgueria"},
    )
    assert resp.status_code == 201

    # Adiciona um item ao cardápio
    new_item = {
        "nome": "Sorvete de Chocolate",
        "preco": 20.0,
        "type": "Sobremesa",
        "descricao": "Sorvete artesanal de chocolate belga",
        "tipo": "Sorvete",
        "tamanho": 150,
    }

    resp = client.post("/restaurants/Juicy Burger/menu", json=new_item)

    resp_before = client.get("/restaurants/Juicy Burger/menu")
    preco_before = resp_before.json()[0]["preco"]

    resp = client.patch(
        "/restaurants/Juicy Burger/menu/Sorvete de Chocolate/discount"
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "Desconto aplicado" in body["message"]

    resp_after = client.get("/restaurants/Juicy Burger/menu")
    preco_after = resp_after.json()[0]["preco"]

    assert preco_after == pytest.approx(round(preco_before * 0.85, 2))


def test_aplica_desconto_em_bebida():
    # Cria um restaurante
    resp = client.post(
        "/restaurants", json={"nome": "Sucos & Cia", "categoria": "Sucos"}
    )
    assert resp.status_code == 201

    # Adiciona um item ao cardápio
    new_item = {
        "nome": "Suco de Melancia",
        "preco": 20.0,
        "type": "Bebida",
        "tamanho": 350,
    }

    resp = client.post("/restaurants/Sucos & Cia/menu", json=new_item)

    resp_before = client.get("/restaurants/Sucos & Cia/menu")
    preco_before = resp_before.json()[0]["preco"]

    resp = client.patch(
        "/restaurants/Sucos & Cia/menu/Suco de Melancia/discount"
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "Desconto aplicado" in body["message"]

    resp_after = client.get("/restaurants/Sucos & Cia/menu")
    preco_after = resp_after.json()[0]["preco"]

    assert preco_after == pytest.approx(round(preco_before * 0.92, 2))


def test_aplica_desconto_em_prato():
    # Cria um restaurante
    resp = client.post(
        "/restaurants", json={"nome": "Praça", "categoria": "Gourmet"}
    )
    assert resp.status_code == 201

    # Adiciona um item ao cardápio
    new_item = {
        "nome": "Pãozinho",
        "preco": 1.9,
        "type": "Prato",
        "descricao": "O melhor pão da cidade",
    }

    resp = client.post("/restaurants/Praça/menu", json=new_item)

    resp_before = client.get("/restaurants/Praça/menu")
    preco_before = resp_before.json()[0]["preco"]

    resp = client.patch("/restaurants/Praça/menu/Pãozinho/discount")
    assert resp.status_code == 200
    body = resp.json()
    assert "Desconto aplicado" in body["message"]

    resp_after = client.get("/restaurants/Praça/menu")
    preco_after = resp_after.json()[0]["preco"]

    assert preco_after == pytest.approx(round(preco_before * 0.95, 2))


def test_aplica_desconto_em_restaurante_inexistente():
    resp = client.patch("/restaurants/Inexistente/menu/Inexistente/discount")
    assert resp.status_code == 404
    assert resp.json() == {
        "detail": "Restaurante 'Inexistente' não encontrado."
    }


def test_aplica_desconto_em_item_inexistente():
    # Cria um restaurante
    resp = client.post(
        "/restaurants", json={"nome": "Praça", "categoria": "Gourmet"}
    )
    assert resp.status_code == 201

    resp = client.patch("/restaurants/Praça/menu/Inexistente/discount")
    assert resp.status_code == 404
    assert resp.json() == {
        "detail": "Item 'Inexistente' não encontrado em 'Praça'."
    }
