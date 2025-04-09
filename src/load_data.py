import os
import pandas as pd
import joblib

DATA_DIR = "data/raw/CSV"
CACHE_FILE = "data/processed/dataframes_cache.pkl"

def carregar_arquivos_csv():
    dataframes = {}
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".csv"):
            nome_df = filename.replace(".csv", "").lower()
            df = pd.read_csv(os.path.join(DATA_DIR, filename), encoding="utf-8")

            # Pré-processamento específico por base
            if "pedido" in nome_df and "valor total" in df.columns:
                df["Valor Total"] = (
                    df["Valor Total"]
                    .astype(str)
                    .str.replace("R$", "", regex=False)
                    .str.replace(".", "", regex=False)
                    .str.replace(",", ".", regex=False)
                    .astype(float)
                )

            if "pedido" in nome_df and "data pedido" in df.columns:
                df["Data Pedido"] = pd.to_datetime(
                    df["Data Pedido"], errors="coerce", dayfirst=True
                )

            if "usuarios" in nome_df and "Login" in df.columns:
                df["Login"] = df["Login"].astype(str)

            dataframes[nome_df] = df
    return dataframes

def salvar_cache(dataframes):
    os.makedirs("data/processed", exist_ok=True)
    joblib.dump(dataframes, CACHE_FILE)

def carregar_cache():
    if os.path.exists(CACHE_FILE):
        return joblib.load(CACHE_FILE)
    return None

def obter_dataframes():
    cache = carregar_cache()
    if cache:
        return cache
    dfs = carregar_arquivos_csv()
    salvar_cache(dfs)
    return dfs
