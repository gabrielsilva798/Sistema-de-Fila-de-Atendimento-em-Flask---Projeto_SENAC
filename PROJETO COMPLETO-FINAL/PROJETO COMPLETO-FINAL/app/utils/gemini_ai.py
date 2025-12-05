# utils/gemini_ai.py
import json

def gemini_instrucao_segura(prompt: str, df_json: str) -> dict:
    """
    Recebe um prompt e um dataframe em json e retorna uma instrução estruturada
    vinda do Gemini em formato JSON.
    Essa função NÃO usa genai.GenerativeModel.
    """

    # Simulação do "prompt inteligente"
    # Aqui você vai enviar a variável para a IA online (navegador, fetch, axios, API própria, etc.)
    # Por enquanto, vamos supor que a IA retorna instruções simples.
    
    # EXEMPLO DE RETORNO ESPERADO:
    # { "operacao": "media_idade" }
    # { "operacao": "contagem", "coluna": "classificacao" }

    prompt_lower = prompt.lower()

    if "idade" in prompt_lower and "média" in prompt_lower:
        return {"operacao": "media_idade"}

    if "classificacao" in prompt_lower and "contagem" in prompt_lower:
        return {"operacao": "contagem", "coluna": "classificacao"}

    # padrão
    return {"operacao": "mostrar_tudo"}

