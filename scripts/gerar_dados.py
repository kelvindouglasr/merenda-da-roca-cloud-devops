"""Gera os arquivos JSON usados pelo site a partir da base do projeto de Data Viz.

Fonte: GS_2TSCPW_DataViz_MerendaDaRoca_RaizDigital.csv (FNDE/PNAE 2011-2022 + IBGE Censo 2022).

Uso: python scripts/gerar_dados.py <caminho_do_csv>
"""
import json
import sys
from pathlib import Path

import pandas as pd

CSV = sys.argv[1]
SAIDA = Path(__file__).resolve().parent.parent / "data"
SAIDA.mkdir(exist_ok=True)

base = pd.read_csv(CSV, sep=";", decimal=",", encoding="utf-8-sig")
validos = base[base["flag_inconsistencia"].eq("NAO")]
municipal = validos[validos["esfera"].eq("MUNICIPAL")]


def resumo(g):
    return {
        "entidades": int(len(g)),
        "valor_transferido": round(float(g["valor_transferido_fnde"].sum()), 2),
        "valor_aquisicao_af": round(float(g["valor_aquisicao_af"].sum()), 2),
        "perc_af": round(float(g["valor_aquisicao_af"].sum() / g["valor_transferido_fnde"].sum()), 4),
        "perc_abaixo_30": round(float((g["perc_af"] < 0.30).mean()), 4),
        "perc_abaixo_45": round(float((g["perc_af"] < 0.45).mean()), 4),
    }


ULTIMO = int(base["ano"].max())
m22 = municipal[municipal["ano"].eq(ULTIMO)]

serie = [{"ano": int(a), "regiao": "Brasil", **resumo(g)} for a, g in validos.groupby("ano")]
serie += [{"ano": int(a), "regiao": r, **resumo(g)} for (a, r), g in validos.groupby(["ano", "regiao"])]

regioes = [{"regiao": r, **resumo(g)} for r, g in m22.groupby("regiao")]
ufs = [{"regiao": r, "uf": u, **resumo(g)} for (r, u), g in m22.groupby(["regiao", "uf"])]

faixas = m22["faixa_meta"].value_counts().to_dict()

dados = {
    "ano_referencia": ULTIMO,
    "brasil": resumo(m22),
    "faixas": {k: int(v) for k, v in faixas.items()},
    "serie": serie,
    "regioes": sorted(regioes, key=lambda x: x["perc_abaixo_45"], reverse=True),
    "ufs": sorted(ufs, key=lambda x: x["perc_abaixo_45"], reverse=True),
}
(SAIDA / "resumo.json").write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")

mun = m22.dropna(subset=["municipio"]).sort_values(["uf", "municipio"])
municipios = [
    {
        "municipio": r.municipio,
        "uf": r.uf,
        "regiao": r.regiao,
        "populacao": int(r.populacao_2022) if pd.notna(r.populacao_2022) else None,
        "transferido": round(float(r.valor_transferido_fnde), 2),
        "aquisicao_af": round(float(r.valor_aquisicao_af), 2),
        "perc_af": round(float(r.perc_af), 4),
        "faixa": r.faixa_meta,
    }
    for r in mun.itertuples()
]
(SAIDA / "municipios.json").write_text(json.dumps(municipios, ensure_ascii=False), encoding="utf-8")

print(f"ano {ULTIMO}: {len(municipios)} municipios, {len(ufs)} UFs, {len(serie)} pontos de serie")
print("brasil:", dados["brasil"])
print("faixas:", dados["faixas"])
