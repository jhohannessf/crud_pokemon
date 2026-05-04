from typing import List
from pydantic import BaseModel, HttpUrl, ConfigDict


# Schema que representa o tipo do Pokemon (ex: fire, water)
class PokemonType(BaseModel):
    name: str       # nome do tipo (ex: "fire")
    url: HttpUrl    # url do tipo na PokeAPI

# Schema que representa as habilidades do Pokemon (ex: overgrow, chlorophyll)
class PokemonAbilities(BaseModel):
    name: str       # nome da Habilidade (ex: "overgrow")
    url: HttpUrl    # url do Move na PokeAPI


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
    id: int                             # ID na Pokedex
    name: str                           # nome do Pokémon
    types: List[PokemonType]            # lista de tipos do Pokémon
    abilities: List[PokemonAbilities]   #lista de habilidades do Pokémon
    moves: List[PokemonMove]            # lista de golpes do Pokémon
    weight: int                         # peso do Pokémon
    height: int                         # altura do Pokémon
    sprites: PokemonSprite              # imagens do Pokémon

    # Configuração do Pydantic v2 — permite converter objetos ORM em schema
    model_config = ConfigDict(from_attributes=True)