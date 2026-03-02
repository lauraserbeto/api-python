# API FastAPI com SQLAlchemy

## Tecnologias Utilizadas

- **Linguagem:** Python (v3.10+)
- **Framework:** FastAPI
- **ORM:** SQLAlchemy (v2.x)
- **Banco de Dados:** SQLite

## Dependências

- fastapi
- uvicorn
- sqlalchemy
- pydantic

## Como rodar o projeto localmente
### 1️⃣ Clone o repositório
```bash
git clone <url-do-seu-repositorio>
```

### 2️⃣ Acesse a pasta do projeto
```bash
cd nome-da-pasta
```

### 3️⃣ Ative o ambiente virtual

Windows:
```bash
.\venv\Scripts\activate
```
Mac/Linux:
```bash
source venv/bin/activate
```

### 4️⃣ Instale as dependências

```bash
pip install fastapi pydantic sqlalchemy uvicorn
```

### 5️⃣ Inicie o servidor

```bash
uvicorn main:app --reload --port 8000
```

## Acesso à API

A API estará disponível em:

http://localhost:8000

## Documentação Interativa

Acesse no navegador:

http://localhost:8000/docs

