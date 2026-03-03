import requests
import pandas as pd
import json

# URL base da API de relatório de atendimento
BASE_URL = "https://api.pipe.run/v1/proposals"

# Token de autenticação
TOKEN = "329808152f40819bd6741d0da39e2f01"

# Cabeçalhos da requisição
headers = {
    'Content-Type': 'application/json',
    'Authorization': TOKEN
}

# Lista que irá armazenar todos os registros de todas as páginas
todos_chamados = []

# Definindo paginação
total_registros = 1000
max_paginas = 1

# Loop para percorrer até 5 páginas
for pagina in range(1, max_paginas + 1):

    # Monta a URL com paginação
    url = f"{BASE_URL}?total_registros={total_registros}&pagina={pagina}"

    # Corpo da requisição com filtro
    payload = json.dumps({
        "filtro_body": {
            "status": 4
        }
    })

    print(f"Buscando página {pagina}...")

    # Envia requisição POST
    response = requests.post(url, headers=headers, data=payload)

    # Se não retornar 200, para o loop
    if response.status_code != 200:
        print("Erro:", response.status_code)
        break

    # Converte resposta para JSON
    data = response.json()

    # Se não houver registros, interrompe
    if 'lista' not in data or len(data['lista']) == 0:
        print("Sem mais registros.")
        break

    print(f"Página {pagina}: {len(data['lista'])} registros")

    # Adiciona os registros na lista geral
    todos_chamados.extend(data['lista'])

print(f"\nTotal final: {len(todos_chamados)} registros")

# =============================
# CRIA O DATAFRAME
# =============================

Relatorio2 = pd.DataFrame(todos_chamados)

# =============================
# TRATAMENTO DOS CAMPOS DICT
# =============================

# Essas colunas vêm como:
# {'id': 63302, 'text': '1.Sysloja.Pro'}
# Então vamos extrair apenas o campo "text"

colunas_dict = ["categoria_primaria", "categoria_secundaria", "mesa_trabalho"]

for col in colunas_dict:
    if col in Relatorio2.columns:
        Relatorio2[col] = Relatorio2[col].apply(
            lambda x: x.get("text") if isinstance(x, dict) else x
        )

# =============================
# SELEÇÃO DAS COLUNAS
# =============================

columns_to_select = [
    "id"
]

# Mantém apenas as colunas existentes
Relatorio2 = Relatorio2[[col for col in columns_to_select if col in Relatorio2.columns]]

# Exibe relatório no terminal
print(Relatorio2.to_string(index=False))
