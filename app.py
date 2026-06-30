import streamlit as st

st.set_page_config(page_title="¡Golpea al Monstruo!", page_icon="👾", layout="centered")

# Ocultar los menús por defecto de Streamlit para que parezca una app nativa
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0d0d13; }
    div.block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# --- JUEGO EN JAVASCRIPT Y HTML5 PREMIUM (Estilo Arcade) ---
juego_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Golpea al Monstruo</title>
    <style>
        body {
            font-family: 'Arial Rounded MT Bold', sans-serif;
            background-color: #0d0d13;
            color: white;
            text-align: center;
            margin: 0;
            padding: 10px;
            user-select: none;
        }
        /* Tablero Superior de la Operación */
        .marcador-container {
            background: linear-gradient(180deg, #1b1b2f 0%, #111122 100%);
            border: 4px solid #00ffcc;
            border-radius: 20px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 0 20px #00ffcc;
        }
        .operacion {
            font-size: 38px;
            color: #ff007f;
            margin: 0;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(255, 0, 127, 0.6);
        }
        .puntos {
            font-size: 18px;
            color: #fffb00;
            margin: 5px 0 0 0;
        }
        /* Cuadrícula de los Monstruos Animados */
        .grid-monstruos {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            max-width: 400px;
            margin: 0 auto;
        }
        /* El contenedor del Monstruo Caricatura */
        .tarjeta-monstruo {
            background: #1a1a2e;
            border: 3px solid #3d3d5c;
            border-radius: 20px;
            padding: 10px;
            position: relative;
            cursor: pointer;
            box-shadow: 0 8px 0 #111122;
            transition: all 0.1s ease;
        }
        .tarjeta-monstruo:active {
            transform: translateY(6px);
            box-shadow: 0 2px 0 #111122;
        }
        /* Dibujo del Monstruo con puro CSS Avanzado (Vectores limpios y coloridos) */
        .dibujo-monstruo {
            width: 80px;
            height: 80px;
            background: #8e44ad;
            border-radius: 50% 50% 40% 40%;
            margin: 10px auto;
            position: relative;
            border: 3px solid #222;
            box-shadow: inset -5px -5px 0 rgba(0,0,0,0.2);
        }
        /* Ojos locos de caricatura */
        .dibujo-monstruo::before {
            content: '';
            position: absolute;
            top: 20px;
            left: 15px;
            width: 18px;
            height: 18px;
            background: white;
            border-radius: 50%;
            border: 2px solid #000;
            box-shadow: 30px 0 0 white, 30px 0 0 #000 inset; /* Segundo ojo */
        }
        /* Pupilas del monstruo */
        .pupila {
            position: absolute;
            top: 27px;
            left: 22px;
            width: 6px;
            height: 6px;
            background: black;
            border-radius: 50%;
            box-shadow: 30px 0 0 black;
        }
        /* Boca con colmillos de fuera */
        .boca {
            position: absolute;
            bottom: 15px;
            left: 25px;
            width: 30px;
            height: 12px;
            background: #2c3e50;
            border-radius: 0 0 15px 15px;
            border: 2px solid #000;
            overflow: hidden;
        }
        .boca::before {
            content: '';
            position: absolute;
            top: 0;
            left: 4px;
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid white;
            box-shadow: 12px 0 0 white;
        }
        /* Antenas divertidas */
        .antena {
            position: absolute;
            top: -8px;
            left: 35px;
            width: 10px;
            height: 12px;
            background: #8e44ad;
            border: 3px solid #222;
            border-radius: 5px;
        }
        /* Globos con el número de la respuesta */
        .numero-cartel {
            background: #00ffcc;
            color: #000;
            font-size: 24px;
            font-weight: bold;
            padding: 5px 15px;
            border-radius: 10px;
            display: inline-block;
            margin-top: 5px;
            border: 2px solid #222;
        }
        /* Variaciones de colores de monstruos según posición */
        .m-verde { background: #2ecc71 !important; }
        .m-verde .antena { background: #2ecc71 !important; }
        .m-naranja { background: #e67e22 !important; }
        .m-naranja .antena { background: #e67e22 !important; }
        .m-rojo { background: #e74c3c !important; }
        .m-rojo .antena { background: #e74c3c !important; }
        
        /* Animación de feedback */
        .flash-correcto { background: #2ecc71 !important; }
        .flash-incorrecto { background: #e74c3c !important; }
    </style>
</head>
<body>

    <div class="marcador-container">
        <p class="operacion" id="txt-operacion">RETO: 5 + 4</p>
        <p class="puntos">🍪 Monstruos Alimentados: <b id="txt-puntos">0</b></p>
    </div>

    <p style="color: #888; font-size: 14px; margin-bottom: 15px;">👇 ¡Golpea al monstruo correcto! 👇</p>

    <div class="grid-monstruos">
        <div class="tarjeta-monstruo" onclick="comprobar(0)">
            <div class="antena"></div>
            <div class="dibujo-monstruo">
                <div class="pupila"></div>
                <div class="boca"></div>
            </div>
            <div class="numero-cartel" id="opt-0">?</div>
        </div>
        <div class="tarjeta-monstruo" onclick="comprobar(1)">
            <div class="antena"></div>
            <div class="dibujo-monstruo m-verde">
                <div class="pupila"></div>
                <div class="boca"></div>
            </div>
            <div class="numero-cartel" id="opt-1">?</div>
        </div>
        <div class="tarjeta-monstruo" onclick="comprobar(2)">
            <div class="antena"></div>
            <div class="dibujo-monstruo m-naranja">
                <div class="pupila"></div>
                <div class="boca"></div>
            </div>
            <div class="numero-cartel" id="opt-2">?</div>
        </div>
        <div class="tarjeta-monstruo" onclick="comprobar(3)">
            <div class="antena"></div>
            <div class="dibujo-monstruo m-rojo">
                <div class="pupila"></div>
                <div class="boca"></div>
            </div>
            <div class="numero-cartel" id="opt-3">?</div>
        </div>
    </div>

    <script>
        let puntos = 0;
        let respuestaCorrecta = 0;
        let opciones = [];

        function generarPregunta() {
            let n1 = Math.floor(Math.random() * 10) + 1;
            let n2 = Math.floor(Math.random() * 10) + 1;
            let op = Math.random() > 0.5 ? '+' : '-';
            
            if (op === '-' && n1 < n2) {
                let temp = n1; n1 = n2; n2 = temp;
            }

            respuestaCorrecta = op === '+' ? n1 + n2 : n1 - n2;
            document.getElementById('txt-operacion').innerText = `RETO: ${n1} ${op} ${n2}`;

            let falsos = new Set();
            while(falsos.size < 3) {
                let f = Math.floor(Math.random() * 20);
                if (f !== respuestaCorrecta) falsos.add(f);
            }

            opciones = Array.from(falsos);
            opciones.push(respuestaCorrecta);
            opciones.sort(() => Math.random() - 0.5);

            for(let i=0; i<4; i++) {
                document.getElementById(`opt-${i}`).innerText = opciones[i];
            }
        }

        function comprobar(indice) {
            let tarjeta = document.getElementsByClassName('tarjeta-monstruo')[indice];
            if (opciones[indice] === respuestaCorrecta) {
                puntos++;
                document.getElementById('txt-puntos').innerText = puntos;
                tarjeta.classList.add('flash-correcto');
                setTimeout(() => {
                    tarjeta.classList.remove('flash-correcto');
                    generarPregunta();
                }, 300);
            } else {
                tarjeta.classList.add('flash-incorrecto');
                setTimeout(() => {
                    tarjeta.classList.remove('flash-incorrecto');
                }, 300);
            }
        }

        // Arrancar juego
        generarPregunta();
    </script>
</body>
</html>
"""

# Renderizar el juego nativo dentro de Streamlit a pantalla completa
st.components.v1.html(juego_html, height=550, scrolling=False)
