import requests
import time

BASE_URL_CLIENTE = "https://apiintegracao.milvus.com.br/api/cliente/criar"
BASE_URL_CHAMADO = "https://apiintegracao.milvus.com.br/api/chamado/criar"

TOKEN = "zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7"

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

# =========================================
# 1️⃣ CRIAR CLIENTE
# =========================================

payload_cliente = {
    "cliente_documento": "65052777000145",
    "cliente_site": "",
    "cliente_observacao": "Cliente cadastrado via integração",
    "cliente_ativo": True,
    "cliente_id_integracao": 0,

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
            "contato_observacao": "Contato principal via WhatsApp"
        }
    ]
}

response_cliente = requests.post(
    BASE_URL_CLIENTE,
    headers=headers,
    json=payload_cliente
)

print("Status Cliente:", response_cliente.status_code)
print("Resposta Cliente:", response_cliente.text)

if response_cliente.status_code != 200:
    print("Erro ao criar cliente.")
    exit()

# 🔥 FORÇANDO COMO INTEIRO
cliente_id = int(response_cliente.text.strip())

print("Cliente ID capturado:", cliente_id)

# Pequeno delay
time.sleep(2)

# =========================================
# 2️⃣ CRIAR CHAMADO
# =========================================

payload_chamado = {
    "cliente_id": "cliente_id",  # 👈 NOME FANTASIA
    "chamado_assunto": "Implantação do Sistema",
    "chamado_descricao": "Chamado automático de implantação criado via integração.",
    "chamado_categoria_primaria": "Implantação",
    "categoria_id": 1
}

response_chamado = requests.post(
    BASE_URL_CHAMADO,
    headers=headers,
    json=payload_chamado
)

print("Status Chamado:", response_chamado.status_code)
print("Resposta Chamado:", response_chamado.text)

if response_chamado.status_code == 200:
    print("Chamado criado com sucesso!")
else:
    print("Erro ao criar chamado.")