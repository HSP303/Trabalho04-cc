from api.app import create_app


def test_get_alertas_returns_200():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/alertas")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert isinstance(payload["data"], list)


def test_get_alertas_has_expected_structure():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/alertas")

    payload = response.get_json()
    alertas = payload["data"]
    primeiro = alertas[0]

    assert len(alertas) >= 10
    assert {
        "id",
        "camera",
        "local",
        "setor",
        "tipo_evento",
        "severidade",
        "data_hora",
        "status",
        "descricao",
    }.issubset(primeiro)


def test_get_alerta_inexistente_returns_404():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/alertas/999")

    assert response.status_code == 404
    payload = response.get_json()
    assert payload["success"] is False
    assert payload["error"]["message"] == "Alerta nao encontrado."


def test_get_status_returns_expected_metadata():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/status")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["nome"] == "Central de Videomonitoramento"
    assert payload["data"]["versao"] == "1.0.0"
    assert payload["data"]["status"] == "operacional"
