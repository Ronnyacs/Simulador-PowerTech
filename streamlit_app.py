import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

st.set_page_config(page_title="Simulador PowerTech", layout="centered")
st.title("🚗 Simulador PowerTech - Velocidad por Marcha y Cambios Óptimos")

# Entrada de parámetros
torque = st.number_input("Par máximo (Nm)", value=373)
rpm_torque = st.number_input("RPM de par máximo", value=3200)
potencia = st.number_input("Potencia máxima (HP)", value=212)
rpm_pot = st.number_input("RPM de potencia máxima", value=4600)
marchas = st.number_input("Número de marchas", min_value=2, max_value=10, value=5)
diff = st.number_input("Relación de diferencial", value=4.1)
diametro = st.number_input("Diámetro del neumático (m)", value=0.6676)
peso = st.number_input("Peso del vehículo (kg)", value=2600)

st.markdown("---")

# Relación de cada marcha
st.subheader("Relaciones de caja")
relaciones = []
cols = st.columns(int(marchas))
for i in range(int(marchas)):
    relaciones.append(cols[i].number_input(f"{i+1}ª marcha", value=float([4.529, 2.517, 1.519, 1.0, 0.741][i]) if i < 5 else 1.0))

# Calcular tabla de velocidad por RPM
st.markdown("---")
st.subheader("Tabla de velocidades por RPM")
rpm_range = np.arange(1000, 5500, 100)
data = {"RPM": rpm_range}

for i, rel in enumerate(relaciones):
    data[f"{i+1}ª"] = [(rpm * pi * diametro * 60) / (rel * diff * 1000) for rpm in rpm_range]

df_vel = pd.DataFrame(data)
st.dataframe(df_vel, use_container_width=True)

# Análisis de cambios óptimos
st.markdown("---")
st.subheader("📌 Recomendaciones de cambio óptimo")
recomendaciones = []
for i in range(1, len(relaciones)):
    col_actual = f"{i}ª"
    col_sig = f"{i+1}ª"
    for j in range(len(df_vel)):
        if df_vel[col_sig][j] >= df_vel[col_actual][j]:
            recomendaciones.append((col_actual, col_sig, df_vel["RPM"][j], round(df_vel[col_actual][j], 1)))
            break

for cambio in recomendaciones:
    st.markdown(f"➡️ Cambia de **{cambio[0]}** a **{cambio[1]}** a **{cambio[2]} RPM** (~{cambio[3]} km/h)")

# Gráfica
st.markdown("---")
st.subheader("📈 Gráfica Velocidad vs RPM")
fig, ax = plt.subplots()
for i in range(int(marchas)):
    ax.plot(df_vel["RPM"], df_vel[f"{i+1}ª"], label=f"{i+1}ª")
for cambio in recomendaciones:
    ax.plot(cambio[2], cambio[3], 'ro')
    ax.text(cambio[2], cambio[3] + 1, f"{cambio[0]}→{cambio[1]}", fontsize=8, color='red')
ax.set_xlabel("RPM")
ax.set_ylabel("Velocidad (km/h)")
ax.legend()
ax.grid(True)
st.pyplot(fig)