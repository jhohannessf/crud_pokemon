🐍 PokeAPI CRUD em Python

Aplicação backend desenvolvida em Python que realiza operações de CRUD utilizando dados da PokeAPI, com persistência em banco de dados e organização em camadas (config, models, services, routes e schemas).

📌 Descrição

Este projeto consome dados da PokeAPI e os armazena em um banco de dados, permitindo manipulação completa através de operações CRUD. A aplicação foi estruturada seguindo boas práticas de separação de responsabilidades, simulando um ambiente real de desenvolvimento backend.

🚀 Funcionalidades

🔍 Consumo de dados da PokeAPI
📝 Criação de registros no banco
📖 Consulta de dados armazenados
✏️ Atualização de informações
❌ Remoção de registros
🔄 Tratamento e organização dos dados

🛠️ Tecnologias utilizadas

Python 3.x
Requests
SQLite
SQLAlchemy
FastAPI 

📂 Estrutura do projeto

crud_pokemon/
│
├── main.py                  # Ponto de entrada da aplicação
├── requirements.txt         # Dependências do projeto
│
├── config/
│   └── database.py          # Configuração da conexão com banco
│
├── models/
│   └── models.py            # Modelos/tabelas do banco de dados
│
├── schemas/
│   └── pokemon.py           # Schemas de validação de dados
│
├── services/
│   └── poke_service.py      # Regras de negócio e integração com API
│
├── routes/
│   └── endpoints.py         # Definição das rotas (CRUD)

⚙️ Instalação

# Clone o repositório
git clone https://github.com/jhohannessf/crud_pokemon.git

# Acesse a pasta
cd crud_pokemon

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

▶️ Como executar

uvicorn main:app --reload

🔄 Como funciona o fluxo

A aplicação consome dados da PokeAPI
Os dados são tratados na camada de services
Os models representam a estrutura no banco
Os dados são validados via schemas
As operações CRUD são expostas via routes

📊 Exemplo de uso

As operações são executadas através das rotas definidas em:
routes/endpoints.py

Exemplos de operações disponíveis:

Consultar Pokémon API
Capturar Pokémon API
Criar Pokémon
Listar um Pokémon
Listar Pokémons capturado
Atualizar dados
Remover Pokémon

🎯 Objetivo do projeto

Praticar consumo de API externa
Trabalhar com persistência de dados
Aplicar padrão de arquitetura em camadas
Simular um backend real
Evoluir boas práticas em Python

🔮 Melhorias futuras

Criar API REST completa com FastAPI
Adicionar documentação automática (Swagger)
Implementar testes com pytest
Dockerizar a aplicação
Implementar autenticação
Deploy em nuvem

📄 Licença

MIT License
