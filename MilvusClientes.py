import requests
import pandas as pd
import json
from datetime import datetime

BASE_URL = "https://apiintegracao.milvus.com.br/api/chat/listagem"
TOKEN = "zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7"

headers = {
    'Content-Type': 'application/json',
    'Authorization': TOKEN
}

todos_chamados = []

print("Buscando registros...")

total_registros = 1000
max_paginas = 1

for pagina in range(1, max_paginas + 1):

    url = f"{BASE_URL}?total_registros={total_registros}&pagina={pagina}"

    payload = json.dumps({
        "filtro_body": {}
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

print(f"\nTotal bruto retornado: {len(todos_chamados)} registros")

# ==============================
# CRIA DATAFRAME
# ==============================

Atendimento = pd.DataFrame(todos_chamados)

# Ajusta campos que vêm como dict
colunas_dict = ["categoria_primaria", "categoria_secundaria", "mesa_trabalho"]

for col in colunas_dict:
    if col in Atendimento.columns:
        Atendimento[col] = Atendimento[col].apply(
            lambda x: x.get("text") if isinstance(x, dict) else x
        )

# ==============================
# FILTRA APENAS DIA ATUAL
# ==============================

if "data_mensagem" in Atendimento.columns:

    Atendimento["data_mensagem"] = pd.to_datetime(
        Atendimento["data_mensagem"],
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce"
    )

    hoje = datetime.now().date()

    Atendimento = Atendimento[
        Atendimento["data_mensagem"].dt.date == hoje
    ]

    print(f"\nTotal de atendimentos HOJE: {len(Atendimento)}")

else:
    print("Coluna 'data_mensagem' não encontrada.")
    print("Colunas disponíveis:", Atendimento.columns)

# ==============================
# SELECIONA COLUNAS
# ==============================

columns_to_select = [

    "endereco_unidade_de_negocio"
]

Atendimento = Atendimento[[col for col in columns_to_select if col in Atendimento.columns]]

print("\nResultado final:\n")
print(Atendimento.to_string(index=False))