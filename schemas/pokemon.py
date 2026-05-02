from typing import List
from pydantic import BaseModel, HttpUrl, ConfigDict


# Schema que representa o tipo do Pokemon (ex: fire, water)
class PokemonType(BaseModel):
    name: str       # nome do tipo (ex: "fire")
    url: HttpUrl    # url do tipo na PokeAPI

# Schema que representa o Move do Pokemon (ex: fire, water)
class PokemonMove(BaseModel):
    name: str       # nome do Move (ex: "fire-punch")
    url: HttpUrl    # url do Move na PokeAPI

# Schema que representa as imagens do Pokemon
class PokemonSprite(BaseModel):
    front_default: HttpUrl | None = None  # imagem frontal padrão (pode ser nula)
    other: dict | None = None             # outras imagens (opcional, pode expandir)


# Schema principal de resposta da nossa API
# Define quais campos da PokeAPI vamos retornar ao usuário
class PokemonInfo(BaseModel):
    id: int                         # ID na Pokédex
    name: str                       # nome do Pokemon
    weight: int                     # peso do Pokemon
    height: int                     # altura do Pokemon
    types: List[PokemonType]        # lista de tipos
    sprites: PokemonSprite          # imagens do Pokemon
    moves_all: List[PokemonMove]    # lista de golpes do pokemon

    # Configuração do Pydantic v2 — permite converter objetos ORM em schema
    model_config = ConfigDict(from_attributes=True)