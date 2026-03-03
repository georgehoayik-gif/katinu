import requests
import json

BASE_URL = "https://apiintegracao.milvus.com.br/api/cliente/criar"
TOKEN = "zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7"

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

payload = {
    "cliente_documento": "65052777000145",
    "cliente_site": "",
    "cliente_observacao": "Cliente cadastrado via integração",
    "cliente_ativo": True,
    "cliente_id_integracao": 0,

    # 👇 IMPORTANTE: Pessoa Jurídica
    "cliente_pessoa_juridica": {
        "nome_fantasia": "Kolorê kids",
        "razao_social": "65.052.777 BEATRIS DOS SANTOS FERREIRA",
        "inscricao_estadual": ""
    },

    "cliente_enderecos": [
        {
            "endereco_padrao": True,
            "endereco_descricao": "Endereço principal",
            "endereco_cep": "11704300",
            "endereco_logradouro": "R DOUTOR VICENTE DE CARVALHO",
            "endereco_numero": "1045",
            "endereco_complemento": "CASA 2",
            "endereco_bairro": "Ocian",
            "endereco_cidade": "Praia Grande",
            "endereco_estado": "SP"
        }
    ],

    "cliente_contatos": [
        {
            "contato_padrao": True,
            "contato_descricao": "Financeiro",
            "contato_email": "beatrizferreira202@gmail.com",
            "contato_telefone": "",
            "contato_celular": "551388772583",
            "contato_observacao": "Contato principal via WhatsApp",


        }
    ]
}

response = requests.post(BASE_URL, headers=headers, json=payload)

print("Status Code:", response.status_code)
print("Resposta:", response.text)