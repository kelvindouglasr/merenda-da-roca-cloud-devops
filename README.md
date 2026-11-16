# Merenda da Roça 🌽

**Solução:** Merenda da Roça - Painel da Prefeitura
**Do pequeno produtor direto para o prato da escola.**

Global Solution 2026.2 · CitizenTech · Cloud Solutions & Scalable Infrastructure · Turma 2TSCPW · Equipe Raiz Digital

## Integrantes

| Nome | RM |
|---|---|
| Elton Vinicios Almeida de Oliveira | RM562187 |
| Emerson dos Santos Silva | RM562033 |
| Kelvin Douglas Ribeiro Rabelo | RM561538 |

## Descrição da solução

**Problema.** O PNAE repassa bilhões de reais por ano para a merenda escolar, e a lei obriga as prefeituras a
comprar parte desse valor da agricultura familiar: 30% até 2025 e **45% a partir de 2026** (Lei 15.226/2025).
Mesmo assim, em 2022, 57% das prefeituras do Brasil com dados válidos ficariam abaixo da nova meta. No Nordeste
são 69%. Muitos produtores não ficam sabendo das chamadas públicas, e a nutricionista da prefeitura não sabe
quanto falta comprar nem de quem.

**Solução.** A Merenda da Roça conecta agricultores familiares às compras da merenda escolar. Este repositório
contém o **Painel da Prefeitura**, uma aplicação web publicada na Azure que:

- mostra os indicadores do Brasil e por região (quanto da verba foi comprado da agricultura familiar);
- permite buscar qualquer município por nome, UF e faixa da meta;
- mostra, para cada município, **quanto falta em reais** para cumprir a meta de 45%;
- expõe uma API (`/api/resumo`) e um endpoint de saúde (`/health`) para o monitoramento do deploy.

Os dados vêm das planilhas oficiais do FNDE (aquisições da agricultura familiar no PNAE, 2011 a 2022)
e do IBGE (população do Censo 2022).

## Origem do projeto

**Reutilizado de outras disciplinas da própria equipe e adaptado para esta entrega.**
A base de dados e o recorte do problema foram criados pela equipe nas disciplinas de *BI e Data Viz* e
*Data Ethics & Governance* da mesma Global Solution (projeto Merenda da Roça). Para esta disciplina, a equipe
transformou a base em uma aplicação web nova em Flask, com identidade visual própria, e montou todo o fluxo
de DevOps no Azure DevOps.

## Tecnologias utilizadas

- **Python 3.12** e **Flask 3** (aplicação web), **Jinja2** (páginas), **Gunicorn** (servidor em produção)
- **pandas** (geração dos dados a partir da base do FNDE/IBGE, em `scripts/gerar_dados.py`)
- **pytest** (testes automatizados executados no pipeline)
- **Azure DevOps**: Boards, Repos e Pipelines
- **Azure App Service** (Web App Linux, Python 3.12)

## Estrutura

```
app.py                  aplicação Flask (rotas e regras da meta)
templates/              páginas HTML (painel, municípios, município, sobre)
static/style.css        identidade visual da Merenda da Roça
data/                   resumo.json e municipios.json gerados da base FNDE/IBGE
scripts/gerar_dados.py  gera a pasta data/ a partir do CSV da equipe
tests/test_app.py       testes automatizados
azure-pipelines.yml     pipeline de CI/CD
```

## Azure DevOps

### Azure Boards
Projeto `MerendaDaRoca` criado com o processo **Agile**. Foi criada a User Story
*"Como nutricionista de prefeitura, quero ver quanto meu município compra da agricultura familiar e quanto
falta para a meta de 45%"*, com descrição, critérios de aceite e responsável. Ela tem três Tasks filhas,
cada uma com título, descrição, responsável e status:

- **Task 01** · Personalizar a aplicação Merenda da Roça
- **Task 02** · Implementar CI/CD com Azure Pipelines e Web App
- **Task 03** · Documentar o projeto no README e reunir evidências

As tasks evoluíram no quadro de *New* → *Active* → *Closed* durante a atividade.

### Azure Repos
O Azure Repos é o repositório principal. A branch `main` guarda a versão publicada, e as alterações
são feitas na branch `feature/update-solution` e integradas à `main` por **Pull Request**. O histórico de
commits registra cada etapa.

### Azure Pipelines
O arquivo `azure-pipelines.yml` define dois estágios:

1. **CI - Build e testes:** instala as dependências, roda os testes com pytest, publica o resultado dos
   testes e empacota a aplicação em um `.zip` publicado como artefato.
2. **CD - Deploy:** baixa o artefato e publica no Azure Web App `merenda-da-roca-raizdigital` pela
   service connection `azure-merenda-da-roca`.

O pipeline roda em um **agente self-hosted** (pool `Default`), porque a organização não tem parallel jobs
hospedados pela Microsoft.

### CI/CD
Todo push ou merge na `main` dispara o pipeline automaticamente (trigger). Se os testes passam, o deploy
acontece sem intervenção manual. Para demonstrar, a equipe publicou a primeira versão e depois fez uma
alteração simples na branch `feature/update-solution`. A alteração foi integrada à `main` por Pull Request,
o pipeline rodou e o site publicado foi atualizado. A versão aparece no rodapé do site e em `/health`.

## Rodar localmente

```bash
pip install -r requirements.txt
python app.py
```

Acesse http://localhost:5000. Testes: `pip install pytest && python -m pytest`.
