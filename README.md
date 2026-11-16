# Merenda da Roça 🌽

**Nome do projeto:** Merenda da Roça
**Nome da solução:** Painel da Prefeitura - Merenda da Roça
**Slogan:** do pequeno produtor direto para o prato da escola.

Global Solution 2026.2 · CitizenTech · **Cloud Solutions & Scalable Infrastructure** · Turma 2TSCPW · Equipe Raiz Digital

| | |
|---|---|
| 🌐 Aplicação publicada | https://merenda-da-roca-raizdigital-g8hufxamgzd3cder.brazilsouth-01.azurewebsites.net |
| 🩺 Health check | https://merenda-da-roca-raizdigital-g8hufxamgzd3cder.brazilsouth-01.azurewebsites.net/health |
| 🛠️ Projeto no Azure DevOps | https://dev.azure.com/rm561538/MerendaDaRoca |

## Integrantes

| Nome | RM | Papel no Azure DevOps |
|---|---|---|
| Elton Vinicios Almeida de Oliveira | RM562187 | Responsável pela User Story e pela Task 03 (documentação e evidências) |
| Emerson dos Santos Silva | RM562033 | Responsável pela Task 02 (CI/CD com Azure Pipelines e Web App) |
| Kelvin Douglas Ribeiro Rabelo | RM561538 | Responsável pela Task 01 (personalização da aplicação) e administrador da organização |

## Descrição da solução

**Problema.** O PNAE (Programa Nacional de Alimentação Escolar) repassa bilhões de reais por ano para a
merenda, e a lei obriga as prefeituras a comprar parte desse valor da agricultura familiar: 30% até 2025 e
**45% a partir de 2026** (Lei 15.226/2025). Mesmo assim, em 2022, **57% das prefeituras** com dados válidos
ficariam abaixo da nova meta. No Nordeste são **69%**. O produtor familiar não fica sabendo das chamadas
públicas, e a nutricionista da prefeitura não sabe quanto falta comprar nem de quem.

**Solução.** A Merenda da Roça conecta agricultores familiares às compras da merenda escolar. Esta entrega
é o **Painel da Prefeitura**, uma aplicação web publicada na Azure que:

- mostra os indicadores do Brasil e por região (quanto da verba foi comprado da agricultura familiar);
- mostra a evolução de 2011 a 2022 em relação às metas de 30% e 45%;
- permite buscar qualquer município por nome, UF e faixa da meta;
- mostra, para cada município, **quanto falta em reais** para cumprir a meta de 45%;
- destaca o piloto de 2026 no Piauí, o estado mais crítico do Nordeste;
- expõe uma API (`/api/resumo`) e um endpoint de saúde (`/health`) com a versão publicada.

Fontes dos dados: FNDE (aquisições da agricultura familiar no PNAE, 2011 a 2022) e IBGE (população do Censo 2022).

## Origem do projeto

**Reutilizado de outras disciplinas da própria equipe e personalizado para esta entrega.**
A base de dados e o recorte do problema foram criados pela equipe nas disciplinas de *BI e Data Viz* e de
*Data Ethics & Governance* da mesma Global Solution. Para esta disciplina, a base virou uma **aplicação web
nova em Flask**, com identidade visual própria (tons de terra e campo), páginas próprias e conteúdo da equipe,
e todo o ciclo de desenvolvimento passou a ser feito no Azure DevOps.
Nenhum template ou página padrão de terceiros foi mantido.

## Tecnologias utilizadas

- **Python 3.12** e **Flask 3** (aplicação web), **Jinja2** (páginas HTML), **Gunicorn** (servidor em produção)
- **pandas** (geração dos dados a partir da base FNDE/IBGE, em `scripts/gerar_dados.py`)
- **pytest** (7 testes automatizados executados no pipeline)
- **Azure DevOps:** Boards, Repos e Pipelines
- **Azure App Service:** Web App Linux, Python 3.12, plano gratuito F1, região Brazil South
- **Azure Pipelines Agent** (agente self-hosted da equipe)

## Estrutura do repositório

