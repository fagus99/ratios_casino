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
    df["Retiro/recarga"] = df["Retiros de saldo"] / df["Recargas de saldo"]
    df["Win/recarga"] = df["Win o GGR"] / df["Recargas de saldo"]
    df["Win/retiros"] = df["Win o GGR"] / df["Retiros de saldo"]
    df["Win/bonus"] = df["Win o GGR"] / df["Bonus"]
    df["Bonus/win"] = df["Bonus"] / df["Win o GGR"]

    # ===== 3. Umbrales para colorear =====
    umbrales = {
        "Recarga/retiro": (1.0, 1.2),   # Ej: ideal entre 1.0 y 1.2
        "Retiro/recarga": (0.8, 1.0),   # Ej: ideal entre 0.8 y 1.0
        "Win/recarga": (0.15, 0.25),    # 15% a 25% del jugado
        "Win/retiros": (0.15, 0.25),
        "Win/bonus": (2, 6),
        "Bonus/win": (0.1, 0.3)
    }

    def colorear(val, col):
        try:
            low, high = umbrales[col]
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
        ax.plot(df_plat["Mes"], df_plat["Win/recarga"], marker="o", label="Win/Recarga")
        ax.plot(df_plat["Mes"], df_plat["Bonus/win"], marker="s", label="Bonus/Win")
        ax.axhline(umbrales["Win/recarga"][0], color="green", linestyle="--", alpha=0.6)
        ax.axhline(umbrales["Win/recarga"][1], color="green", linestyle="--", alpha=0.6)
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

