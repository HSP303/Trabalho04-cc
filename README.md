# Central de Videomonitoramento

API REST em Flask para o trabalho final de Cloud Computing.

## Objetivo

Simular uma central de videomonitoramento com:

- `GET /status`
- `GET /alertas`
- `GET /alertas/<id>`

Os dados ficam em arquivo JSON externo.

## Estrutura

```text
.
├── api/
│   ├── app.py
│   ├── data/
│   │   └── alertas.json
│   └── tests/
│       └── test_api.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Requisitos

- Python 3.12+
- Docker, se for executar por container

## Execucao local

1. Criar e ativar um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements-dev.txt
```

3. Rodar a API:

```bash
flask --app api.app run --debug
```

4. Acessar:

- `GET http://127.0.0.1:5000/status`
- `GET http://127.0.0.1:5000/alertas`
- `GET http://127.0.0.1:5000/alertas/1`

## Execucao com Docker

1. Gerar a imagem:

```bash
docker build -t central-videomonitoramento-api .
```

2. Executar o container:

```bash
docker run --rm -p 5000:5000 central-videomonitoramento-api
```

## Testes

```bash
pytest
```

## Lint

```bash
ruff check api
ruff format --check api
```

## Observacao sobre o tema

O recurso principal da API foi modelado como `alertas`, por ser coerente com uma
central de videomonitoramento e permitir uma simulacao realista de registros.

