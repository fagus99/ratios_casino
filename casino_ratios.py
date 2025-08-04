import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ratios Casino Online", layout="wide")
st.title("🎰 Análisis de Ratios - Casino Online")

st.write("Subí el archivo Excel con los datos para calcular y visualizar los 12 ratios con formato de colores.")

# ===== SUBIR ARCHIVO =====
archivo = st.file_uploader("📂 Cargar archivo Excel", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
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

    # ===== UMBRALES =====
    umbrales = {
        "Recarga/retiro": (1.0, 1.5, 0.8, 1.7),
        "retiro/recarga": (0.6, 1.0, 0.5, 1.1),
        "win/recarga": (0.15, 0.30, 0.10, 0.35),
        "win/retiros": (0.15, 0.30, 0.10, 0.35),
        "Dif entre recarga y retiro": (0, float("inf"), -1000000, float("inf")),
        "win / dif rec y ret": (0.10, 0.50, 0.05, 0.60),
        "bonos/win": (0.05, 0.25, 0.03, 0.30),
        "win/bonos": (3, float("inf"), 2, float("inf")),
        "bonos/retiros": (0.05, 0.25, 0.03, 0.30),
        "Bonos/recargas": (0.05, 0.25, 0.03, 0.30),
        "recargas/bonos": (3, float("inf"), 2, float("inf")),
        "retiros/bonos": (3, float("inf"), 2, float("inf")),
    }

    # ===== FUNCIÓN PARA COLOREAR =====
    def colorear_valor(val, col):
        try:
            min_v, max_v, min_a, max_a = umbrales[col]
            if pd.isna(val):
                return "background-color: lightgray"
            if min_v <= val <= max_v:
                return "background-color: lightgreen"  # Verde
            elif min_a <= val <= max_a:
                return "background-color: khaki"  # Amarillo
            else:
                return "background-color: lightcoral"  # Rojo
        except KeyError:
            return ""

    # ===== MOSTRAR POR PLATAFORMA =====
    plataformas = df["Plataforma"].unique()
    for plataforma in plataformas:
        st.subheader(f"📊 Plataforma: {plataforma}")
        df_plataforma = df[df["Plataforma"] == plataforma].copy()

        # Redondear ratios
        for col in umbrales.keys():
            df_plataforma[col] = df_plataforma[col].round(2)

        # Aplicar colores a toda la tabla de ratios
        st.dataframe(
            df_plataforma.style.apply(
                lambda row: [colorear_valor(v, c) for c, v in zip(df_plataforma.columns, row)],
                axis=1
            )
        )

else:
    st.info("📥 Subí un archivo Excel para continuar.")
