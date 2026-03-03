import requests
import pandas as pd
import json
from datetime import datetime, timedelta

BASE_URL = "https://apiintegracao.milvus.com.br/api/chamado/listagem"
TOKEN = "zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7"

headers = {
    'Content-Type': 'application/json',
    'Authorization': TOKEN
}

todos_chamados = []

# ==============================
# CALCULA ÚLTIMOS 30 DIAS
# ==============================

hoje = datetime.now()
data_inicio = (hoje - timedelta(days=30)).strftime("%Y-%m-%d 00:00:00")
data_fim = hoje.strftime("%Y-%m-%d 23:59:59")

print(f"Buscando chamados de {data_inicio} até {data_fim}")

total_registros = 1000
max_paginas = 5

for pagina in range(1, max_paginas + 1):

    url = f"{BASE_URL}?total_registros={total_registros}&pagina={pagina}"

    payload = json.dumps({
        "filtro_body": {
            "data_criacao_inicio": data_inicio,
            "data_criacao_fim": data_fim
        }
    })

    print(f"Buscando página {pagina}...")

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        print("Erro:", response.status_code)
        print(response.text)
        break

    data = response.json()

    if 'lista' not in data or len(data['lista']) == 0:
        print("Sem mais registros.")
        break

    print(f"Página {pagina}: {len(data['lista'])} registros")

    todos_chamados.extend(data['lista'])

print(f"\nTotal final: {len(todos_chamados)} registros")

# ==============================
# CRIA DATAFRAME
# ==============================

df = pd.DataFrame(todos_chamados)

# Ajusta campos que vêm como dict
colunas_dict = ["categoria_primaria", "categoria_secundaria", "mesa_trabalho"]

for col in colunas_dict:
    if col in df.columns:
        df[col] = df[col].apply(
            lambda x: x.get("text") if isinstance(x, dict) else x
        )

columns_to_select = [

    "endereco_unidade_de_negocio"
]

df = df[[col for col in columns_to_select if col in df.columns]]

print(df.to_string(index=False))
