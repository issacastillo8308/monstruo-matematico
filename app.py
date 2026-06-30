import streamlit as st
import random

st.set_page_config(page_title="Monstruo Tragón", page_icon="👾")

st.title("👾 ¡El Monstruo Tragón de los Números! 👾")
st.write("¡Aliméntalo con respuestas correctas para hacerlo engordar!")

# Guardamos los aciertos y los números en la sesión
if 'aciertos' not in st.session_state:
    st.session_state.aciertos = 0
if 'num1' not in st.session_state:
    st.session_state.num1 = random.randint(1, 10)
    st.session_state.num2 = random.randint(1, 10)
    st.session_state.operacion = random.choice(['+', '-'])
    if st.session_state.operacion == '-' and st.session_state.num1 < st.session_state.num2:
        st.session_state.num1, st.session_state.num2 = st.session_state.num2, st.session_state.num1

n1 = st.session_state.num1
n2 = st.session_state.num2
op = st.session_state.operacion
puntos = st.session_state.aciertos

# --- LA EVOLUCIÓN DEL MONSTRUO (¡Aquí pasa la magia!) ---
st.markdown("### El estado de tu monstruo:")
if puntos == 0:
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>💀 <br><small style='font-size:15px;'>¡Tengo un chorro de hambre, mírame qué flaco!</small></h1>", unsafe_allow_html=True)
elif puntos == 1:
    st.markdown("<h1 style='text-align: center; font-size: 70px;'>👾 <br><small style='font-size:15px;'>¡Yumi! Ya me voy sintiendo mejor.</small></h1>", unsafe_allow_html=True)
elif puntos == 2:
    st.markdown("<h1 style='text-align: center; font-size: 100px;'>🤖 <br><small style='font-size:15px;'>¡Ya me creció la panza!</small></h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; font-size: 140px;'>👹 <br><small style='font-size:15px;'>¡ESTOY REVENTANDO DE GORDITO! ¡GRACIAS!</small></h1>", unsafe_allow_html=True)

st.write(f"✨ **Galletas acumuladas en su panza:** {puntos}")
st.write("---")

# Reto matemático
st.header(f"¿Cuánto es {n1} {op} {n2}? 🤔")
respuesta = st.number_input("Tu respuesta aquí 👇", min_value=0, step=1, key="resp")

if st.button("🎯 ¡ALIMENTAR!"):
    correcto = n1 + n2 if op == '+' else n1 - n2
    if respuesta == correcto:
        st.session_state.aciertos += 1
        st.success(f"🎉 ¡Esooo! {n1} {op} {n2} = {correcto}. ¡Le diste una galleta!")
        st.balloons()
        
        # Cambiamos de operación automáticamente para la próxima ronda
        st.session_state.num1 = random.randint(1, 10)
        st.session_state.num2 = random.randint(1, 10)
        st.session_state.operacion = random.choice(['+', '-'])
        if st.session_state.operacion == '-' and st.session_state.num1 < st.session_state.num2:
            st.session_state.num1, st.session_state.num2 = st.session_state.num2, st.session_state.num1
        st.rerun()
    else:
        st.error("❌ ¡Ay, no! Fallaste y el monstruo sigue con hambre. ¡Intenta otra vez!")

if st.button("🔄 Reiniciar juego / Vaciar monstruo"):
    st.session_state.aciertos = 0
    st.rerun()
