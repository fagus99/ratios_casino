import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Análisis de Ratios - Casino Online", layout="wide")
st.title("📊 Análisis de Ratios Financieros - Casino Online")

# ===== 1. Subir archivo =====
archivo = st.file_uploader("📥 Subí el archivo Excel con los datos", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)

    # Aseguramos tipos numéricos
    cols_numericas = ["Recargas de saldo", "Retiros de saldo", "Win o GGR", "Bonus"]
    for col in cols_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ===== 2. Calcular ratios =====
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

    # ===== 3. Umbrales para colorear (ajustables) =====
    umbrales = {
        "Recarga/retiro": (1.0, 1.2),
        "retiro/recarga": (0.8, 1.0),
        "win/recarga": (0.15, 0.25),
        "win/retiros": (0.15, 0.25),
        "bonos/win": (0.1, 0.3),
        "win/bonos": (2, 6),
        "bonos/retiros": (0.05, 0.25),
        "Bonos/recargas": (0.05, 0.25),
        "recargas/bonos": (3, 15),
        "retiros/bonos": (3, 15)
        # "Dif entre recarga y retiro" y "win / dif rec y ret" no tienen umbrales definidos fijos
    }

    def colorear(val, col):
        try:
            low, high = umbrales[col]
            if pd.isna(val):
                return ''
            color = 'background-color: lightgreen' if low <= val <= high else 'background-color: salmon'
        except:
            color = ''
        return color

    # ===== 4. Mostrar análisis por plataforma =====
    plataformas = df["Plataforma"].unique()

    for plataforma in plataformas:
        st.subheader(f"📍 Plataforma: {plataforma}")
        df_plat = df[df["Plataforma"] == plataforma].copy()

        # Mostrar tabla coloreada
        st.dataframe(
            df_plat.style.apply(lambda row: [colorear(row[col], col) if col in umbrales else '' for col in df_plat.columns], axis=1)
        )

        # ===== 5. Gráficos =====
        st.write("### 📈 Tendencia Win/Recarga y Bonus/Win")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df_plat["Mes"], df_plat["win/recarga"], marker="o", label="Win/Recarga")
        ax.plot(df_plat["Mes"], df_plat["bonos/win"], marker="s", label="Bonus/Win")
        ax.axhline(umbrales["win/recarga"][0], color="green", linestyle="--", alpha=0.6)
        ax.axhline(umbrales["win/recarga"][1], color="green", linestyle="--", alpha=0.6)
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # ===== 6. Alertas =====
        alertas = []
        for col, (low, high) in umbrales.items():
            fuera = df_plat[(df_plat[col] < low) | (df_plat[col] > high)]
            if not fuera.empty:
                alertas.append(f"⚠ {col} fuera de rango en {len(fuera)} registros.")
        if alertas:
            st.warning("\n".join(alertas))
        else:
            st.success("✅ Todos los indicadores en rango para esta plataforma.")
