import pytest

from app import app, falta_para_meta


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_painel_inicial(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Merenda da Roça" in r.get_data(as_text=True)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_busca_municipio_por_uf(client):
    r = client.get("/municipios?uf=PI")
    html = r.get_data(as_text=True)
    assert r.status_code == 200
    assert "Teresina" in html


def test_pagina_do_municipio(client):
    r = client.get("/municipio/PI/Teresina")
    assert r.status_code == 200
    assert "Teresina" in r.get_data(as_text=True)


def test_municipio_inexistente(client):
    assert client.get("/municipio/PI/Cidade-Que-Nao-Existe").status_code == 404


def test_api_resumo(client):
    dados = client.get("/api/resumo").get_json()
    assert dados["ano_referencia"] == 2022
    assert 0 < dados["brasil"]["perc_af"] < 1


def test_falta_para_meta():
    assert falta_para_meta({"transferido": 1000, "aquisicao_af": 200}) == 250
    assert falta_para_meta({"transferido": 1000, "aquisicao_af": 600}) == 0
