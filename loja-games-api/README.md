# Loja de Games API

API desenvolvida com FastAPI, SQLAlchemy e SQLite para gerenciar plataformas, jogos e avaliações.

## Como executar

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   ```

   Windows:

   ```bash
   venv\Scripts\activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Inicie a API:

   ```bash
   uvicorn main:app --reload
   ```

4. Abra a documentação interativa:

   http://127.0.0.1:8000/docs

O banco SQLite `loja_games.db` e as tabelas são criados automaticamente na primeira execução.

## Endpoints

### Plataformas
- `GET /plataformas/`
- `POST /plataformas/`

### Jogos
- `GET /jogos/`
- `GET /jogos/{id}`
- `POST /jogos/`
- `PUT /jogos/{id}`
- `DELETE /jogos/{id}`

### Avaliações
- `GET /jogos/{id}/avaliacoes`
- `POST /avaliacoes/`
- `DELETE /avaliacoes/{id}`

## Exemplos para testar no Swagger

Cadastre uma plataforma:

```json
{
  "nome": "PlayStation 5"
}
```

Cadastre um jogo (use o `id` retornado ao cadastrar a plataforma):

```json
{
  "titulo": "God of War Ragnarök",
  "genero": "Ação e aventura",
  "preco": 249.90,
  "plataforma_id": 1
}
```

Cadastre uma avaliação (use o `id` retornado ao cadastrar o jogo):

```json
{
  "nota": 5,
  "comentario": "Excelente jogo!",
  "jogo_id": 1
}
```

A nota é validada para aceitar somente valores inteiros de 1 a 5. O cadastro e a atualização de jogos verificam se a plataforma existe, e o cadastro de avaliações verifica se o jogo existe.
