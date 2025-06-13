# main.py

from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.responses import HTMLResponse
from typing import List, Dict, Type
from contextlib import asynccontextmanager


from modelos.restaurante import Restaurante
from modelos.cardapio.prato import Prato
from modelos.cardapio.bebida import Bebida
from modelos.cardapio.sobremesa import Sobremesa
from modelos.cardapio.item_cardapio import ItemCardapio
from schemas.schemas import (
    CreateRestaurant,
    Rating,
    MenuItem,
    RestaurantSummary,
    RestaurantDetail,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Restaurante.carregar_dados()
    yield
    Restaurante.salvar_dados()


app = FastAPI(lifespan=lifespan, title="Saborexpress API")


@app.post("/restaurants", status_code=201, summary="Cria restaurante")
async def create_restaurant(data: CreateRestaurant):
    if any(
        r._nome.lower() == data.nome.lower() for r in Restaurante.restaurantes
    ):
        raise HTTPException(
            status_code=400, detail=f"O restaurante '{data.nome}' já existe."
        )
    Restaurante(data.nome, data.categoria)
    Restaurante.salvar_dados()
    return {"message": f"Restaurante '{data.nome}' cadastrado com sucesso."}


@app.get(
    "/restaurants",
    response_model=List[RestaurantDetail],
    summary="Lista completa de restaurantes",
)
async def list_restaurants():
    def to_dict(r: Restaurante):
        return {
            "nome": r._nome,
            "categoria": r._categoria,
            "ativo": r._ativo,
            "avaliacoes": [
                {"cliente": a._cliente, "nota": a._nota} for a in r._avaliacao
            ],
            "cardapio": [item.to_dict() for item in r._cardapio],
        }

    return [to_dict(r) for r in Restaurante.restaurantes]


@app.get(
    "/restaurants/summary",
    response_model=List[RestaurantSummary],
    summary="Lista sumarizada de restaurantes",
)
async def summary_restaurants():
    """Retorna resumo (nome, categoria, situaçao e média de avaliações)"""
    return [
        {
            "nome": r._nome,
            "categoria": r._categoria,
            "ativo": r.ativo,
            "media_avaliacoes": r.media_avaliacoes,
        }
        for r in Restaurante.restaurantes
    ]


@app.patch(
    "/restaurants/{nome}/toggle",
    summary="Alterna estado do restaurante - 🟢 / 🔴",
)
async def toggle_restaurant(
    nome: str = Path(..., description="Nome do restaurante")
):
    for r in Restaurante.restaurantes:
        if r._nome.lower() == nome.lower():
            msg = r.alternar_estado()
            Restaurante.salvar_dados()
            return {"message": msg}
    raise HTTPException(
        status_code=404, detail=f"Restaurante '{nome}' não encontrado."
    )


@app.post("/restaurants/{nome}/rating", summary="Avalia restaurante")
async def rate_restaurant(
    nome: str = Path(..., description="Nome do restaurante"),
    rating: Rating = Body(...),
):
    # Validação antes de gravar
    if not (1 <= rating.nota <= 5):
        raise HTTPException(
            status_code=422,
            detail=["Value error, a nota deve ser um número entre 1 e 5."],
        )
    for r in Restaurante.restaurantes:
        if r._nome.lower() == nome.lower():
            # Registra a avaliação
            r.receber_avaliacao(rating.cliente, rating.nota)
            Restaurante.salvar_dados()
            return {"message": f"Avaliação registrada para '{nome}'."}
    raise HTTPException(
        status_code=404, detail=f"Restaurante '{nome}' não encontrado."
    )


@app.post(
    "/restaurants/{nome}/menu",
    status_code=201,
    summary="Adiciona item ao cardápio do restaurante",
)
async def add_menu_item(
    nome: str = Path(..., description="Nome do restaurante"),
    item: MenuItem = Body(...),
):
    for r in Restaurante.restaurantes:
        if r._nome.lower() == nome.lower():
            cls_map: Dict[str, Type[ItemCardapio]] = {
                "Prato": Prato,
                "Bebida": Bebida,
                "Sobremesa": Sobremesa,
            }
            cls_item = cls_map.get(item.type, ItemCardapio)
            # Cria um dicionário de kwargs baseado no tipo fornecido.
            data = item.model_dump()
            new_item = cls_item.from_dict({**data, "__type__": item.type})
            r.adicionar_ao_cardapio(new_item)
            return {
                "message": (
                    f"Item '{item.nome}' adicionado ao cardápio"
                    f" de '{nome}'."
                )
            }
    raise HTTPException(
        status_code=404, detail=f"Restaurante '{nome}' não encontrado."
    )


@app.get("/restaurants/{nome}/menu", summary="Obtém o cardápio do restaurante")
async def get_menu(nome: str = Path(..., description="Nome do restaurante")):
    for r in Restaurante.restaurantes:
        if r._nome.lower() == nome.lower():
            return [item.to_dict() for item in r._cardapio]
    raise HTTPException(
        status_code=404, detail=f"Restaurante '{nome}' não encontrado."
    )


@app.patch(
    "/restaurants/{nome}/menu/{item_nome}/discount",
    summary="Aplica desconto ao item do cardápio",
    response_model=dict,
    description="Aplica desconto ao item do cardápio do restaurante.",
)
async def apply_discount(
    nome: str = Path(..., description="Nome do restaurante"),
    item_nome: str = Path(..., description="Nome do item do cardápio"),
):
    for r in Restaurante.restaurantes:
        if r._nome.lower() == nome.lower():
            for item in r._cardapio:
                if item._nome.lower() == item_nome.lower():
                    item.aplicar_desconto()
                    Restaurante.salvar_dados()
                    return {
                        "message": (
                            f"Desconto aplicado em '{item_nome}'"
                            f" de '{nome}'."
                        ),
                        "item": item.to_dict(),
                    }
            raise HTTPException(
                status_code=404,
                detail=f"Item '{item_nome}' não encontrado em '{nome}'.",
            )
    raise HTTPException(
        status_code=404, detail=f"Restaurante '{nome}' não encontrado."
    )


@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <h1>Bem-vindo à Saborexpress API!</h1>
    <ul>
      <li><a href="/docs">Swagger UI (Documentação Interativa)</a></li>
      <li><a href="/redoc">ReDoc (Documentação Estática)</a></li>
    </ul>
    """
    return HTMLResponse(content=html_content)
