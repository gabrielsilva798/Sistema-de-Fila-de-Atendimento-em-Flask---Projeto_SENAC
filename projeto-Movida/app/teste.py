import google.generativeai as genai

genai.configure(api_key="SUA_CHAVE_AQUI")

models = genai.list_models()

for m in models:
    print(m.name)
