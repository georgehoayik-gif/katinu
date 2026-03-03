import requests
import json

url = "https://apiintegracao.milvus.com.br/api/relatorio-atendimento/listagem"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7'
}

payload = json.dumps({
    "filtro_body": {
        "status": 4
    }
})

response = requests.post(url, headers=headers, data=payload)
data = response.json()

vazios = 0
preenchidos = 0

for chamado in data.get("lista", []):
    if chamado.get("unidade_negocio") is None:
        vazios += 1
    else:
        preenchidos += 1

print("Preenchidos:", preenchidos)
print("Vazios:", vazios)