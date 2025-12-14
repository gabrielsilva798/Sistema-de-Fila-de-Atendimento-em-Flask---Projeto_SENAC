# utils/gemini_ai.py
import json

def gemini_instrucao_segura(prompt: str, df_json: str) -> dict:
    """
    Função simplificada que sempre retorna alguma operação plotável.
    """

    prompt_lower = prompt.lower()

    # === 1. média de idade ===
    if "idade" in prompt_lower or "nascimento" in prompt_lower:
        return {"operacao": "media_idade"}

    # === 2. contagem por classificação ===
    if "classificacao" in prompt_lower or "quantidade" in prompt_lower:
        return {"operacao": "contagem", "coluna": "classificacao"}

    # === 3. fallback que sempre dá gráfico ===
    return {"operacao": "contagem", "coluna": "classificacao"}
