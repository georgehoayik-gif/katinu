import requests
import json

url = "https://apiintegracao.milvus.com.br/api/chamado/criar"

API_TOKEN = "zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7"

headers = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

payload = {
    "cliente_id": "TOKEN_ID_DO_CLIENTE",
    "chamado_assunto": "Sysloja( Cliente contratando)",
    "chamado_descricao": "Informações do cliente para contratação do Sysloja.PRO - Vendedor responsável: Diego",
    "chamado_mesa": "Implantação Sysloja Pró",
    "chamado_setor": "Setor padrão",
    "chamado_categoria_primaria": "1.Sysloja.Pro",
    "chamado_categoria_secundaria": "Implantação",
    "categoria_id": 325329
}

response = requests.post(url, headers=headers, json=payload)

print("Status:", response.status_code)
print("Resposta:", response.text)