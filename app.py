import streamlit as st
import random

st.set_page_config(page_title="Golpea al Monstruo", page_icon="👾", layout="centered")

st.title("👾 ¡Juego Interactivo: Golpea al Monstruo! 👾")
st.write("Mira la operación arriba y toca al monstruo que tenga la respuesta correcta.")

# Inicializar estados del juego
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

# Crear opciones falsas para los otros monstruos
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

# --- PANTALLA DE JUEGO ---
# Tablero superior estilo Arcade
st.markdown(f"""
<div style="background-color: #2e2e3a; padding: 15px; border-radius: 15px; text-align: center; border: 3px solid #ff007f;">
    <h2 style="color: #00ffcc; margin: 0; font-family: 'Courier New', monospace;">RETO: {n1} {op} {n2} = ?</h2>
    <h4 style="color: #ff007f; margin: 5px 0 0 0;">🍪 Puntos en la panza: {st.session_state.score}</h4>
</div>
""", unsafe_allow_html=True)

st.write("")

# Mostrar el diseño de los monstruos tragones para elegir con un clic
cols = st.columns(2)

for i, opcion in enumerate(opciones):
    # Determinar qué tan gordito está el monstruo visualmente en el botón
    size_emoji = "👾" if st.session_state.score < 3 else "👹"
    
    with cols[i % 2]:
        # Cada monstruo es un botón interactivo gigante con su número
        if st.button(f"{size_emoji}\n\n {opcion} ", key=f"btn_{i}_{opcion}", use_container_width=True):
            if opcion == respuesta_correcta:
                st.session_state.score += 1
                st.success(f"💥 ¡ZAS! ¡Alimentaste al correcto! +1 Galleta 🍪")
                st.balloons()
                
                # Siguiente pregunta automática
                st.session_state.n1 = random.randint(1, 10)
                st.session_state.n2 = random.randint(1, 10)
                st.session_state.op = random.choice(['+', '-'])
                if st.session_state.op == '-' and st.session_state.n1 < st.session_state.n2:
                    st.session_state.n1, st.session_state.n2 = st.session_state.n2, st.session_state.n1
                st.session_state.actualizar_opciones = True
                st.rerun()
            else:
                st.error(f"❌ ¡Uf! Ese monstruo se quedó con hambre. ¡Intenta otra vez!")

# Opción para reiniciar el marcador
st.write("---")
if st.button("🔄 Reiniciar Marcador Arcadé"):
    st.session_state.score = 0
    st.session_state.actualizar_opciones = True
    st.rerun()
