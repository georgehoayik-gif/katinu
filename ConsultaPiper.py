import requests
import json
from datetime import datetime

API_TOKEN = "329808152f40819bd6741d0da39e2f01"

headers = {
    "accept": "application/json",
    "token": API_TOKEN
}

# ===============================
# 1️⃣ BUSCAR PROPOSTAS
# ===============================

url = "https://api.pipe.run/v1/proposals"
response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()
propostas = data.get("data", data)

print(f"Total de propostas retornadas: {len(propostas)}")

# ===============================
# 2️⃣ FILTRAR STATUS GANHO
# (ajuste se seu status for diferente)
# ===============================

ganhas = [p for p in propostas if str(p.get("status")) == "1"]

if not ganhas:
    print("Nenhuma proposta ganha encontrada.")
    exit()

# ===============================
# 3️⃣ MANTER APENAS MAIOR VERSÃO
# ===============================

propostas_unicas = {}

for p in ganhas:
    numero = p.get("number")
    versao = p.get("version", 0)

    if numero not in propostas_unicas or versao > propostas_unicas[numero].get("version", 0):
        propostas_unicas[numero] = p

lista_final = list(propostas_unicas.values())

# ===============================
# 4️⃣ ORDENAR PELA DATA DE FECHAMENTO (mais recente primeiro)
# ===============================

lista_final.sort(
    key=lambda x: datetime.strptime(x["closed_at"], "%Y-%m-%d %H:%M:%S")
    if x.get("closed_at") else datetime.min,
    reverse=True
)

ultimo = lista_final[0]

# ===============================
# 5️⃣ BUSCAR CLIENTE E ESTABELECIMENTO VIA DEAL
# ===============================

deal_id = ultimo.get("deal_id")
cliente = {}
estabelecimento = {}

if deal_id:
    # 🔎 Busca o DEAL
    url_deal = f"https://api.pipe.run/v1/deals/{deal_id}"
    response_deal = requests.get(url_deal, headers=headers)
    response_deal.raise_for_status()

    deal = response_deal.json().get("data", {})

    # ================= CLIENTE =================
    person_id = deal.get("person_id")

    if person_id:
        url_cliente = f"https://api.pipe.run/v1/persons/{person_id}"
        response_cliente = requests.get(url_cliente, headers=headers)
        response_cliente.raise_for_status()
        cliente = response_cliente.json().get("data", {})

    # ================= ESTABELECIMENTO =================

estabelecimento = {}

company_id = cliente.get("company_id")

if company_id:
    url_company = f"https://api.pipe.run/v1/companies/{company_id}"
    response_company = requests.get(url_company, headers=headers)
    response_company.raise_for_status()

    estabelecimento = response_company.json().get("data", {})
else:
    print("Cliente não possui company_id.")
if person_id:
    url_cliente = f"https://api.pipe.run/v1/persons/{person_id}?with=contactPhones"
    response_cliente = requests.get(url_cliente, headers=headers)
    response_cliente.raise_for_status()

    cliente = response_cliente.json().get("data", {})

    # ================= TELEFONES =================
    telefones = []

    for telefone in cliente.get("contactPhones", []):
        numero = telefone.get("phone")
        if numero:
            telefones.append(numero)
else:
    telefones = []
# ===============================
# 6️⃣ RESULTADO FINAL
# ===============================

resultado_final = {
    "proposta": ultimo,
    "cliente": cliente,
    "estabelecimento": estabelecimento

}

print("\n===== RESULTADO COMPLETO =====\n")
print(json.dumps(resultado_final, indent=4, ensure_ascii=False))

