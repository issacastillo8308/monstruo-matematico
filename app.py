import streamlit as st

st.set_page_config(page_title="¡Reto Arcade Matemático!", page_icon="👾", layout="centered")

# Limpieza de pantalla para modo app nativa en celular
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0c0c14; }
    div.block-container { padding-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE JUEGO HTML5 + AUDIO WEB + TIEMPO ---
juego_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monstruos Matemáticos Arcade</title>
    <style>
        body {
            font-family: 'Arial Rounded MT Bold', sans-serif;
            background-color: #0c0c14;
            color: white;
            text-align: center;
            margin: 0;
            padding: 8px;
            user-select: none;
            -webkit-user-select: none;
        }
        /* Tablero Superior con Neón */
        .tablero-principal {
            background: linear-gradient(180deg, #161626 0%, #0b0b14 100%);
            border: 4px solid #ff007f;
            border-radius: 20px;
            padding: 12px;
            margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(255, 0, 127, 0.5);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 5px;
            font-size: 14px;
            color: #fffb00;
            margin-bottom: 10px;
        }
        .operacion {
            font-size: 42px;
            color: #00ffcc;
            margin: 5px 0;
            font-weight: bold;
            text-shadow: 0 0 12px rgba(0, 255, 204, 0.6);
        }
        /* Cuadrícula de Juego */
        .grid-monstruos {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            max-width: 380px;
            margin: 0 auto;
        }
        .tarjeta-monstruo {
            background: #141426;
            border: 3px solid #32324d;
            border-radius: 20px;
            padding: 12px;
            position: relative;
            cursor: pointer;
            box-shadow: 0 6px 0 #07070f;
            transition: all 0.05s ease;
        }
        .tarjeta-monstruo:active {
            transform: translateY(4px);
            box-shadow: 0 2px 0 #07070f;
        }
        /* Gráficos de Monstruos (Vectores CSS) */
        .dibujo-monstruo {
            width: 75px;
            height: 75px;
            background: #9b59b6;
            border-radius: 50% 50% 35% 35%;
            margin: 8px auto;
            position: relative;
            border: 3px solid #111;
            box-shadow: inset -4px -4px 0 rgba(0,0,0,0.2);
        }
        .dibujo-monstruo::before {
            content: '';
            position: absolute;
            top: 18px;
            left: 14px;
            width: 16px;
            height: 16px;
            background: white;
            border-radius: 50%;
            border: 2px solid #000;
            box-shadow: 26px 0 0 white, 26px 0 0 #000 inset;
        }
        .pupila {
            position: absolute;
            top: 24px;
            left: 20px;
            width: 6px;
            height: 6px;
            background: black;
            border-radius: 50%;
            box-shadow: 26px 0 0 black;
        }
        .boca {
            position: absolute;
            bottom: 12px;
            left: 22px;
            width: 26px;
            height: 10px;
            background: #1a1a2e;
            border-radius: 0 0 12px 12px;
            border: 2px solid #000;
            overflow: hidden;
        }
        .boca::before {
            content: '';
            position: absolute;
            top: 0; left: 3px;
            width: 0; height: 0;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid white;
            box-shadow: 10px 0 0 white;
        }
        .antena {
            position: absolute;
            top: -6px; left: 33px;
            width: 8px; height: 10px;
            background: #9b59b6;
            border: 3px solid #111;
            border-radius: 4px;
        }
        .numero-cartel {
            background: #ff007f;
            color: white;
            font-size: 26px;
            font-weight: bold;
            padding: 4px 18px;
            border-radius: 12px;
            display: inline-block;
            border: 2px solid #111;
            text-shadow: 1px 1px 0 #000;
        }
        /* Colores Alternativos */
        .m-verde { background: #2ecc71 !important; } .m-verde .antena { background: #2ecc71 !important; }
        .m-azul { background: #3498db !important; } .m-azul .antena { background: #3498db !important; }
        .m-amarillo { background: #f1c40f !important; } .m-amarillo .antena { background: #f1c40f !important; }
        
        /* Pantalla de Fin de Juego */
        .overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(12, 12, 20, 0.95);
            z-index: 10;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .btn-reiniciar {
            background: #00ffcc;
            color: black;
            border: none;
            padding: 15px 30px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 12px;
            cursor: pointer;
            margin-top: 20px;
            box-shadow: 0 0 15px #00ffcc;
        }
        /* Clases de efectos rápidos */
        .correcto-flash { background: #2ecc71 !important; }
        .incorrecto-flash { background: #e74c3c !important; }
    </style>
</head>
<body>

    <div id="pantalla-fin" class="overlay">
        <h1 style="color: #ff007f; font-size: 40px; margin: 0;">⏱️ ¡TIEMPO FUERA!</h1>
        <p style="font-size: 22px; margin: 15px 0;">Puntuación Final: <span id="final-puntos" style="color:#fffb00; font-weight:bold;">0</span></p>
        <button class="btn-reiniciar" onclick="reiniciarJuego()">🎮 JUGAR OTRA VEZ</button>
    </div>

    <div class="tablero-principal">
        <div class="stats-grid">
            <div>⏱️ Tiempo: <b id="timer" style="color:white; font-size:16px;">30</b>s</div>
            <div>🍪 Panza: <b id="puntos" style="color:white; font-size:16px;">0</b></div>
            <div>🏆 Récord: <b id="record" style="color:white; font-size:16px;">0</b></div>
        </div>
        <p class="operacion" id="operacion-texto">RETO: 0 + 0</p>
    </div>

    <div class="grid-monstruos">
        <div class="tarjeta-monstruo" onclick="tocarMonstruo(0)">
            <div class="antena"></div><div class="dibujo-monstruo"><div class="pupila"></div><div class="boca"></div></div>
            <div class="numero-cartel" id="opt-0">?</div>
        </div>
        <div class="tarjeta-monstruo" onclick="tocarMonstruo(1)">
            <div class="antena"></div><div class="dibujo-monstruo m-verde"><div class="pupila"></div><div class="boca"></div></div>
            <div class="numero-cartel" id="opt-1">?</div>
        </div>
        <div class="tarjeta-monstruo" onclick="tocarMonstruo(2)">
            <div class="antena"></div><div class="dibujo-monstruo m-azul"><div class="pupila"></div><div class="boca"></div></div>
            <div class="numero-cartel" id="opt-2">?</div>
        </div>
        <div class="tarjeta-monstruo" onclick="tocarMonstruo(3)">
            <div class="antena"></div><div class="dibujo-monstruo m-amarillo"><div class="pupila"></div><div class="boca"></div></div>
            <div class="numero-cartel" id="opt-3">?</div>
        </div>
    </div>

    <script>
        let puntos = 0;
        let record = 0;
        let tiempo = 30;
        let respuestaCorrecta = 0;
        let opciones = [];
        let juegoActivo = true;
        let cronometro;

        // --- SINTETIZADOR DE EFECTOS DE SONIDO (Web Audio API) ---
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        function sonar(tipo) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            if (tipo === 'correcto') {
                // Sonido Arcade de Moneda/Acierto Ascendente
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(523.25, audioCtx.currentTime); // Nota C5
                osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.08); // Nota A5
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
                osc.start(); osc.stop(audioCtx.currentTime + 0.25);
            } else if (tipo === 'incorrecto') {
                // Sonido Descendente de Error
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(180, audioCtx.currentTime);
                osc.frequency.linearRampToValueAtTime(80, audioCtx.currentTime + 0.2);
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
                osc.start(); osc.stop(audioCtx.currentTime + 0.2);
            } else if (tipo === 'fin') {
                // Pitido largo de Game Over
                osc.type = 'square';
                osc.frequency.setValueAtTime(330, audioCtx.currentTime);
                osc.frequency.setValueAtTime(220, audioCtx.currentTime + 0.15);
                gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.6);
                osc.start(); osc.stop(audioCtx.currentTime + 0.6);
            }
        }

        function generarReto() {
            let n1 = Math.floor(Math.random() * 10) + 1;
            let n2 = Math.floor(Math.random() * 10) + 1;
            let op = Math.random() > 0.5 ? '+' : '-';
            
            if (op === '-' && n1 < n2) { let t = n1; n1 = n2; n2 = t; }
            respuestaCorrecta = op === '+' ? n1 + n2 : n1 - n2;
            
            document.getElementById('operacion-texto').innerText = `RETO: ${n1} ${op} ${n2}`;

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

        function iniciarTiempo() {
            cronometro = setInterval(() => {
                if (!juegoActivo) return;
                tiempo--;
                document.getElementById('timer').innerText = tiempo;
                if (tiempo <= 0) {
                    finalizarJuego();
                }
            }, 1000);
        }

        function tocarMonstruo(indice) {
            if (!juegoActivo) return;
            let tarjeta = document.getElementsByClassName('tarjeta-monstruo')[indice];
            
            if (opciones[indice] === respuestaCorrecta) {
                puntos++;
                document.getElementById('puntos').innerText = puntos;
                if (puntos > record) {
                    record = puntos;
                    document.getElementById('record').innerText = record;
                }
                sonar('correcto');
                tarjeta.classList.add('correcto-flash');
                setTimeout(() => {
                    tarjeta.classList.remove('correcto-flash');
                    generarReto();
                }, 150);
            } else {
                sonar('incorrecto');
                tarjeta.classList.add('incorrecto-flash');
                setTimeout(() => {
                    tarjeta.classList.remove('incorrecto-flash');
                }, 200);
            }
        }

        function finalizarJuego() {
            juegoActivo = false;
            clearInterval(cronometro);
            sonar('fin');
            document.getElementById('final-puntos').innerText = puntos;
            document.getElementById('pantalla-fin').style.display = 'flex';
        }

        function reiniciarJuego() {
            puntos = 0;
            tiempo = 30;
            juegoActivo = true;
            document.getElementById('puntos').innerText = puntos;
            document.getElementById('timer').innerText = tiempo;
            document.getElementById('pantalla-fin').style.display = 'none';
            generarReto();
            clearInterval(cronometro);
            iniciarTiempo();
        }

        // Encendido inicial
        generarReto();
        iniciarTiempo();
    </script>
</body>
</html>
"""

st.components.v1.html(juego_html, height=540, scrolling=False)
