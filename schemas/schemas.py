from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, Union, List, Annotated


class ItemType(str, Enum):
    PRATO = "Prato"
    BEBIDA = "Bebida"
    SOBREMESA = "Sobremesa"


class CreateRestaurant(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        json_schema_extra={
            "example": {"nome": "Sabor & Cia", "categoria": "Brasileira"}
        },
    )

    nome: Annotated[str, Field(description="Nome do restaurante")]
    categoria: Annotated[str, Field(description="Categoria do restaurante")]


class Rating(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        json_schema_extra={"example": {"cliente": "João", "nota": 4.5}},
    )

    cliente: Annotated[str, Field(description="Nome do cliente")]
    nota: Annotated[float, Field(description="Nota de 1 a 5")]

    @model_validator(mode="after")
    def validar_nota(self):
        if not (1 <= self.nota <= 5):
            raise ValueError("a nota deve ser um número entre 1 e 5.")
        return self


class MenuItem(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        json_schema_extra={
            "example": {
                "type": "Sobremesa",
                "nome": "Sorvete de Chocolate",
                "preco": 10.95,
                "descricao": "Sorvete artesanal de chocolate belga",
                "tamanho": 150,
                "tipo": "Sorvete",
            }
        },
    )

    type: Annotated[ItemType, Field(description="Tipo do item")]
    nome: Annotated[str, Field(description="Nome do item")]
    preco: Annotated[float, Field(ge=0, description="Preço em reais")]
    descricao: Annotated[
        Optional[str],
        Field(None, description="Descrição do item (se aplicável)"),
    ]
    tamanho: Annotated[
        Optional[int], Field(None, description="Volume em ml (se aplicável)")
    ]
    tipo: Annotated[
        Optional[str],
        Field(None, description="Tipo da sobremesa (se aplicável)"),
    ]


class RestaurantSummary(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        json_schema_extra={
            "example": {
                "nome": "Sabor & Cia",
                "categoria": "Brasileira",
                "media_avaliacoes": 4.5,
                "ativo": True,
            }
        },
    )

    nome: Annotated[str, Field(description="Nome do restaurante")]
    categoria: Annotated[str, Field(description="Categoria do restaurante")]
    media_avaliacoes: Annotated[
        Union[float, str],
        Field(description="Média das avaliações ou '-' se não houver"),
    ]
    ativo: Annotated[
        bool, Field(description="Indica se o restaurante está ativo")
    ]


class AvaliacaoSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        json_schema_extra={"example": {"cliente": "Zé", "nota": 2}},
    )

    cliente: Annotated[str, Field(description="Nome do cliente")]
    nota: Annotated[float, Field(description="Nota de 1 a 5")]


class CardapioItemSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        json_schema_extra={
            "example": {
                "__type__": "Bebida",
                "nome": "Suco de Melancia",
                "preco": 4.6,
                "descricao": "O melhor pão da cidade",
                "tamanho": "grande",
                "tipo": "Doce",
            }
        },
    )

    type_: Annotated[
        ItemType, Field(alias="__type__", description="Tipo do item")
    ]
    nome: Annotated[str, Field(description="Nome do item")]
    preco: Annotated[Union[int, float], Field(description="Preço do item")]
    descricao: Annotated[
        Optional[str],
        Field(None, description="Descrição do item (se aplicável)"),
    ]
    tamanho: Annotated[
        Optional[Union[int, str]], Field(None, description="Tamanho ou volume")
    ]
    tipo: Annotated[
        Optional[str], Field(None, description="Tipo de sobremesa")
    ]


class RestaurantDetail(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        json_schema_extra={
            "example": {
                "nome": "praça",
                "categoria": "Gourmet",
                "ativo": True,
                "avaliacoes": [{"cliente": "Zé", "nota": 2}],
                "cardapio": [
                    {
                        "__type__": "Bebida",
                        "nome": "Suco de Melancia",
                        "preco": 4.6,
                        "tamanho": "grande",
                    },
                    {
                        "__type__": "Prato",
                        "nome": "Pãozinho",
                        "preco": 1.9,
                        "descricao": "O melhor pão da cidade",
                    },
                    {
                        "__type__": "Sobremesa",
                        "nome": "Sorvete de Chocolate",
                        "preco": 10.96,
                        "descricao": "Sorvete artesanal de chocolate belga",
                        "tipo": "Sorvete",
                        "tamanho": "Médio",
                    },
                ],
            }
        },
    )

    nome: Annotated[str, Field(description="Nome do restaurante")]
    categoria: Annotated[str, Field(description="Categoria do restaurante")]
    ativo: Annotated[
        bool, Field(description="Indica se o restaurante está ativo")
    ]
    avaliacoes: Annotated[
        List[AvaliacaoSchema],
        Field(description="Lista de avaliações do restaurante"),
    ]
    cardapio: Annotated[
        List[CardapioItemSchema],
        Field(description="Itens do cardápio do restaurante"),
    ]
