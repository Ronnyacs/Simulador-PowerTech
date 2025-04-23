import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

st.set_page_config(page_title="Simulador PowerTech", layout="centered")
st.title("🚗 Simulador PowerTech - Velocidad por Marcha")

# Entrada de parámetros
marchas = 6
diff = st.number_input("Relación de diferencial", value=4.1)
diametro = st.number_input("Diámetro del neumático (m)", value=0.6676)

st.markdown("---")

# Relación de cada marcha
st.subheader("Relaciones de caja")
relaciones = []
cols = st.columns(marchas)
def valores_por_defecto(i):
    por_defecto = [4.529, 2.517, 1.519, 1.0, 0.741, 0.620]
    return float(por_defecto[i]) if i < len(por_defecto) else 1.0

for i in range(marchas):
    relaciones.append(cols[i].number_input(f"{i+1}ª marcha", value=valores_por_defecto(i)))

# Calcular tabla de velocidad por RPM
st.markdown("---")
st.subheader("Tabla de velocidades por RPM")
rpm_range = np.arange(1000, 5500, 100)
data = {"RPM": rpm_range}

for i, rel in enumerate(relaciones):
    data[f"{i+1}ª"] = [(rpm * pi * diametro * 60) / (rel * diff * 1000) for rpm in rpm_range]

df_vel = pd.DataFrame(data)
st.dataframe(df_vel, use_container_width=True)

# Gráfica sin recomendaciones
st.markdown("---")
st.subheader("📈 Gráfica Velocidad vs RPM")
fig, ax = plt.subplots()

colores = ['blue', 'red', 'green', 'purple', 'deepskyblue', 'orange']

for i in range(marchas):
    ax.plot(df_vel["RPM"], df_vel[f"{i+1}ª"], label=f"{i+1}ª", color=colores[i])

ax.set_xlabel("RPM")
ax.set_ylabel("Velocidad (km/h)")
ax.legend()
ax.grid(True)
st.pyplot(fig)
