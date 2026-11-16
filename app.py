"""Merenda da Roça - Painel da Prefeitura (Equipe Raiz Digital).

Aplicação Flask que mostra quanto cada município comprou da agricultura familiar
com a verba da merenda escolar (PNAE) e quanto falta para a meta de 45%.
"""
import json
import os
import unicodedata
from functools import lru_cache
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
META_ANTIGA = 0.30
META_NOVA = 0.45
VERSAO = os.environ.get("APP_VERSION", "1.0.0")

app = Flask(__name__)


@lru_cache(maxsize=None)
def carregar(nome):
    return json.loads((DATA_DIR / nome).read_text(encoding="utf-8"))


def sem_acento(texto):
    texto = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return texto.lower().strip()


def falta_para_meta(mun, meta=META_NOVA):
    """Quanto em R$ o município ainda precisaria comprar da agricultura familiar."""
    return max(0.0, round(mun["transferido"] * meta - mun["aquisicao_af"], 2))


@app.template_filter("reais")
def reais(valor):
    texto = f"{valor:,.0f}".replace(",", ".")
    return f"R$ {texto}"


@app.template_filter("milhoes")
def milhoes(valor):
    return f"R$ {valor / 1e6:,.1f} mi".replace(",", "X").replace(".", ",").replace("X", ".")


@app.template_filter("pct")
def pct(valor):
    return f"{valor * 100:.1f}%".replace(".", ",")


@app.context_processor
def contexto_global():
    return {"versao": VERSAO, "meta_nova": META_NOVA, "meta_antiga": META_ANTIGA}


@app.route("/")
def inicio():
    resumo = carregar("resumo.json")
    serie_br = [s for s in resumo["serie"] if s["regiao"] == "Brasil"]
    return render_template("index.html", r=resumo, serie=serie_br)


@app.route("/municipios")
def municipios():
    lista = carregar("municipios.json")
    resumo = carregar("resumo.json")
    uf = request.args.get("uf", "").upper()
    busca = sem_acento(request.args.get("q", ""))
    faixa = request.args.get("faixa", "")
    filtrados = [
        m for m in lista
        if (not uf or m["uf"] == uf)
        and (not busca or busca in sem_acento(m["municipio"]))
        and (not faixa or m["faixa"] == faixa)
    ]
    filtrados = sorted(filtrados, key=lambda m: m["perc_af"])
    ufs = sorted({m["uf"] for m in lista})
    faixas = list(resumo["faixas"].keys())
    return render_template(
        "municipios.html", municipios=filtrados[:200], total=len(filtrados),
        ufs=ufs, faixas=faixas, uf=uf, q=request.args.get("q", ""), faixa=faixa,
        falta=falta_para_meta,
    )


@app.route("/municipio/<uf>/<nome>")
def municipio(uf, nome):
    alvo = sem_acento(nome)
    for m in carregar("municipios.json"):
        if m["uf"] == uf.upper() and sem_acento(m["municipio"]) == alvo:
            return render_template("municipio.html", m=m, falta=falta_para_meta(m),
                                   falta30=falta_para_meta(m, META_ANTIGA))
    abort(404)


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/api/resumo")
def api_resumo():
    return jsonify(carregar("resumo.json"))


@app.route("/health")
def health():
    return jsonify(status="ok", app="merenda-da-roca", versao=VERSAO)


@app.errorhandler(404)
def nao_encontrado(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
