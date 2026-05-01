from typing import Optional
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict
from config.database import Base


# ─────────────────────────────────────────────
# MODELO ORM — representa a tabela no banco
# ─────────────────────────────────────────────
class Item(Base):
    __tablename__ = "pokemon"

    id             = Column(Integer, primary_key=True, index=True, autoincrement=False)  # ID da Pokédex (definido manualmente)
    name           = Column(String,  nullable=False)   # nome do Pokemon
    type           = Column(String,  nullable=False)   # tipos separados por vírgula (ex: "fire, flying")
    abilities      = Column(String,  nullable=False)   # habilidades separadas por vírgula
    hp             = Column(Integer, nullable=True)    # stat HP
    attack         = Column(Integer, nullable=True)    # stat Ataque
    defense        = Column(Integer, nullable=True)    # stat Defesa
    special_attack  = Column(Integer, nullable=True)   # stat Ataque Especial
    special_defense = Column(Integer, nullable=True)   # stat Defesa Especial
    speed          = Column(Integer, nullable=True)    # stat Velocidade

    # __init__ explícito necessário para aceitar kwargs (ex: Item(id=1, name="pikachu"))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# ─────────────────────────────────────────────
# SCHEMAS PYDANTIC — validação e serialização
# ─────────────────────────────────────────────

# Base compartilhada entre Create e Read
class ItemBase(BaseModel):
    id:              int
    name:            str
    type:            Optional[str] = None
    abilities:       Optional[str] = None
    hp:              Optional[int] = None
    attack:          Optional[int] = None
    defense:         Optional[int] = None
    special_attack:  Optional[int] = None
    special_defense: Optional[int] = None
    speed:           Optional[int] = None


# Schema usado no POST manual — herda todos os campos do ItemBase
class ItemCreate(ItemBase):
    pass


# Schema usado nas respostas — garante que o id sempre virá
# from_attributes permite converter o objeto ORM direto para este schema
class ItemRead(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Schema usado no PATCH — todos os campos são opcionais
# o dev pode enviar apenas o que quer alterar
class ItemUpdate(BaseModel):
    name:            Optional[str] = None
    type:            Optional[str] = None
    abilities:       Optional[str] = None
    hp:              Optional[int] = None
    attack:          Optional[int] = None
    defense:         Optional[int] = None
    special_attack:  Optional[int] = None
    special_defense: Optional[int] = None
    speed:           Optional[int] = None

    model_config = ConfigDict(from_attributes=True)