import requests
import json
from datetime import datetime

# ==========================================
# 🔐 CONFIGURAÇÕES
# ==========================================

PIPERUN_TOKEN = "329808152f40819bd6741d0da39e2f01"
MILVUS_TOKEN = "zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7"

headers_piperun = {
    "accept": "application/json",
    "token": PIPERUN_TOKEN
}

headers_milvus = {
    "Authorization": MILVUS_TOKEN,
    "Content-Type": "application/json"
}

# ==========================================
# 1️⃣ BUSCAR ÚLTIMA PROPOSTA GANHA
# ==========================================

def buscar_ultima_proposta_ganha():
    url = "https://api.pipe.run/v1/proposals"
    response = requests.get(url, headers=headers_piperun)
    response.raise_for_status()

    propostas = response.json().get("data", [])

    ganhas = [p for p in propostas if str(p.get("status")) == "1"]

    if not ganhas:
        print("Nenhuma proposta ganha encontrada.")
        return None

    propostas_unicas = {}
    for p in ganhas:
        numero = p.get("number")
        versao = p.get("version", 0)

        if numero not in propostas_unicas or versao > propostas_unicas[numero].get("version", 0):
            propostas_unicas[numero] = p

    lista_final = list(propostas_unicas.values())

    lista_final.sort(
        key=lambda x: datetime.strptime(x["closed_at"], "%Y-%m-%d %H:%M:%S")
        if x.get("closed_at") else datetime.min,
        reverse=True
    )

    return lista_final[0]

# ==========================================
# 2️⃣ BUSCAR DADOS DO CLIENTE E EMPRESA
# ==========================================

def buscar_dados_cliente(proposta):
    deal_id = proposta.get("deal_id")

    if not deal_id:
        return None, None

    # 🔎 Buscar deal
    deal = requests.get(
        f"https://api.pipe.run/v1/deals/{deal_id}",
        headers=headers_piperun
    ).json().get("data", {})

    person_id = deal.get("person_id")

    cliente = {}
    empresa = {}

    # 🔎 Buscar cliente COM TELEFONES
    if person_id:
        cliente = requests.get(
            f"https://api.pipe.run/v1/persons/{person_id}?with=contactPhones",
            headers=headers_piperun
        ).json().get("data", {})

    # 🔎 Buscar empresa
    company_id = cliente.get("company_id")

    if company_id:
        empresa = requests.get(
            f"https://api.pipe.run/v1/companies/{company_id}",
            headers=headers_piperun
        ).json().get("data", {})

    return cliente, empresa

# ==========================================
# 🔹 NOVO: EXTRATOR DE TELEFONE
# ==========================================

def extrair_telefone(cliente):

    telefones = cliente.get("contactPhones", [])

    if not telefones:
        return ""

    principal = next((t for t in telefones if t.get("is_main") == 1), None)

    if principal:
        numero = principal.get("phone")
    else:
        numero = telefones[0].get("phone")

    if not numero:
        return ""

    numero = numero.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")

    if numero.startswith("0"):
        numero = numero[1:]


    return numero

# ==========================================
# 3️⃣ CADASTRAR CLIENTE NO MILVUS
# ==========================================

def cadastrar_cliente_milvus(cliente, empresa):

    telefone = extrair_telefone(cliente)

    payload = {
        "cliente_documento": empresa.get("cnpj", "").replace(".", "").replace("/", "").replace("-", ""),
        "cliente_site": empresa.get("website") or "",
        "cliente_observacao": "Cliente cadastrado automaticamente via PipeRun",
        "cliente_ativo": True,
        "cliente_id_integracao": cliente.get("id"),

        "cliente_pessoa_juridica": {
            "nome_fantasia": empresa.get("name"),
            "razao_social": empresa.get("company_name"),
            "inscricao_estadual": empresa.get("ie") or ""
        },

        "cliente_enderecos": [
            {
                "endereco_padrao": True,
                "endereco_descricao": "Endereço principal",
                "endereco_cep": empresa.get("cep"),
                "endereco_logradouro": empresa.get("address"),
                "endereco_numero": empresa.get("address_number"),
                "endereco_complemento": empresa.get("address_complement"),
                "endereco_bairro": empresa.get("district"),
                "endereco_cidade": "Praia Grande",
                "endereco_estado": "SP"
            }
        ],

        "cliente_contatos": [
            {
                "contato_padrao": True,
                "contato_descricao": cliente.get("name"),
                "contato_email": "",
                "contato_telefone": "",
                "contato_celular": telefone,
                "contato_observacao": cliente.get("name")
            }
        ]
    }

    url = "https://apiintegracao.milvus.com.br/api/cliente/criar"
    response = requests.post(url, headers=headers_milvus, json=payload)

    print("Cadastro cliente Milvus:", response.status_code)
    print("Resposta:", response.text)

    if response.status_code == 200:
        return response.json()  # retorna ID numérico

    return None

