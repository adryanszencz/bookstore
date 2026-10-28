# bookstore

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
