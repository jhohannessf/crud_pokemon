# 🐍 PokeAPI CRUD em Python v.1.0.1

Aplicação backend desenvolvida em Python com apoio de IA, que realiza operações de CRUD utilizando dados da PokeAPI, com persistência em banco de dados e organização em camadas.

---

## 📌 Descrição

Este projeto consome dados da PokeAPI e os armazena em um banco de dados, permitindo manipulação completa através de operações CRUD. A aplicação segue uma arquitetura organizada por responsabilidades.

---

## 🚀 Funcionalidades

- Consumo de dados da PokeAPI  
- Criação de registros no banco  
- Consulta de dados  
- Atualização de informações  
- Remoção de registros  

---

## 🛠️ Tecnologias

- Python 3.14  
- PostgreSQL 18.3
- SQLAlchemy
- FastAPI
- Alembic
- Pydantic v2
- Httpx
- Python-dotenv

---

## 📂 Estrutura do projeto


crud_pokemon/

├── .env                        ← variáveis de ambiente (não sobe pro Git)

├── .gitignore

├── main.py                     ← Ponto de entrada da aplicação

├── requirements.txt

├── alembic.ini

├── config/

│   └── database.py             ← cria banco automaticamente + engine PostgreSQL

├── models/

│   └── models.py               ← ORM + schemas Pydantic

├── schemas/

│   └── pokemon.py              ← Schema de resposta da PokéAPI

├── services/

│   └── poke_service.py         ← Comunicação com a PokéAPI

├── routes/

│   └── endpoints.py            ← Todos os endpoints CRUD

└── migrations/                 ← Arquivos do Alembic

    ├── env.py
    ├── script.py.mako
    ├── README
    └── versions/
        └── 7fbf9053edd8_criacao_inicial.py


## ⚙️ Instalação

# Clone o repositório
git clone https://github.com/jhohannessf/crud_pokemon.git

# Acesse a pasta
cd crud_pokemon

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente
1. Windows: 
venv\Scripts\activate
2. Linux/Mac: 
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Instale o Postgres
Necessário instalar o PosgreSQL para uso do serviço. No projeto estou usando a versão 18.3, junto com o Dbeaver.

# Arquivo .env
Necessário você criar o arquivo .env conforme suas variáveis de ambiente.

A estrutura da URL segue esse padrão:

DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco

Substituindo:

postgresql://  usuário  :  senha  @  host      :  porta  /  nome_do_banco

Exemplo:

postgresql://  postgres :  postgres   @  localhost  :  5432   /  crud_pokemon


## ▶️ Como iniciar o projeto 

uvicorn main:app --reload

## ▶️ Caso altere o models.py
Adicionar coluna, mudar tipo, criar nova tabela. 

Após a implementação do Alembic, não é mais necessário apagar o banco, apenas rodar os códigos abaixo:

1. Gera a migration

alembic revision --autogenerate -m "descricao do que mudou"

2. Aplica no banco

alembic upgrade head


## 📄 Docs da aplicação

Acesse o endereço no navegador: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
Aqui você terá informações de todos os métodos aceitos para consumo e manipulação dos dados.
Sugiro utilizar programas para consumo de API, pode ser o Insomnia ou Postman.

## 🔄 Como funciona o fluxo

1. A aplicação consome dados da PokeAPI
2. Os dados são tratados na camada de services
3. Os models representam a estrutura no banco
4. Os dados são validados via schemas
5. As operações CRUD são expostas via routes

## 📊 Exemplo de uso

As operações são executadas através das rotas definidas em:
routes/endpoints.py

## Exemplos de operações disponíveis:

### -> Consulte a DOC : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

1. Consultar Pokémon API (Método GET | URL: http://127.0.0.1:8000/api/v1/pokemon/{identifier})
2. Capturar Pokémon API (Método POST | URL: http://127.0.0.1:8000/api/v1/capture/pokemon/{identifier})
3. Criar Pokémon (Método POST | URL: http://127.0.0.1:8000/api/v1/create/pokemon/{identifier})
4. Listar um Pokémon (Método GET | URL: http://127.0.0.1:8000/api/v1/read/pokemon/{identifier})
5. Listar Pokémons capturado (Método GET | URL: http://127.0.0.1:8000/api/v1/read/pokemon/)
6. Atualizar dados (Método PATCH | URL: http://127.0.0.1:8000/api/v1/update/pokemon/{identifier})
7. Remover Pokémon (Método DELETE | URL: http://127.0.0.1:8000/api/v1/delete/pokemon/{identifier})

## Regras de negócio implementadas:

*   move_1 obrigatório na criação manual
*   Moves sorteados aleatoriamente sem repetição via sample
*   ability sorteada aleatoriamente via choice
*   PATCH valida ability contra abilities do pokemon
*   PATCH valida moves contra moves do pokemon
*   PATCH impede repetição de moves entre move_1 a move_4
*   Campos editáveis no PATCH: name, ability, move_1, move_2, move_3, move_4

## 🎯 Objetivo do projeto

1. Praticar consumo de API externa
2. Trabalhar com persistência de dados
3. Aplicar padrão de arquitetura em camadas
4. Simular um backend real
5. Evoluir boas práticas em Python

## 🔮 Melhorias futuras

1. Implementar testes com pytest
2. Dockerizar a aplicação
3. Implementar autenticação
4. Deploy em nuvem

## 📄 Licença

MIT License
