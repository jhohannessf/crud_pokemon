from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# carrega as variáveis do arquivo .env
load_dotenv()

# lê a URL do banco da variável de ambiente
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

# para PostgreSQL removemos o connect_args que era específico do SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URI)


def create_database_if_not_exists():
    """Conecta no banco padrão 'postgres' e cria o crud_pokemon se não existir."""

    # troca o nome do banco na URL para 'postgres' (banco padrão que sempre existe)
    default_url = SQLALCHEMY_DATABASE_URI.rsplit("/", 1)[0] + "/postgres"

    # autocommit=True é necessário para criar banco fora de uma transação
    default_engine = create_engine(default_url, isolation_level="AUTOCOMMIT")

    with default_engine.connect() as conn:
        # verifica se o banco já existe
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'crud_pokemon'")
        )
        exists = result.fetchone()

        if not exists:
            conn.execute(text("CREATE DATABASE crud_pokemon"))
            print("✅ Banco 'crud_pokemon' criado com sucesso!")
        else:
            print("✅ Banco 'crud_pokemon' já existe, seguindo...")

    default_engine.dispose()


# cria o banco se não existir antes de conectar
create_database_if_not_exists()

if "sqlite" in SQLALCHEMY_DATABASE_URI:
    engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
else:
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



