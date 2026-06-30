import streamlit as st
import random

st.set_page_config(page_title="Golpea al Monstruo", page_icon="👾", layout="centered")

# --- DISEÑO DE GRÁFICOS Y ESTILOS (CSS) ---
st.markdown("""
<style>
    /* Fondo general del juego */
    .stApp {
        background-color: #12121c !important;
    }
    
    /* Contenedor del reto superior */
    .tablero-arcade {
        background: linear-gradient(135deg, #1f1f3a 0%, #2d1b4e 100%);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        border: 4px solid #00ffcc;
        box-shadow: 0px 0px 15px #00ffcc;
        margin-bottom: 25px;
    }
    
    /* Texto del reto */
    .texto-reto {
        color: #ff007f !important;
        font-size: 32px !important;
        font-weight: bold;
        font-family: 'Trebuchet MS', sans-serif;
        text-shadow: 2px 2px #000;
        margin: 0;
    }
    
    /* Marcador de galletas */
    .marcador {
        color: #fffb00 !important;
        font-size: 18px !important;
        margin-top: 10px;
    }

    /* Modificar los botones nativos de Streamlit para que parezcan monstruos chidos */
    div.stButton > button {
        background: linear-gradient(145deg, #ff007f, #b30059) !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0px 4px 10px rgba(255, 0, 127, 0.4) !important;
        padding: 15px 0px !important;
        transition: all 0.2s ease !important;
    }
    
    /* Efecto al presionar el monstruo */
    div.stButton > button:active {
        transform: scale(0.95) !important;
        box-shadow: 0px 2px 5px rgba(255, 0, 127, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DEL JUEGO ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(1, 10)
    st.session_state.n2 = random.randint(1, 10)
    st.session_state.op = random.choice(['+', '-'])
    if st.session_state.op == '-' and st.session_state.n1 < st.session_state.n2:
        st.session_state.n1, st.session_state.n2 = st.session_state.n2, st.session_state.n1

n1, n2, op = st.session_state.n1, st.session_state.n2, st.session_state.op
respuesta_correcta = n1 + n2 if op == '+' else n1 - n2

if 'opciones' not in st.session_state or st.session_state.get('actualizar_opciones', False):
    falsos = set()
    while len(falsos) < 3:
        f = random.randint(0, 20)
        if f != respuesta_correcta:
            falsos.add(f)
    opciones = list(falsos) + [respuesta_correcta]
    random.shuffle(opciones)
    st.session_state.opciones = opciones
    st.session_state.actualizar_opciones = False

opciones = st.session_state.opciones

# --- PANTALLA VISUAL ---
st.markdown(f"""
<div class="tablero-arcade">
    <p class="texto-reto">👾 RETO: {n1} {op} {n2} 👾</p>
    <p class="marcador">🍪 Galletas devoradas: <b>{st.session_state.score}</b></p>
</div>
""", unsafe_allow_html=True)

st.write("<p style='text-align:center; color:#aaa;'>👇 ¡Toca al monstruo con la respuesta correcta! 👇</p>", unsafe_allow_html=True)

# Cuadrícula de 2x2 para que se acomoden perfecto en el celular
col1, col2 = st.columns(2)

# Monstruos dinámicos según los puntos
emoji_monstruo = "👾" if st.session_state.score < 3 else "👹"
if st.session_state.score >= 6:
    emoji_monstruo = "🛸"

with col1:
    if st.button(f"{emoji_monstruo}\n\n{opciones[0]}", key="btn_0", use_container_width=True):
        accion_click = opciones[0]
    if st.button(f"{emoji_monstruo}\n\n{opciones[1]}", key="btn_1", use_container_width=True):
        accion_click = opciones[1]

with col2:
    if st.button(f"{emoji_monstruo}\n\n{opciones[2]}", key="btn_2", use_container_width=True):
        accion_click = opciones[2]
    if st.button(f"{emoji_monstruo}\n\n{opciones[3]}", key="btn_3", use_container_width=True):
        accion_click = opciones[3]

# Procesar el resultado del clic
if 'accion_click' in locals():
    if accion_click == respuesta_correcta:
        st.session_state.score += 1
        st.success("💥 ¡ZAS! ¡Alimentaste al correcto!")
        st.balloons()
        
        # Siguiente ronda
        st.session_state.n1 = random.randint(1, 10)
        st.session_state.n2 = random.randint(1, 10)
        st.session_state.op = random.choice(['+', '-'])
        if st.session_state.op == '-' and st.session_state.n1 < st.session_state.n2:
            st.session_state.n1, st.session_state.n2 = st.session_state.n2, st.session_state.n1
        st.session_state.actualizar_opciones = True
        st.rerun()
    else:
        st.error("❌ ¡Ups! Ese monstruo no tiene esa respuesta. ¡Intenta otra vez!")

# Reiniciar
st.write("---")
if st.button("🔄 Reiniciar Juego"):
    st.session_state.score = 0
    st.session_state.actualizar_opciones = True
    st.rerun()
