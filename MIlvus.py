import requests
import pandas as pd
import json

# ==============================
# 🔗 API RELATÓRIO DE ATENDIMENTO
# ==============================
url = "https://apiintegracao.milvus.com.br/api/relatorio-atendimento/listagem"

payload = json.dumps({
    "filtro_body": {
        "data_inicial": "2024-01-01",
        "data_final": "2024-12-31"
    }
})

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7'
}

response = requests.post(url, headers=headers, data=payload)

if response.status_code != 200:
    print("Erro na requisição:", response.text)
    exit()

data = response.json()

if "lista" not in data:
    print("Resposta inesperada:", data)
    exit()
# ==============================
# 📊 TRANSFORMA EM DATAFRAME
# ==============================
df = pd.DataFrame(data["lista"])
df["nome_mesa"].unique()

# Extrair nome da mesa (vem como objeto JSON)
df["mesa_trabalho"] = df["mesa_trabalho"].apply(
    lambda x: x.get("nome") if isinstance(x, dict) else None
)

# Converter data
df["data"] = pd.to_datetime(df["data_inicial"], errors="coerce")

# ==============================
# 📅 FILTRAR SÁBADO E DOMINGO
# ==============================
df_fds = df[df["data"].dt.weekday >= 5]

# ==============================
# 🎯 FILTRAR MESAS
# ==============================
suporte_tecnico = df_fds[df_fds["mesa_trabalho"] == "Suporte Técnico"]
suporte_emergencia = df_fds[df_fds["mesa_trabalho"] == "Suporte de emergência"]

# ==============================
# 📊 CÁLCULOS
# ==============================
total_tecnico = len(suporte_tecnico)
total_emergencia = len(suporte_emergencia)
media = (total_tecnico + total_emergencia) / 2

# ==============================
# 🧾 DATAFRAMES DE SAÍDA
# ==============================
df_resumo = pd.DataFrame({
    "Mesa": ["Suporte Técnico", "Suporte de emergência"],
    "Total de Atendimentos": [total_tecnico, total_emergencia]
})

df_media = pd.DataFrame({
    "Métrica": ["Média de Atendimentos (FDS)"],
    "Valor": [media]
})

# ==============================
# 💾 SALVAR NA ÁREA DE TRABALHO
# ==============================
caminho = r"C:\Users\usuario\Desktop\relatorio_fds.xlsx"

with pd.ExcelWriter(caminho) as writer:
    df_resumo.to_excel(writer, sheet_name="Resumo FDS", index=False)
    df_media.to_excel(writer, sheet_name="Média", index=False)

print("Relatório de fim de semana gerado com sucesso na área de trabalho!")