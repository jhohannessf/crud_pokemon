from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite local (troque a URL caso queira Postgres, MySQL etc.)
SQLALCHEMY_DATABASE_URI = 'sqlite:///./crud_pokemon.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

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



