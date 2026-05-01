from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session
from typing import List

import models.models as models
import config.database as database
from services.poke_service import fetch_pokemon, PokeAPIError
from schemas.pokemon import PokemonInfo, PokemonType, PokemonSprite

# APIRouter agrupa as rotas — é registrado no main.py via app.include_router()
router = APIRouter()


# ─────────────────────────────────────────────
# CONSULTAR POKEMON NA POKEAPI (sem salvar)
# ─────────────────────────────────────────────
@router.get("/pokemon/{identifier}", response_model=PokemonInfo,
            summary="Consulta um Pokemon disponível na PokeAPI",
            description="Consulta um Pokémon pelo ID Dex ou Nome. Exemplos: `25` para Pikachu, ou `pikachu`.")
async def get_pokemon(
    identifier: str = Path(description="Informe o **ID da Pokédex** ou **Nome**. Ex: `25` ou `pikachu`.")
):
    try:
        # chama o serviço que busca os dados na PokeAPI
        raw = await fetch_pokemon(identifier)
    except PokeAPIError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # monta o schema de resposta com os campos que nos interessam
    return PokemonInfo(
        id=raw["id"],
        name=raw["name"],
        weight=raw["weight"],
        height=raw["height"],
        types=[
            PokemonType(name=t["type"]["name"], url=t["type"]["url"])
            for t in raw["types"]
        ],
        sprites=PokemonSprite(front_default=raw["sprites"]["front_default"]),
    )


# ─────────────────────────────────────────────
# CAPTURAR POKEMON — busca na PokeAPI e salva no banco
# ─────────────────────────────────────────────
@router.post("/capture/pokemon/{identifier}", response_model=models.ItemRead, status_code=201,
             summary="Captura um Pokémon",
             description="Busca o Pokémon na PokeAPI e salva no banco de dados.")