```
app.py                  aplicação Flask (rotas e regra da meta de 45%)
templates/              páginas HTML (painel, municípios, município, sobre, 404)
static/style.css        identidade visual da Merenda da Roça
data/                   resumo.json e municipios.json gerados da base FNDE/IBGE
scripts/gerar_dados.py  gera a pasta data/ a partir do CSV da equipe
tests/test_app.py       testes automatizados (pytest)
azure-pipelines.yml     pipeline de CI/CD
requirements.txt        dependências da aplicação
```

## Azure DevOps

Fluxo demonstrado: **Ideia → Azure Boards → Azure Repos → Branch → Commit → Pull Request → Azure Pipeline
→ Build + Testes → Deploy no Web App → Ambiente atualizado.**

### Azure Boards
Projeto `MerendaDaRoca` criado com o processo **Agile**.

- **User Story #15:** *"Como nutricionista de prefeitura, quero ver quanto meu município compra da
  agricultura familiar e quanto falta para a meta de 45%"*. Tem descrição, critérios de aceite e responsável (Elton).
- **Task 01 (#16):** Personalizar a aplicação Merenda da Roça. Responsável: Kelvin.
- **Task 02 (#17):** Implementar CI/CD com Azure Pipelines e Web App. Responsável: Emerson.
- **Task 03 (#18):** Documentar o projeto no README e reunir as evidências. Responsável: Elton.

Cada item tem título, descrição, responsável e status, e evoluiu de **New → Active → Closed** durante a
atividade. Os commits e Pull Requests citam o número da task (`#16`, `#17`, `#18`), então aparecem ligados
aos work items na seção *Development*.

### Azure Repos
O **Azure Repos é o repositório principal** da atividade (`MerendaDaRoca`).

- `main`: versão publicada, protegida pelo fluxo de Pull Request;
- `feature/update-solution`: branch usada para as alterações na aplicação.

As alterações foram feitas na branch `feature/update-solution` e integradas à `main` por Pull Request
(PR !1, PR !2 e PR !3). O histórico de commits registra cada etapa: base de dados, aplicação, testes,
pipeline, documentação e atualizações.

### Azure Pipelines
O pipeline `MerendaDaRoca` é definido no arquivo `azure-pipelines.yml`, versionado no próprio repositório,
e é conectado ao Azure Repos. Ele tem dois estágios:

1. **CI - Build e testes:** cria um ambiente Python, instala as dependências, roda os 7 testes com pytest,
   publica o resultado dos testes e empacota a aplicação em um `.zip`, publicado como artefato.
2. **CD - Deploy no Azure Web App:** baixa o artefato e publica no Web App `merenda-da-roca-raizdigital`
   pela service connection `azure-merenda-da-roca`. A conexão usa Azure Resource Manager com Workload
   Identity Federation, sem senha nem segredo guardados.

A organização não tem parallel jobs hospedados pela Microsoft. Por isso, o pipeline roda em um **agente
self-hosted** da equipe (pool `Default`, agente `MerendaPC`).

### CI/CD
- **Gatilho automático:** todo push ou merge na `main` dispara o pipeline (`trigger: main`).
- **Primeira publicação:** execução manual `#20261116.1`, com CI e CD com sucesso. Publicou a versão 1.0.1.
- **Atualização do ambiente:** a equipe fez uma alteração simples na branch `feature/update-solution`
  (destaque do piloto 2026 no Piauí na página inicial) e integrou pelo **PR !1**. O pipeline foi disparado
  sozinho (*Individual CI*).
- **Falha real e correção:** essa execução (`#20261116.2`) passou no CI, mas falhou no deploy. O agente
  self-hosted guardava o `.zip` da execução anterior, e a tarefa encontrou dois pacotes. A correção (limpar o
  workspace a cada job e usar o pacote exato do build atual) entrou pelo **PR !2**. O pipeline rodou de novo
  sozinho (`#20261116.3`) e publicou a versão 1.0.3 com o destaque do Piauí.
- A versão publicada aparece no rodapé do site e em `/health` (`1.0.<BuildId>`). Isso prova que a alteração
  chegou ao ambiente pelo pipeline.

## Rodar localmente

```bash
pip install -r requirements.txt
python app.py
```

Acesse http://localhost:5000. Para rodar os testes: `pip install pytest && python -m pytest`.

Para regenerar os dados a partir da base da equipe:
`python scripts/gerar_dados.py GS_2TSCPW_DataViz_MerendaDaRoca_RaizDigital.csv`.
