from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# carrega as variáveis do arquivo .env
load_dotenv()

# lê a URL do banco da variável de ambiente
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

# para PostgreSQL removemos o connect_args que era específico do SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Classe para modelos
Base = declarative_base()

# Sessão que será injetada nas rotas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependência FastAPI que fornece uma sessão."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Cria as tabelas a partir dos modelos."""
    Base.metadata.create_all(bind=engine)



