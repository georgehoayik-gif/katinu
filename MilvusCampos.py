# Importa a biblioteca para fazer requisições HTTP (conectar na API)
import requests

# Importa o pandas para manipular dados em formato de tabela (DataFrame)
import pandas as pd

# Importa a biblioteca para trabalhar com JSON
import json


# Define a URL da API
# total_registros=1 significa que queremos apenas 1 chamado
url = "https://apiintegracao.milvus.com.br/api/chamado/listagem"


# Define os cabeçalhos (headers) da requisição
headers = {
    # Informa que estamos enviando dados no formato JSON
    'Content-Type': 'application/json',
    
    # Token de autenticação da API (permite acesso aos dados)
    'Authorization': 'zayqrw9btEIxTtM26w0JjCWrW8GS4QsVXFkAePTm2unCU6DsTrmWUD7lOP94lxocEgXRZBdlxTmSPrkjM9vdCrFEytnsbZOQFxgK7'
}


# Corpo (payload) da requisição
# Aqui estamos aplicando um filtro
payload = json.dumps({
    "filtro_body": {
        # Status 4 normalmente significa chamados finalizados
        "status": 4
    }
})


try:
    # Faz a requisição POST para a API
    response = requests.post(url, headers=headers, data=payload)
    
    # Verifica se houve erro HTTP (ex: 401, 500, etc)
    response.raise_for_status()
    
    # Converte a resposta da API para formato JSON (dicionário Python)
    data = response.json()

# Se ocorrer qualquer erro, ele entra aqui
except Exception as e:
    print("Erro na requisição:", e)
    exit()


# Verifica se a chave 'lista' existe na resposta
# e se ela contém pelo menos 1 registro
if 'lista' in data and len(data['lista']) > 0:

    # Converte a lista de chamados em uma tabela (DataFrame)
    df = pd.DataFrame(data['lista'])

    print("\n=== CAMPOS DISPONÍVEIS ===\n")
    
    # Percorre cada coluna do DataFrame
    for coluna in df.columns:
        # Imprime o nome da coluna
        print(coluna)

else:
    # Caso não tenha retornado nenhum registro
    print("Nenhum registro retornado.")