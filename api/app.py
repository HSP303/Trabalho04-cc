from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify


APP_NAME = "Central de Videomonitoramento"
APP_VERSION = "1.0.0"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["APP_NAME"] = APP_NAME
    app.config["APP_VERSION"] = APP_VERSION
    app.config["DATA_FILE"] = Path(__file__).resolve().parent / "data" / "alertas.json"

    @app.get("/status")
    def status() -> tuple:
        payload = {
            "success": True,
            "data": {
                "nome": app.config["APP_NAME"],
                "versao": app.config["APP_VERSION"],
                "status": "operacional",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "error": None,
        }
        return jsonify(payload), 200

    @app.get("/alertas")
    def listar_alertas() -> tuple:
        try:
            alertas = load_alertas(app.config["DATA_FILE"])
        except Exception as exc:  # pragma: no cover - defensive path
            return error_response(
                "Falha ao carregar os alertas.",
                details=str(exc),
                status_code=500,
            )

        return success_response(alertas, status_code=200)

    @app.get("/alertas/<int:alerta_id>")
    def detalhe_alerta(alerta_id: int) -> tuple:
        try:
            alertas = load_alertas(app.config["DATA_FILE"])
        except Exception as exc:  # pragma: no cover - defensive path
            return error_response(
                "Falha ao carregar o alerta solicitado.",
                details=str(exc),
                status_code=500,
            )

        alerta = next((item for item in alertas if item["id"] == alerta_id), None)
        if alerta is None:
            return error_response(
                "Alerta nao encontrado.",
                details=f"ID {alerta_id} inexistente.",
                status_code=404,
            )

        return success_response(alerta, status_code=200)

    return app


def load_alertas(data_file: Path) -> list[dict]:
    with data_file.open("r", encoding="utf-8") as file:
        alertas = json.load(file)

    if not isinstance(alertas, list):
        raise ValueError("O arquivo de dados deve conter uma lista de alertas.")

    return alertas


def success_response(data: object, status_code: int = 200) -> tuple:
    return jsonify({"success": True, "data": data, "error": None}), status_code


def error_response(message: str, details: str | None, status_code: int) -> tuple:
    return (
        jsonify(
            {
                "success": False,
                "data": None,
                "error": {"message": message, "details": details},
            }
        ),
        status_code,
    )


app = create_app()
