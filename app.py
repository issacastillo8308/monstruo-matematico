import streamlit as st
import random

st.set_page_config(page_title="Reto Matemático", page_icon="⚡")

st.title("👾 ¡El Monstruo de los Números! 👾")
st.subheader("Resuelve la operación para alimentar al monstruo.")

# Inicializar variables en la sesión para que no cambien al escribir
if 'num1' not in st.session_state:
    st.session_state.num1 = random.randint(1, 10)
    st.session_state.num2 = random.randint(1, 10)
    st.session_state.operacion = random.choice(['+', '-'])
    if st.session_state.operacion == '-' and st.session_state.num1 < st.session_state.num2:
        st.session_state.num1, st.session_state.num2 = st.session_state.num2, st.session_state.num1

n1 = st.session_state.num1
n2 = st.session_state.num2
op = st.session_state.operacion

st.header(f"¿Cuánto es {n1} {op} {n2}? 🤔")

respuesta = st.number_input("Tu respuesta aquí 👇", min_value=0, step=1, key="resp")

if st.button("🎯 COMPROBAR RESULTADO"):
    correcto = n1 + n2 if op == '+' else n1 - n2
    if respuesta == correcto:
        st.success(f"🎉 ¡EXCELENTE! {n1} {op} {n2} es igual a {correcto}. ¡El monstruo está feliz!")
        st.balloons()
        # Botón para generar otro reto
        if st.button("🔄 Jugar otra vez"):
            del st.session_state.num1
            st.rerun()
    else:
        st.error("❌ ¡Uf, casi! Inténtalo de nuevo.")
