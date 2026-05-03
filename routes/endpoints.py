from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session
from typing import List
from random import sample, choice

import models.models as models
import config.database as database
from services.poke_service import fetch_pokemon, PokeAPIError
from schemas.pokemon import PokemonInfo, PokemonType, PokemonSprite, PokemonMove

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
        moves_all=[
            PokemonMove(name=m["move"]["name"], url=m["move"]["url"])
               for m in raw["moves"]],
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

    # extrai a lista de nomes de moves diretamente (sem juntar e separar)
    abilities_all_list = [a["ability"]["name"] for a in raw["abilities"]]

    # choice escolhe 1 elemento aleatório da lista
    # se tiver só 1 habilidade, retorna ela mesma
    abilitie_chosen = choice(abilities_all_list) if abilities_all_list else None

    # transforma a lista de stats em dicionário para facilitar o acesso
    # ex: {"hp": 45, "attack": 49, ...}
    stats = {s["stat"]["name"]: s["base_stat"] for s in raw["stats"]}

    # extrai todos os moves como string separada por vírgula (ex: "fire-punch, thunder-punch")
    moves_all = ", ".join(m["move"]["name"] for m in raw["moves"])

    # extrai a lista de nomes de moves diretamente (sem juntar e separar)
    moves_all_list = [m["move"]["name"] for m in raw["moves"]]

    # sample escolhe 4 elementos aleatórios SEM repetição
    # min(...) garante que funciona mesmo se o pokemon tiver menos de 4 moves
    moves_chosen = sample(moves_all_list, min(4, len(moves_all_list)))

    # distribui nos campos — usa None se não houver moves suficientes
    move_1 = moves_chosen[0] if len(moves_chosen) > 0 else None
    move_2 = moves_chosen[1] if len(moves_chosen) > 1 else None
    move_3 = moves_chosen[2] if len(moves_chosen) > 2 else None
    move_4 = moves_chosen[3] if len(moves_chosen) > 3 else None

    # cria o objeto ORM com todos os dados extraídos
    db_item = models.Item(
        id=raw["id"],
        name=raw["name"],
        type=tipos,
        abilitie_chosen=abilitie_chosen,
        abilities=abilities,
        hp=stats.get("hp"),
        attack=stats.get("attack"),
        defense=stats.get("defense"),
        special_attack=stats.get("special-attack"),    # atenção: chave com hífen na PokeAPI
        special_defense=stats.get("special-defense"),  # atenção: chave com hífen na PokeAPI
        speed=stats.get("speed"),
        moves_all=moves_all,
        move_1=move_1,
        move_2=move_2,
        move_3=move_3,
        move_4=move_4,

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

    update_data = item_in.dict(exclude_unset=True)

    # valida abilitie_chosen — deve estar dentro do campo abilities do pokémon
    if "abilitie_chosen" in update_data:
        abilities_disponiveis = [a.strip() for a in db_item.abilities.split(",")]
        if update_data["abilitie_chosen"] not in abilities_disponiveis:
            raise HTTPException(
                status_code=400,
                detail=f"Habilidade inválida. Disponíveis para esse pokemon: {abilities_disponiveis}"
            )

    # valida move_1, move_2, move_3, move_4 — devem estar dentro de moves_all do pokémon
    if db_item.moves_all:
        moves_disponiveis = [m.strip() for m in db_item.moves_all.split(",")]
        for move_field in ["move_1", "move_2", "move_3", "move_4"]:
            if move_field in update_data:
                if update_data[move_field] not in moves_disponiveis:
                    raise HTTPException(
                        status_code=400,
                        detail=f"{move_field} inválido. Escolha um move disponível em moves_all do pokemon"
                    )

    # valida que os 4 moves não se repetem entre si
    # cruza os moves novos (enviados) com os atuais (já no banco)
    moves_novos = [update_data[m] for m in ["move_1", "move_2", "move_3", "move_4"] if m in update_data]
    moves_atuais = [getattr(db_item, m) for m in ["move_1", "move_2", "move_3", "move_4"] if m not in update_data]
    todos_moves = [m for m in moves_novos + moves_atuais if m is not None]

    if len(todos_moves) != len(set(todos_moves)):
        raise HTTPException(
            status_code=400,
            detail="Os moves não podem se repetir entre move_1, move_2, move_3 e move_4"
        )

    # aplica apenas os campos permitidos — rejeita qualquer outro campo
    campos_permitidos = {"name", "abilitie_chosen", "move_1", "move_2", "move_3", "move_4"}
    for key, value in update_data.items():
        if key not in campos_permitidos:
            raise HTTPException(status_code=400, detail=f"Campo '{key}' não pode ser alterado")
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