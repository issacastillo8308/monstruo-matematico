import streamlit as st

st.set_page_config(page_title="¡Reto Arcade Matemático!", page_icon="👾", layout="centered")

# Ocultar menús para modo app nativa
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0b0914; }
    div.block-container { padding-top: 0rem; padding-bottom: 0rem; }
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE JUEGO PREMIUM CON MONSTRUOS DETALLADOS Y CONFETI ---
juego_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monstruos Arcade Pro</title>
    <style>
        body {
            font-family: 'Arial Rounded MT Bold', sans-serif;
            background-color: #0b0914;
            background-image: 
                linear-gradient(rgba(255, 0, 127, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 0, 127, 0.1) 1px, transparent 1px);
            background-size: 40px 40px;
            color: white;
            text-align: center;
            margin: 0;
            padding: 10px;
            overflow: hidden;
            user-select: none;
            -webkit-user-select: none;
        }

        /* Contenedor Principal */
        .game-wrapper {
            max-width: 420px;
            margin: 0 auto;
            position: relative;
        }

        /* Tablero de Neon Superior */
        .tablero-neon {
            background: rgba(22, 16, 41, 0.9);
            border: 4px solid #ff007f;
            border-radius: 24px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 0 20px #ff007f, inset 0 0 10px #ff007f;
            position: relative;
        }
        .stats-bar {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 5px;
            font-size: 13px;
            color: #fffb00;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .operacion-titulo {
            font-size: 46px;
            color: #00ffcc;
            margin: 10px 0 0 0;
            font-weight: 900;
            text-shadow: 0 0 15px #00ffcc, 0 0 5px #00ffcc;
            letter-spacing: 1px;
        }

        /* Cuadrícula de Juego */
        .grid-monstruos {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        /* Botón de Monstruo Estilo Tarjeta Gamer */
        .tarjeta-arcade {
            background: #15102a;
            border: 3px solid #3d2b6b;
            border-radius: 24px;
            padding: 15px 10px;
            cursor: pointer;
            position: relative;
            box-shadow: 0 8px 0 #080512, 0 10px 20px rgba(0,0,0,0.5);
            transition: all 0.05s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .tarjeta-arcade:active {
            transform: translateY(6px);
            box-shadow: 0 2px 0 #080512;
        }

        /* --- MONSTRUOS EN SVG VECTORIAL (Detallados y con cuernos) --- */
        .monster-svg {
            width: 105px;
            height: 105px;
            filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3));
            animation: bounce 2s infinite ease-in-out;
        }
        .m1 { animation-delay: 0s; }
        .m2 { animation-delay: 0.3s; }
        .m3 { animation-delay: 0.6s; }
        .m4 { animation-delay: 0.9s; }

        @keyframes bounce {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-6px) scale(1.02); }
        }

        /* Cartel de Número */
        .badge-numero {
            background: linear-gradient(180deg, #ff007f 0%, #cc0066 100%);
            color: white;
            font-size: 28px;
            font-weight: bold;
            padding: 6px 24px;
            border-radius: 14px;
            margin-top: 10px;
            border: 2px solid #ffffff;
            box-shadow: 0 4px 0 #800040;
            text-shadow: 1px 2px 2px rgba(0,0,0,0.5);
            min-width: 50px;
        }

        /* Efectos Especiales de Impacto */
        .correcto-impacto { background: #2ecc71 !important; border-color: #fff !important; box-shadow: 0 0 25px #2ecc71 !important; }
        .incorrecto-impacto { background: #e74c3c !important; border-color: #fff !important; box-shadow: 0 0 25px #e74c3c !important; }

        /* Pantalla de Game Over */
        .game-over-screen {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(11, 9, 20, 0.98);
            z-index: 100;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .btn-restart {
            background: linear-gradient(180deg, #00ffcc 0%, #00b38f 100%);
            color: black;
            border: 3px solid white;
            padding: 16px 36px;
            font-size: 22px;
            font-weight: bold;
            border-radius: 16px;
            cursor: pointer;
            margin-top: 25px;
            box-shadow: 0 0 20px #00ffcc;
        }

        /* Canvas para Partículas de Confeti */
        #confetti-canvas {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: 50;
        }
    </style>
</head>
<body>

    <canvas id="confetti-canvas"></canvas>

    <div id="pantalla-fin" class="game-over-screen">
        <h1 style="color: #ff007f; font-size: 46px; margin: 0; text-shadow: 0 0 15px #ff007f;">⏱️ ¡TIEMPO!</h1>
        <p style="font-size: 24px; margin: 15px 0;">Puntuación Lograda: <span id="final-puntos" style="color:#fffb00; font-weight:bold; font-size: 32px;">0</span></p>
        <button class="btn-restart" onclick="reiniciarJuego()">🎮 VOLVER A JUGAR</button>
    </div>

    <div class="game-wrapper">
        <div class="tablero-neon">
            <div class="stats-bar">
                <div>⏱️ Tiempo: <b id="timer" style="color:white; font-size:16px;">30</b>s</div>
                <div>🍪 Panza: <b id="puntos" style="color:white; font-size:16px;">0</b></div>
                <div>🏆 Récord: <b id="record" style="color:white; font-size:16px;">0</b></div>
            </div>
            <p class="operacion-titulo" id="operacion-texto">RETO: 6 + 6</p>
        </div>

        <div class="grid-monstruos">
            <div class="tarjeta-arcade" onclick="tocarMonstruo(0)">
                <svg class="monster-svg m1" viewBox="0 0 100 100">
                    <rect x="25" y="8" width="10" height="15" rx="4" fill="#5b3475" stroke="#111" stroke-width="3"/>
                    <rect x="65" y="8" width="10" height="15" rx="4" fill="#5b3475" stroke="#111" stroke-width="3"/>
                    <ellipse cx="50" cy="55" rx="38" ry="35" fill="#8e44ad" stroke="#111" stroke-width="3.5"/>
                    <circle cx="50" cy="45" r="14" fill="white" stroke="#111" stroke-width="3"/>
                    <circle cx="50" cy="45" r="5" fill="black"/>
                    <path d="M 38 68 Q 50 82 62 68" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round"/>
                    <path d="M 44 69 L 46 74 L 48 69 Z M 52 69 L 54 74 L 56 69 Z" fill="white"/>
                </svg>
                <div class="badge-numero" id="opt-0">3</div>
            </div>

            <div class="tarjeta-arcade" onclick="tocarMonstruo(1)">
                <svg class="monster-svg m2" viewBox="0 0 100 100">
                    <path d="M 20 15 Q 30 5 35 25 M 80 15 Q 70 5 65 25" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round"/>
                    <ellipse cx="22" cy="12" rx="5" ry="5" fill="#f1c40f" stroke="#111" stroke-width="2"/>
                    <ellipse cx="78" cy="12" rx="5" ry="5" fill="#f1c40f" stroke="#111" stroke-width="2"/>
                    <ellipse cx="50" cy="55" rx="38" ry="35" fill="#2ecc71" stroke="#111" stroke-width="3.5"/>
                    <circle cx="35" cy="45" r="9" fill="white" stroke="#111" stroke-width="2.5"/>
                    <circle cx="35" cy="45" r="3.5" fill="black"/>
                    <circle cx="65" cy="45" r="9" fill="white" stroke="#111" stroke-width="2.5"/>
                    <circle cx="65" cy="45" r="3.5" fill="black"/>
                    <path d="M 35 68 Q 50 82 65 68" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round"/>
                    <path d="M 48 69 L 50 75 L 52 69 Z" fill="white"/>
                </svg>
                <div class="badge-numero" id="opt-1">0</div>
            </div>

            <div class="tarjeta-arcade" onclick="tocarMonstruo(2)">
                <svg class="monster-svg m3" viewBox="0 0 100 100">
                    <path d="M 30 15 Q 50 2 70 15" fill="none" stroke="#111" stroke-width="4.5"/>
                    <ellipse cx="50" cy="55" rx="38" ry="35" fill="#3498db" stroke="#111" stroke-width="3.5"/>
                    <circle cx="32" cy="46" r="8" fill="white" stroke="#111" stroke-width="2"/>
                    <circle cx="32" cy="46" r="3" fill="black"/>
                    <circle cx="50" cy="40" r="9" fill="white" stroke="#111" stroke-width="2"/>
                    <circle cx="50" cy="40" r="3.5" fill="black"/>
                    <circle cx="68" cy="46" r="8" fill="white" stroke="#111" stroke-width="2"/>
                    <circle cx="68" cy="46" r="3" fill="black"/>
                    <rect x="34" y="66" width="32" height="8" rx="4" fill="#2c3e50" stroke="#111" stroke-width="2.5"/>
                    <path d="M 40 66 L 42 70 L 44 66 M 56 66 L 58 70 L 60 66" fill="none" stroke="white" stroke-width="2"/>
                </svg>
                <div class="badge-numero" id="opt-2">12</div>
            </div>

            <div class="tarjeta-arcade" onclick="tocarMonstruo(3)">
                <svg class="monster-svg m4" viewBox="0 0 100 100">
                    <path d="M 15 35 Q 5 25 15 50 M 85 35 Q 95 25 85 50" fill="#d35400" stroke="#111" stroke-width="3"/>
                    <ellipse cx="50" cy="55" rx="38" ry="35" fill="#f1c40f" stroke="#111" stroke-width="3.5"/>
                    <circle cx="34" cy="45" r="9" fill="white" stroke="#111" stroke-width="2.5"/>
                    <circle cx="34" cy="45" r="4" fill="black"/>
                    <circle cx="66" cy="45" r="9" fill="white" stroke="#111" stroke-width="2.5"/>
                    <circle cx="66" cy="45" r="4" fill="black"/>
                    <path d="M 32 66 Q 50 78 68 66" fill="#e67e22" stroke="#111" stroke-width="3"/>
                    <path d="M 42 67 L 44 71 L 46 68 M 54 68 L 56 71 L 58 67" fill="none" stroke="white" stroke-width="2"/>
                </svg>
                <div class="badge-numero" id="opt-3">17</div>
            </div>
        </div>
    </div>

    <script>
        let puntos = 0, record = 0, tiempo = 30;
        let respuestaCorrecta = 0, opciones = [], juegoActivo = true, cronometro;
        
        // --- EFECTOS DE CONFETI EN CANVAS ---
        const canvas = document.getElementById('confetti-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        
        function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        function lanzarConfeti() {
            for (let i = 0; i < 40; i++) {
                particles.push({
                    x: window.innerWidth / 2, y: window.innerHeight / 2,
                    angle: Math.random() * Math.PI * 2,
                    speed: Math.random() * 8 + 4,
                    color: `hsl(${Math.random() * 360}, 100%, 60%)`,
                    r: Math.random() * 5 + 3,
                    d: Math.random() * 20 + 20
                });
            }
        }

        function drawParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach((p, idx) => {
                p.x += Math.cos(p.angle) * p.speed;
                p.y += Math.sin(p.angle) * p.speed + 1.5; // Gravedad
                p.d--;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.fill();
                if (p.d <= 0) particles.splice(idx, 1);
            });
            requestAnimationFrame(drawParticles);
        }
        drawParticles();

        // --- SISTEMA DE AUDIO ARCADE ---
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function sonar(tipo) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            if (tipo === 'correcto') {
                osc.type = 'triangle'; osc.frequency.setValueAtTime(587.33, audioCtx.currentTime);
                osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.06);
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.2);
            } else if (tipo === 'incorrecto') {
                osc.type = 'sawtooth'; osc.frequency.setValueAtTime(150, audioCtx.currentTime);
                osc.frequency.linearRampToValueAtTime(70, audioCtx.currentTime + 0.15);
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.15);
            } else if (tipo === 'fin') {
                osc.type = 'square'; osc.frequency.setValueAtTime(293.66, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.2, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.5);
            }
        }

        // --- LÓGICA DE JUEGO ---
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
            opciones = Array.from(falsos); opciones.push(respuestaCorrecta);
            opciones.sort(() => Math.random() - 0.5);

            for(let i=0; i<4; i++) { document.getElementById(`opt-${i}`).innerText = opciones[i]; }
        }

        function iniciarTiempo() {
            cronometro = setInterval(() => {
                if (!juegoActivo) return;
                tiempo--;
                document.getElementById('timer').innerText = tiempo;
                if (tiempo <= 0) finalizarJuego();
            }, 1000);
        }

        function tocarMonstruo(indice) {
            if (!juegoActivo) return;
            let tarjeta = document.getElementsByClassName('tarjeta-arcade')[indice];
            if (opciones[indice] === respuestaCorrecta) {
                puntos++; document.getElementById('puntos').innerText = puntos;
                if (puntos > record) { record = puntos; document.getElementById('record').innerText = record; }
                sonar('correcto'); lanzarConfeti();
                tarjeta.classList.add('correcto-impacto');
                setTimeout(() => { tarjeta.classList.remove('correcto-impacto'); generarReto(); }, 120);
            } else {
                sonar('incorrecto'); tarjeta.classList.add('incorrecto-impacto');
                setTimeout(() => tarjeta.classList.remove('incorrecto-impacto'), 180);
            }
        }

        function finalizarJuego() {
            juegoActivo = false; clearInterval(cronometro); sonar('fin');
            document.getElementById('final-puntos').innerText = puntos;
            document.getElementById('pantalla-fin').style.display = 'flex';
        }

        function reiniciarJuego() {
            puntos = 0; tiempo = 30; juegoActivo = true;
            document.getElementById('puntos').innerText = puntos;
            document.getElementById('timer').innerText = tiempo;
            document.getElementById('pantalla-fin').style.display = 'none';
            generarReto(); clearInterval(cronometro); iniciarTiempo();
        }

        generarReto();
        iniciarTiempo();
    </script>
</body>
</html>
"""

st.components.v1.html(juego_html, height=560, scrolling=False)
