import streamlit as st
import pandas as pd

# 1. Configuración de la página (Optimizado para móvil)
st.set_page_config(page_title="Analizador Ruleta", layout="centered")
st.title("📊 Rastreador de Ruleta")

# 2. Inicializar el historial en la sesión
if 'historial' not in st.session_state:
    st.session_state.historial = []

# 3. Definición de propiedades de los números
ROJOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

def analizar_numero(n):
    if n == 0:
        return "Cero", "Cero", "Cero"
    
    paridad = "Par" if n % 2 == 0 else "Impar"
    color = "Rojo" if n in ROJOS else "Negro"
    rango = "1-18" if 1 <= n <= 18 else "19-36"
    
    return paridad, color, rango

# 4. Entrada de datos (Formulario fácil de tocar en celular)
with st.form("entrada", clear_on_submit=True):
    nuevo_num = st.number_input("Ingresa el número:", min_value=0, max_value=36, step=1)
    boton = st.form_submit_button("Añadir Número")

if boton:
    st.session_state.historial.append(nuevo_num)

# 5. Cálculos y Estadísticas
if st.session_state.historial:
    data = []
    for n in st.session_state.historial:
        p, c, r = analizar_numero(n)
        data.append({"Número": n, "Paridad": p, "Color": c, "Rango": r})
    
    df = pd.DataFrame(data)
    # Excluimos el 0 para las estadísticas de color/paridad/rango
    total_suertes = len(df[df["Número"] != 0])

    if total_suertes > 0:
        st.subheader("Análisis de Tendencias")
        
        # Usamos 2 columnas para que no se vea pequeño en el móvil
        col1, col2 = st.columns(2)
        
        with col1:
            p_par = (df["Paridad"] == "Par").sum() / total_suertes * 100
            st.metric("Pares", f"{p_par:.1f}%")
            
            p_rojo = (df["Color"] == "Rojo").sum() / total_suertes * 100
