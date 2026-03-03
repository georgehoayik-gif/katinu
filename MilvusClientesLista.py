import requests
import json

API_TOKEN = "zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7"

url = "https://apiintegracao.milvus.com.br/api/cliente/busca"

headers = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

params = {
    "status": 1  # clientes ativos
}

response = requests.get(url, headers=headers, params=params)

print("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()
    
    lista_clientes = data.get("lista", [])
    
    print("\nÚltimos 10 clientes:\n")
    
    for cliente in lista_clientes[-10:]:
        print(f"ID: {cliente['id']}")
        print(f"Razão Social: {cliente['razao_social']}")
        print(f"Nome Fantasia: {cliente['nome_fantasia']}")
        print(f"CNPJ/CPF: {cliente['cnpj_cpf']}")
        print(f"TOKEN: {cliente['token']}")
        print("-" * 40)

else:
    print("Erro:", response.text)