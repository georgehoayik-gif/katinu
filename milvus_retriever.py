import os

def buscar_conhecimento(query: str, top_k: int = 3) -> str:
    """
    Busca a query em arquivos de treinamento locais (.txt) no diretório especificado.
    """
    pasta_treinamento = "C:/unitak/programas/treinamento"
    arquivos = [f for f in os.listdir(pasta_treinamento) if f.endswith('PDFpdfplumber')]

    resultados = []

    for nome_arquivo in arquivos:
        caminho = os.path.join(pasta_treinamento, nome_arquivo)
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                if query.lower() in conteudo.lower():
                    # Pega um trecho do contexto da primeira ocorrência
                    index = conteudo.lower().find(query.lower())
                    trecho = conteudo[max(0, index-100): index+len(query)+100]
                    resultados.append((nome_arquivo, trecho.strip()))
        except Exception as e:
            print(f"Erro ao ler o arquivo {nome_arquivo}: {e}")

    if not resultados:
        return "Nenhum manual relevante encontrado nos arquivos locais."

    # Retorna os top_k primeiros encontrados
    contexto = ""
    for nome, trecho in resultados[:top_k]:
        contexto += f"--- Manual: {nome} ---\n{trecho}\n\n"

    return contexto