import requests

url = "https://apiintegracao.milvus.com.br/api/cliente/criar"

headers = {
    "Authorization": "zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7",
    "Content-Type": "application/json"
}

payload = {
    "cliente_documento": "11123445667",
    "cliente_site": "www.site.com",
    "cliente_observacao": "Cliente criado via integração",
    "cliente_ativo": True,
    "cliente_id_integracao": 1001,
    "cliente_pessoa_juridica": {
        "nome": "João da Silva",
        "data_nascimento": "1990-01-01",
        "sexo": "M"
    },
    "cliente_enderecos": [{
        "endereco_padrao": True,
        "endereco_descricao": "Principal",
        "endereco_cep": "11700000",
        "endereco_logradouro": "Rua Exemplo",
        "endereco_numero": "123",
        "endereco_bairro": "Centro",
        "endereco_cidade": "Praia Grande",
        "endereco_estado": "SP"
    }],
    "cliente_contatos": [{
        "contato_padrao": True,
        "contato_descricao": "Financeiro",
        "contato_email": "cliente@email.com",
        "contato_telefone": "(13) 3333-3333",
        "contato_celular": "(13) 99999-9999",
        "contato_app": "Whatsapp",
        "contato_observacao": "Contato principal"
    }]
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)