async def save_pokemon(
    identifier: str = Path(description="Informe o **ID da Pokédex** ou **Nome**. Ex: `25` ou `pikachu`."),
    db: Session = Depends(database.get_db)
):
    try:
        raw = await fetch_pokemon(identifier)
    except PokeAPIError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    # verifica se o pokemon já foi capturado antes de salvar
    existe = db.query(models.Item).filter(models.Item.id == raw["id"]).first()
    if existe:
        raise HTTPException(status_code=409, detail="Pokémon já capturado!")

    # extrai os tipos como string separada por vírgula (ex: "fire, flying")
    tipos = ", ".join(t["type"]["name"] for t in raw["types"])

    # extrai as habilidades como string separada por vírgula (ex: "static, lightning-rod")
    abilities = ", ".join(a["ability"]["name"] for a in raw["abilities"])

    # transforma a lista de stats em dicionário para facilitar o acesso
    # ex: {"hp": 45, "attack": 49, ...}
    stats = {s["stat"]["name"]: s["base_stat"] for s in raw["stats"]}

    # cria o objeto ORM com todos os dados extraídos
    db_item = models.Item(
        id=raw["id"],
        name=raw["name"],
        type=tipos,
        abilities=abilities,
        hp=stats.get("hp"),
        attack=stats.get("attack"),
        defense=stats.get("defense"),
        special_attack=stats.get("special-attack"),    # atenção: chave com hífen na PokeAPI
        special_defense=stats.get("special-defense"),  # atenção: chave com hífen na PokeAPI
        speed=stats.get("speed")
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # atualiza o objeto com os dados persistidos no banco
    return db_item


# ─────────────────────────────────────────────
# CREATE — criação manual de um Pokemon no banco
# ─────────────────────────────────────────────
@router.post("/create/pokemon/{identifier}", response_model=models.ItemRead, status_code=status.HTTP_201_CREATED,
             summary="Cria um Pokémon manualmente",
             description="Cria um Pokémon manualmente pelo **ID da Pokédex** ou **Nome**.")
def create_item(
    identifier: str = Path(description="Nome ou ID do Pokémon. Ex: `pikachu` ou `25`"),
    item_in: models.ItemCreate = None,
    db: Session = Depends(database.get_db)
):
    # valida se o identifier bate com os dados do body enviado
    if identifier.isdigit():
        if item_in.id != int(identifier):
            raise HTTPException(status_code=400, detail="ID do identifier não corresponde ao ID do body")
    else:
        if item_in.name.lower() != identifier.lower():
            raise HTTPException(status_code=400, detail="Nome do identifier não corresponde ao nome do body")

    # verifica se já existe no banco para evitar duplicatas
    db_item = db.query(models.Item).filter(models.Item.id == item_in.id).first()
    if db_item:
        raise HTTPException(status_code=409, detail="Pokémon já cadastrado")

    # desempacota o schema como kwargs para criar o objeto ORM
    db_item = models.Item(**item_in.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ─────────────────────────────────────────────
# READ — busca um Pokemon pelo ID ou nome
# ─────────────────────────────────────────────
@router.get("/read/pokemon/{identifier}", response_model=models.ItemRead,
            summary="Busca um Pokémon capturado",
            description="Busca um Pokémon pelo **ID da Pokédex** ou **Nome**.")
def read_item(
    identifier: str = Path(description="Nome ou ID do Pokémon. Ex: `pikachu` ou `25`"),
    db: Session = Depends(database.get_db)
):
    # se for número busca por id, senão busca por nome
    if identifier.isdigit():
        db_item = db.query(models.Item).filter(models.Item.id == int(identifier)).first()
    else:
        db_item = db.query(models.Item).filter(models.Item.name == identifier.lower()).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Pokemon não encontrado")
    return db_item


# ─────────────────────────────────────────────
# READ ALL — lista todos os Pokemon capturados
# ─────────────────────────────────────────────
@router.get("/read/pokemon/", response_model=List[models.ItemRead],
            summary="Lista todos os Pokémon capturados",
            description="Retorna todos os Pokémon salvos no banco.")
def list_items(
    skip: int = 0,    # quantos registros pular (paginação)
    limit: int = 100, # quantidade máxima de registros retornados
    db: Session = Depends(database.get_db)
):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items


# ─────────────────────────────────────────────
# UPDATE — atualiza dados de um Pokemon capturado
# ─────────────────────────────────────────────
@router.patch("/update/pokemon/{identifier}", response_model=models.ItemRead,
              summary="Altera um Pokémon capturado",
              description="Altera um Pokémon pelo **ID da Pokédex** ou **Nome**.")
def update_item(
    identifier: str = Path(description="Nome ou ID do Pokémon. Ex: `pikachu` ou `25`"),
    item_in: models.ItemUpdate = None,
    db: Session = Depends(database.get_db)
):
    if identifier.isdigit():
        db_item = db.query(models.Item).filter(models.Item.id == int(identifier)).first()
    else:
        db_item = db.query(models.Item).filter(models.Item.name == identifier.lower()).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Pokemon não encontrado")

    # atualiza apenas os campos enviados no body (ignora os não enviados)
    for key, value in item_in.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ─────────────────────────────────────────────
# DELETE — remove um Pokemon do banco
# ─────────────────────────────────────────────
@router.delete("/delete/pokemon/{identifier}", response_model=dict,
               summary="Deleta um Pokémon capturado",
               description="Deleta um Pokémon pelo **ID da Pokédex** ou **Nome**.")
def delete_item(
    identifier: str = Path(description="Nome ou ID do Pokémon. Ex: `pikachu` ou `25`"),
    db: Session = Depends(database.get_db)
):
    if identifier.isdigit():
        db_item = db.query(models.Item).filter(models.Item.id == int(identifier)).first()
    else:
        db_item = db.query(models.Item).filter(models.Item.name == identifier.lower()).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Pokemon não encontrado")

    db.delete(db_item)
    db.commit()
    return {"mensagem": "O Pokemon foi deletado com sucesso!"}