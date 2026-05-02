# 🐍 PokeAPI CRUD em Python

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
- SQLite
- SQLAlchemy
- FastAPI

---

## 📂 Estrutura do projeto


crud_pokemon /


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

## ▶️ Como executar

uvicorn main:app --reload

## ▶️ Docs da aplicação

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
