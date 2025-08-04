import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análisis Ratios Casino Online", layout="wide")
st.title("🎰 Análisis de Ratios - Casino Online")

st.write("Subí el archivo Excel con los datos para calcular los 12 ratios y analizarlos por plataforma.")

# ===== SUBIR ARCHIVO =====
archivo = st.file_uploader("📂 Cargar archivo Excel", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)

    # Normalizar nombres de columnas (por si hay espacios)
    df.columns = df.columns.str.strip()

    # ===== CALCULAR RATIOS =====
    df["Recarga/retiro"] = df["Recargas de saldo"] / df["Retiros de saldo"]
    df["retiro/recarga"] = df["Retiros de saldo"] / df["Recargas de saldo"]
    df["win/recarga"] = df["Win o GGR"] / df["Recargas de saldo"]
    df["win/retiros"] = df["Win o GGR"] / df["Retiros de saldo"]
    df["Dif entre recarga y retiro"] = df["Recargas de saldo"] - df["Retiros de saldo"]
    df["win / dif rec y ret"] = df["Win o GGR"] / df["Dif entre recarga y retiro"]
    df["bonos/win"] = df["Bonus"] / df["Win o GGR"]
    df["win/bonos"] = df["Win o GGR"] / df["Bonus"]
    df["bonos/retiros"] = df["Bonus"] / df["Retiros de saldo"]
    df["Bonos/recargas"] = df["Bonus"] / df["Recargas de saldo"]
    df["recargas/bonos"] = df["Recargas de saldo"] / df["Bonus"]
    df["retiros/bonos"] = df["Retiros de saldo"] / df["Bonus"]

    # ===== UMBRALES TENTATIVOS PARA COLOREO =====
    umbrales = {
        "Recarga/retiro": (1.0, 1.5),
        "retiro/recarga": (0.6, 1.0),
        "win/recarga": (0.15, 0.30),
        "win/retiros": (0.15, 0.30),
        "Dif entre recarga y retiro": (0, float("inf")),  # Positivo esperado
        "win / dif rec y ret": (0.10, 0.50),
        "bonos/win": (0.05, 0.25),
        "win/bonos": (3, float("inf")),
        "bonos/retiros": (0.05, 0.25),
        "Bonos/recargas": (0.05, 0.25),
        "recargas/bonos": (3, float("inf")),
        "retiros/bonos": (3, float("inf")),
    }

    def colorear_valor(val, col):
        try:
            min_val, max_val = umbrales[col]
            if pd.isna(val):
                return "background-color: lightgray"
            if min_val <= val <= max_val:
                return "background-color: lightgreen"  # Dentro de rango
            else:
                return "background-color: lightcoral"  # Fuera de rango
        except KeyError:
            return ""

    # ===== MOSTRAR TABLA POR PLATAFORMA =====
    plataformas = df["Plataforma"].unique()
    for plataforma in plataformas:
        st.subheader(f"📊 Plataforma: {plataforma}")
        df_plataforma = df[df["Plataforma"] == plataforma].copy()

        # Redondear ratios
        for col in umbrales.keys():
            df_plataforma[col] = df_plataforma[col].round(2)

        # Mostrar tabla con colores
        st.dataframe(df_plataforma.style.applymap(
            lambda v, col=None: colorear_valor(v, col),
            subset=list(umbrales.keys())
        ))

else:
    st.info("Por favor, subí un archivo Excel para continuar.")
