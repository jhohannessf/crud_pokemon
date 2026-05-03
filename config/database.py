from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# carrega as variáveis do arquivo .env
load_dotenv()

# lê a URL do banco da variável de ambiente
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


def create_database_if_not_exists():
    """Conecta no banco padrão 'postgres' e cria o banco definido no .env se não existir."""

    # extrai o nome do banco do final da URL
    # ex: "postgresql://postgres:1234@localhost:5432/crud_pokemon" → "crud_pokemon"
    db_name = SQLALCHEMY_DATABASE_URI.rsplit("/", 1)[1]

    # troca o nome do banco na URL para 'postgres' (banco padrão que sempre existe)
    default_url = SQLALCHEMY_DATABASE_URI.rsplit("/", 1)[0] + "/postgres"

    # autocommit=True é necessário para criar banco fora de uma transação
    default_engine = create_engine(default_url, isolation_level="AUTOCOMMIT")

    with default_engine.connect() as conn:
        # verifica se o banco já existe usando o nome extraído do .env
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": db_name}
        )
        exists = result.fetchone()

        if not exists:
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"✅ Banco '{db_name}' criado com sucesso!")
        else:
            print(f"✅ Banco '{db_name}' já existe, seguindo...")

    default_engine.dispose()


# cria o banco se não existir antes de conectar
create_database_if_not_exists()

# só agora cria o engine — banco já existe garantidamente
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# classe para modelos
Base = declarative_base()

# sessão que será injetada nas rotas
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