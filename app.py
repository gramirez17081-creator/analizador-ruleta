import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Analizador Ruleta Pro", layout="centered")
st.title("📊 Rastreador y Asistente de Ruleta")

if 'historial' not in st.session_state:
    st.session_state.historial = []

ROJOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

def analizar_numero(n):
    if n == 0: return "Cero", "Cero", "Cero"
    paridad = "Par" if n % 2 == 0 else "Impar"
    color = "Rojo" if n in ROJOS else "Negro"
    rango = "1-18" if 1 <= n <= 18 else "19-36"
    return paridad, color, rango

# 2. Entrada de datos
with st.form("entrada", clear_on_submit=True):
    nuevo_num = st.number_input("Ingresa el número:", min_value=0, max_value=36, step=1)
    boton = st.form_submit_button("Añadir Número")

if boton:
    st.session_state.historial.append(nuevo_num)

# 3. Lógica de Análisis y Recomendación
if st.session_state.historial:
    data = []
    for n in st.session_state.historial:
        p, c, r = analizar_numero(n)
        data.append({"Número": n, "Paridad": p, "Color": c, "Rango": r})
    
    df = pd.DataFrame(data)
    df_sin_cero = df[df["Número"] != 0]
    total_suertes = len(df_sin_cero)

    if total_suertes > 0:
        st.subheader("📈 Análisis de Tendencias")
        
        # Cálculos de porcentajes
        p_par = (df_sin_cero["Paridad"] == "Par").sum() / total_suertes
        p_rojo = (df_sin_cero["Color"] == "Rojo").sum() / total_suertes
        p_bajo = (df_sin_cero["Rango"] == "1-18").sum() / total_suertes

        # ORGANIZACIÓN POR FILAS (Para evitar desorden)
        
        # Fila 1: COLORES
        st.write("**Color**")
        f1_c1, f1_c2 = st.columns(2)
        f1_c1.metric("Rojo", f"{p_rojo*100:.1f}%")
        f1_c2.metric("Negro", f"{(1-p_rojo)*100:.1f}%")
        
        # Fila 2: PARIDAD
        st.write("**Paridad**")
        f2_c1, f2_c2 = st.columns(2)
        f2_c1.metric("Pares", f"{p_par*100:.1f}%")
        f2_c2.metric("Impares", f"{(1-p_par)*100:.1f}%")
        
        # Fila 3: RANGOS
        st.write("**Rango**")
        f3_c1, f3_c2 = st.columns(2)
        f3_c1.metric("1-18 (Bajo)", f"{p_bajo*100:.1f}%")
        f3_c2.metric("19-36 (Alto)", f"{(1-p_bajo)*100:.1f}%")

        # --- SECCIÓN DE RECOMENDACIÓN (A partir de 8 números) ---
        st.write("---")
        if len(st.session_state.historial) >= 8:
            st.subheader("💡 Nota de Apuesta Sugerida")
            
            recomendaciones = []
            
            # Lógica: Sugerir lo que menos ha salido (reversión a la media)
            if p_rojo > 0.60: recomendaciones.append("Apostar a **NEGRO** (Atrasado)")
            elif p_rojo < 0.40: recomendaciones.append("Apostar a **ROJO** (Atrasado)")
            
            if p_par > 0.60: recomendaciones.append("Apostar a **IMPAR** (Atrasado)")
            elif p_par < 0.40: recomendaciones.append("Apostar a **PAR** (Atrasado)")
            
            if p_bajo > 0.60: recomendaciones.append("Apostar a **ALTO (19-36)** (Atrasado)")
            elif p_bajo < 0.40: recomendaciones.append("Apostar a **BAJO (1-18)** (Atrasado)")
            
            if recomendaciones:
                for rec in recomendaciones:
                    st.success(rec)
            else:
                st.info("Tendencias equilibradas. Espera una mayor desviación.")
        else:
            st.warning(f"Faltan {8 - len(st.session_state.historial)} números para generar recomendación.")

    # Historial
    st.write("### Historial Reciente:")
    st.info(", ".join(map(str, st.session_state.historial[-15:])))
    
    if st.button("🗑️ Limpiar Todo"):
        st.session_state.historial = []
        st.rerun()
