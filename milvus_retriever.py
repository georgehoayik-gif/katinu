import requests

BASE_URL = "https://apiintegracao.milvus.com.br/api/base-conhecimento/buscar-contexto"
TOKEN = "zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7I"

headers = {
    "Content-Type": "application/json",
    "Authorization": TOKEN
}

payload = {
    "pergunta": "Como instalar uma impressora na rede?"
}

response = requests.post(BASE_URL, headers=headers, json=payload)

print("Status:", response.status_code)
print("Resposta:", response.text)