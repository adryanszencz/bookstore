# bookstore

[![Build e testes](https://github.com/adryanszencz/bookstore/actions/workflows/build.yml/badge.svg)](https://github.com/adryanszencz/bookstore/actions/workflows/build.yml)

API de uma livraria feita com Django e Django REST Framework, no curso Profissão: Desenvolvedor Full Stack Python da EBAC.

**Autor:** Adryan Szenczuk

## Como rodar

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Testes: `poetry run python manage.py test`

## Docker

```bash
docker build -t bookstore .
docker run -p 8000:8000 bookstore
```

A API fica em http://localhost:8000/bookstore/v1/products/

## Docker Compose (Django + Postgres)

```bash
docker compose up -d --build
docker compose exec web python manage.py test
```

As variáveis de desenvolvimento ficam em `env.dev`.

## Integração contínua (GitHub Actions)

- `build.yml`: em todo push na main e em todo PR, instala com Poetry, checa as migrações e roda os testes contra um Postgres.
- `code-review.yml`: em todo PR, o flake8 (via reviewdog) comenta no próprio PR as linhas fora do padrão.

## Deploy no PythonAnywhere

Publicado em https://adryanszencz.pythonanywhere.com/bookstore/v1/products/

No console Bash do PythonAnywhere:

```bash
git clone https://github.com/adryanszencz/bookstore.git
cd bookstore
python3.12 -m venv env && source env/bin/activate
pip install poetry && poetry config virtualenvs.create false && poetry install --no-root
python manage.py migrate && python manage.py collectstatic --noinput
```
