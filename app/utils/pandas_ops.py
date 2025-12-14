# utils/pandas_ops.py
import pandas as pd
from datetime import datetime

def calcular_idade(data_nascimento):
    if pd.isnull(data_nascimento):
        return None

    # 🔥 Garante que é datetime
    if not isinstance(data_nascimento, pd.Timestamp):
        try:
            data_nascimento = pd.to_datetime(data_nascimento, errors="coerce")
        except:
            return None

    if pd.isnull(data_nascimento):
        return None

    hoje = datetime.today()
    return hoje.year - data_nascimento.year - (
        (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
    )


def executar_operacao(df: pd.DataFrame, instrucao: dict) -> pd.DataFrame:
    operacao = instrucao.get("operacao")

    if operacao == "media_idade":
        # gerar coluna idade com base em nascimento
        df["idade"] = df["nascimento"].apply(calcular_idade)
        media = df["idade"].mean()
        return pd.DataFrame({"média de idade": [round(media, 2)]})

    if operacao == "contagem" and "coluna" in instrucao:
        coluna = instrucao["coluna"]
        cont = df[coluna].value_counts().reset_index()
        cont.columns = [coluna, "total"]
        return cont

    # operação padrão — mostra tudo
    return df
