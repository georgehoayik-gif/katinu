# arquivo: llm_generator.py
import ollama

def gerar_resposta(prompt: str) -> str:
    """
    Envia um prompt para o modelo de linguagem no Ollama e retorna a resposta.
    """
    try:
        response = ollama.chat(
            model='llama3', # ou o modelo que você baixou
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            stream=False # Para uma resposta única e não em streaming
        )
        return response['message']['content']
    except Exception as e:
        print(f"Erro ao se comunicar com o Ollama: {e}")
        return "Desculpe, não consegui gerar uma resposta no momento.teste"