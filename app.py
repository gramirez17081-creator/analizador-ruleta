import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Analizador Ruleta", layout="centered")
st.title("📊 Rastreador de Ruleta")

if 'historial' not in st.session_state:
    st.session_state.historial = []

ROJOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

def analizar_numero(n):
    if n == 0: return "Cero", "Cero", "Cero"
    paridad = "Par" if n % 2 == 0 else "Impar"
    color = "Rojo" if n in ROJOS else "Negro"
    rango = "1-18" if 1 <= n <= 18 else "19-36"
    return paridad, color, rango

# Entrada de datos
with st.form("entrada", clear_on_submit=True):
    nuevo_num = st.number_input("Ingresa el número:", min_value=0, max_value=36, step=1)
    boton = st.form_submit_button("Añadir Número")

if boton:
    st.session_state.historial.append(nuevo_num)

# Estadísticas
if st.session_state.historial:
    data = []
    for n in st.session_state.historial:
        p, c, r = analizar_numero(n)
        data.append({"Número": n, "Paridad": p, "Color": c, "Rango": r})
    
    df = pd.DataFrame(data)
    total_suertes = len(df[df["Número"] != 0])

    if total_suertes > 0:
        st.header("Análisis de Tendencias")
        
        # Agrupamos las métricas de 2 en 2 para que quepan bien
        c1, c2 = st.columns(2)
        
        with c1:
            # PAR / IMPAR
            val_par = (df["Paridad"] == "Par").sum() / total_suertes * 100
            st.metric("Pares", f"{val_par:.1f}%")
            st.metric("Impares", f"{100 - val_par:.1f}%")
            st.write("---")
            # ROJO / NEGRO
            val_rojo = (df["Color"] == "Rojo").sum() / total_suertes * 100
            st.metric("Rojo", f"{val_rojo:.1f}%")
            st.metric("Negro", f"{100 - val_rojo:.1f}%")

        with c2:
            # BAJO / ALTO
            val_bajo = (df["Rango"] == "1-18").sum() / total_suertes * 100
            st.metric("1-18 (Bajo)", f"{val_bajo:.1f}%")
            st.metric("19-36 (Alto)", f"{100 - val_bajo:.1f}%")

    # Historial
    st.write("### Últimos números:")
    st.info(", ".join(map(str, st.session_state.historial[-15:])))
    
    if st.button("Limpiar Historial"):
        st.session_state.historial = []
        st.rerun()
