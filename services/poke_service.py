import httpx
from typing import List, Dict, Any

POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon"


class PokeAPIError(RuntimeError):
    """Erro genérico ao communicating com a PokéAPI."""


async def fetch_pokemon(identifier: str) -> Dict[str, Any]:
    """
    Busca informações de um Pokémon na PokéAPI.

    Parameters
    ----------
    identifier: str
        Nome ou id do Pokémon (ex.: "pikachu" ou "25").

    Returns
    -------
    dict
        Dados brutos retornados pela PokéAPI.

    Raises
    ------
    PokeAPIError
        Se a chamada falhar (404, timeout, etc.).
    """
    url = f"{POKEAPI_BASE}/{identifier}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)

    if response.status_code == 404:
        raise PokeAPIError(f"Pokémon '{identifier}' não encontrado.")
    if response.is_error:
        raise PokeAPIError(
            f"Erro ao consultar PokéAPI: {response.status_code} – {response.text}"
        )
    return response.json()