def buscar_token_cliente(cliente_id):

    print("🔎 Buscando token do cliente pelo ID:", cliente_id)

    url = "https://apiintegracao.milvus.com.br/api/cliente/busca"

    params = {
        "status": 1
    }

    response = requests.get(url, headers=headers_milvus, params=params)

    print("Status busca:", response.status_code)

    if response.status_code != 200:
        print("Erro ao buscar clientes:", response.text)
        return None

    data = response.json()
    lista_clientes = data.get("lista", [])

    for cliente in lista_clientes:
        if cliente.get("id") == cliente_id:
            token = cliente.get("token")
            print("✅ TOKEN encontrado:", token)
            return token

    print("❌ Cliente não encontrado na lista.")
    return None





# ==========================================
# 4️⃣ CRIAR TICKET DE IMPLANTAÇÃO
# ==========================================
def definir_configuracao_chamado(proposta):

    items = proposta.get("items", [])

    for item in items:
        nome_produto = str(item.get("product_name", "")).lower()

        if "saurus" in nome_produto:
            return {
                "mesa": "Implantação Saurus",
                "categoria_primaria": "7. Saurus"
            }

        elif "sysloja" in nome_produto:
            return {
                "mesa": "Implantação Sysloja Pró",
                "categoria_primaria": "1.Sysloja.Pro"
            }

        elif "syscook" in nome_produto:
            return {
                "mesa": "Implantação Syscook",
                "categoria_primaria": "2.Syscook"
            }

    # fallback padrão
    return {
        "mesa": "Implantação",
        "categoria_primaria": "1.Sysloja.Pro"
    }


def criar_ticket(token, proposta):

    config = definir_configuracao_chamado(proposta)

    chamado_mesa = config["mesa"]
    categoria_primaria = config["categoria_primaria"]

    print("🎫 Criando ticket para mesa:", chamado_mesa)
    print("📂 Categoria primária:", categoria_primaria)

    payload = {
        "cliente_id": token,
        "chamado_assunto": f"{chamado_mesa}",
        "chamado_descricao": f"""
Cliente fechado no PipeRun.

Proposta: {proposta.get('name')}
Valor MRR: {proposta.get('value_mrr')}
Data fechamento: {proposta.get('closed_at')}
OBS: {proposta.get('observation')}
PDF: {proposta.get('url')}
        """,
        "chamado_mesa": chamado_mesa,
        "chamado_setor": "Setor padrão",
        "chamado_categoria_primaria": categoria_primaria,
        "chamado_categoria_secundaria": "Implantação",
        "categoria_id": 325329

    }

    url = "https://apiintegracao.milvus.com.br/api/chamado/criar"

    response = requests.post(url, headers=headers_milvus, json=payload)

    print("Status criação ticket:", response.status_code)
    print("Resposta ticket:", response.text)
# ==========================================
# 🚀 EXECUÇÃO
# ==========================================

def main():

    print("🔎 Buscando proposta ganha...")
    proposta = buscar_ultima_proposta_ganha()

    if not proposta:
        return

    print("📋 Proposta encontrada:", proposta.get("number"))

    cliente, empresa = buscar_dados_cliente(proposta)

    if not cliente or not empresa:
        print("Erro ao buscar cliente ou empresa.")
        return

    print("👤 Cliente:", cliente.get("name"))
    print("🏢 Empresa:", empresa.get("name"))

    # 1️⃣ Cadastrar cliente no Milvus (retorna ID numérico)
    cliente_id_milvus = cadastrar_cliente_milvus(cliente, empresa)

    if not cliente_id_milvus:
        print("Erro ao cadastrar cliente no Milvus.")
        return

    print("🆔 Cliente cadastrado no Milvus. ID:", cliente_id_milvus)

    # 2️⃣ Buscar TOKEN usando o ID
    cliente_token = buscar_token_cliente(cliente_id_milvus)

    if not cliente_token:
        print("Erro ao obter TOKEN do cliente.")
        return

    print("🔑 Token do cliente:", cliente_token)

    # 3️⃣ Criar ticket usando TOKEN (e não ID)
    print("🎫 Criando ticket de implantação...")
    criar_ticket(cliente_token, proposta)

    print("✅ Processo finalizado com sucesso!")


if __name__ == "__main__":
    main()