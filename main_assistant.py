# arquivo: main_assistant.py
from milvus_retriever import buscar_conhecimento
from llm_generator import gerar_resposta

def criar_prompt_formatado(contexto: str, pergunta: str) -> str:
    """
    Cria o prompt final que será enviado para o LLM.
    """
    template_prompt = f"""
    Você é um assistente especialista em automação comercial e impostos para o sistema da empresa. 
    Sua tarefa é responder à pergunta do usuário de forma precisa e direta, baseando-se exclusivamente no contexto fornecido abaixo.
    Não utilize nenhum conhecimento prévio que não esteja no contexto. Se a resposta não estiver no contexto, diga "A informação para responder a essa pergunta não foi encontrada na minha base de conhecimento.".

    --- CONTEXTO FORNECIDO ---
    {contexto}
    --- FIM DO CONTEXTO ---

    PERGUNTA DO USUÁRIO:
    "{pergunta}"

    Sua Resposta:
    """
    return template_prompt

def main():
    """
    Função principal do assistente de IA.
    """
    print("Olá! Sou seu assistente de automação comercial. Como posso ajudar?")
    print("Digite 'sair' a qualquer momento para terminar.")

    while True:
        pergunta_usuario = input("\nSua pergunta: ")
        if pergunta_usuario.lower() == 'sair':
            break

        print("\nBuscando na base de conhecimento...")
        # Passo 1: Recuperar contexto do Milvus Helpdesk
        contexto_relevante = buscar_conhecimento(pergunta_usuario)
        
        # Opcional: mostrar o contexto encontrado para depuração
        # print(f"--- Contexto encontrado ---\n{contexto_relevante[:500]}...\n--------------------------")

        print("Gerando resposta com a IA...")
        # Passo 2: Formatar o prompt para o LLM
        prompt_final = criar_prompt_formatado(contexto_relevante, pergunta_usuario)
        
        # Passo 3: Gerar a resposta com o Ollama
        resposta_final = gerar_resposta(prompt_final)

        print("\n--- Resposta do Assistente ---")
        print(resposta_final)
        print("------------------------------")

if __name__ == '__main__':
    main()