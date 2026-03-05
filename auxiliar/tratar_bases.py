import pandas as pd

def pegar_moods_nao_resolvidos(df: pd.DataFrame) -> pd.DataFrame:
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["intensidade"] = pd.to_numeric(df["intensidade"], errors="coerce").fillna(0).astype(int)
    
    ultimo_registro = df.groupby(["incomodo"])["data"].max().reset_index()

    marcar_ultimo_registro = pd.merge(df, ultimo_registro, on=["incomodo", "data"], how="inner")
    marcar_ultimo_registro = marcar_ultimo_registro.drop_duplicates(subset=["incomodo","data"], keep="last")

    resultado = marcar_ultimo_registro.drop(columns=["data"]).reset_index(drop=True)
    resultado = resultado.loc[resultado["intensidade"] > 0].reset_index(drop=True)

    return resultado
