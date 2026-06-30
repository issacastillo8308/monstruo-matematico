import streamlit as st

st.set_page_config(page_title="¡Monstruos Mutantes Arcade!", page_icon="👾", layout="centered")

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

# --- MOTOR DE JUEGO CORREGIDO PARA QUE NO SE CORTE ---
juego_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monstruos con Patas y Brazos</title>
    <style>
        body {
            font-family: 'Arial Rounded MT Bold', sans-serif;
            background-color: #09070f;
            background-image: 
                linear-gradient(rgba(255, 0, 127, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 0, 127, 0.05) 1px, transparent 1px);
            background-size: 30px 30px;
            color: white;
            text-align: center;
            margin: 0;
            padding: 8px;
            overflow: hidden;
            user-select: none;
            -webkit-user-select: none;
        }

        .game-wrapper {
            max-width: 400px;
            margin: 0 auto;
        }

        /* Tablero de Neon */
        .tablero-neon {
            background: rgba(18, 11, 36, 0.95);
            border: 4px solid #ff007f;
            border-radius: 22px;
            padding: 12px;
            margin-bottom: 12px;
            box-shadow: 0 0 15px #ff007f;
        }
        .stats-bar {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 5px;
            font-size: 13px;
            color: #fffb00;
            text-transform: uppercase;
        }
        .operacion-titulo {
            font-size: 44px;
            color: #00ffcc;
            margin: 8px 0 0 0;
            font-weight: 900;
            text-shadow: 0 0 12px #00ffcc;
        }

        /* Rejilla 2x2 */
        .grid-monstruos {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }

        .tarjeta-arcade {
            background: #130f26;
            border: 3px solid #362563;
            border-radius: 22px;
            padding: 15px 5px;
            cursor: pointer;
            box-shadow: 0 6px 0 #05030f;
            transition: all 0.05s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .tarjeta-arcade:active {
            transform: translateY(4px);
            box-shadow: 0 2px 0 #05030f;
        }

        /* Contenedor Animado */
        .svg-container {
            width: 115px;
            height: 115px;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: bounce 1.5s infinite ease-in-out;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-4px) scale(1.03); }
        }

        .badge-numero {
            background: linear-gradient(180deg, #ff007f 0%, #b30059 100%);
            color: white;
            font-size: 26px;
            font-weight: bold;
            padding: 4px 22px;
            border-radius: 12px;
            margin-top: 8px;
            border: 2px solid #ffffff;
            box-shadow: 0 3px 0 #660033;
        }

        .correcto-impacto { background: #2ecc71 !important; box-shadow: 0 0 20px #2ecc71 !important; }
        .incorrecto-impacto { background: #e74c3c !important; box-shadow: 0 0 20px #e74c3c !important; }

        /* --- BOTÓN DE FACEBOOK --- */
        .fb-container {
            margin-top: 18px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .btn-fb-sigueme {
            display: inline-flex;
            align-items: center;
            background: #1877f2;
            color: white !important;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: bold;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            border: 2px solid white;
            box-shadow: 0 4px 15px rgba(24, 119, 242, 0.4);
            transition: all 0.2s ease;
        }
        .btn-fb-sigueme:active {
            transform: scale(0.95);
            box-shadow: 0 2px 5px rgba(24, 119, 242, 0.6);
        }
        .fb-icon {
            width: 20px;
            height: 20px;
            fill: white;
            margin-right: 10px;
        }
        .text-neon-fb {
            color: #00ffcc;
            margin-left: 5px;
            animation: pulse 1.2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 0.7; text-shadow: 0 0 2px #00ffcc; }
            50% { opacity: 1; text-shadow: 0 0 8px #00ffcc; }
        }

        .game-over-screen {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(9, 7, 15, 0.98);
            z-index: 100;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .btn-restart {
            background: #00ffcc;
            color: black;
            border: none;
            padding: 15px 32px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 14px;
            box-shadow: 0 0 15px #00ffcc;
        }
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
        <h1 style="color: #ff007f; font-size: 42px; margin: 0;">⏱️ ¡TIEMPO!</h1>
        <p style="font-size: 24px; margin: 15px 0;">Puntuación: <span id="final-puntos" style="color:#fffb00; font-weight:bold;">0</span></p>
        <button class="btn-restart" onclick="reiniciarJuego()">🎮 VOLVER A JUGAR</button>
    </div>

    <div class="game-wrapper">
        <div class="tablero-neon">
            <div class="stats-bar">
                <div>⏱️ Tiempo: <b id="timer" style="color:white;">30</b>s</div>
                <div>🍪 Panza: <b id="puntos" style="color:white;">0</b></div>
                <div>🏆 Récord: <b id="record" style="color:white;">0</b></div>
            </div>
            <p class="operacion-titulo" id="operacion-texto">RETO: 2 + 1</p>
        </div>

        <div class="grid-monstruos">
            <div class="tarjeta-arcade" onclick="tocarMonstruo(0)">
                <div class="svg-container" id="avatar-0"></div>
                <div class="badge-numero" id="opt-0">?</div>
            </div>
            <div class="tarjeta-arcade" onclick="tocarMonstruo(1)">
                <div class="svg-container" id="avatar-1" style="animation-delay: 0.2s;"></div>
                <div class="badge-numero" id="opt-1">?</div>
            </div>
            <div class="tarjeta-arcade" onclick="tocarMonstruo(2)">
                <div class="svg-container" id="avatar-2" style="animation-delay: 0.4s;"></div>
                <div class="badge-numero" id="opt-2">?</div>
            </div>
            <div class="tarjeta-arcade" onclick="tocarMonstruo(3)">
                <div class="svg-container" id="avatar-3" style="animation-delay: 0.6s;"></div>
                <div class="badge-numero" id="opt-3">?</div>
            </div>
        </div>

        <div class="fb-container">
            <a href="https://www.facebook.com/share/1F44VdrjnF/" target="_blank" class="btn-fb-sigueme">
                <svg class="fb-icon" viewBox="0 0 24 24">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
                Profa. Issa Castillo <span class="text-neon-fb">¡Sígueme! 👍</span>
            </a>
        </div>
    </div>

    <script>
        let puntos = 0, record = 0, tiempo = 30;
        let respuestaCorrecta = 0, opciones = [], juegoActivo = true, cronometro;
        
        const coloresMonster = ['#ff007f', '#2ecc71', '#3498db', '#f1c40f', '#9b59b6', '#e67e22', '#00ffcc'];
        
        function generarMonsterSVG(idContenedor) {
            const colorCuerpo = coloresMonster[Math.floor(Math.random() * coloresMonster.length)];
            const colorCuernos = coloresMonster[Math.floor(Math.random() * coloresMonster.length)];
            const tipoOjos = Math.random() > 0.4 ? 2 : 1; 
            const estiloBrazos = Math.floor(Math.random() * 2); 
            
            let brazosSVG = '';
            if (estiloBrazos === 0) {
                brazosSVG = `
                    <path d="M 20 55 Q 5 35 12 20" fill="none" stroke="${colorCuerpo}" stroke-width="10" stroke-linecap="round"/>
                    <circle cx="12" cy="18" r="6" fill="${colorCuernos}"/>
                    <path d="M 80 55 Q 95 35 88 20" fill="none" stroke="${colorCuerpo}" stroke-width="10" stroke-linecap="round"/>
                    <circle cx="88" cy="18" r="6" fill="${colorCuernos}"/>
                `;
            } else {
                brazosSVG = `
                    <path d="M 25 60 L 5 60" fill="none" stroke="${colorCuerpo}" stroke-width="11" stroke-linecap="round"/>
                    <path d="M 5 54 L 2 60 L 5 66" fill="none" stroke="${colorCuernos}" stroke-width="3"/>
                    <path d="M 75 60 L 95 60" fill="none" stroke="${colorCuerpo}" stroke-width="11" stroke-linecap="round"/>
                    <path d="M 95 54 L 98 60 L 95 66" fill="none" stroke="${colorCuernos}" stroke-width="3"/>
                `;
            }

            let patasSVG = `
                <rect x="30" y="78" width="12" height="15" rx="5" fill="${colorCuerpo}" stroke="#111" stroke-width="2"/>
                <ellipse cx="32" cy="92" rx="9" ry="5" fill="${colorCuernos}" stroke="#111" stroke-width="2"/>
                <rect x="58" y="78" width="12" height="15" rx="5" fill="${colorCuerpo}" stroke="#111" stroke-width="2"/>
                <ellipse cx="68" cy="92" rx="9" ry="5" fill="${colorCuernos}" stroke="#111" stroke-width="2"/>
            `;

            let cuernosSVG = `
                <path d="M 30 36 Q 14 10 26 6 Q 34 18 36 34" fill="${colorCuernos}" stroke="#111" stroke-width="3"/>
                <path d="M 70 36 Q 86 10 74 6 Q 66 18 64 34" fill="${colorCuernos}" stroke="#111" stroke-width="3"/>
            `;

            let ojosSVG = '';
            if (tipoOjos === 1) {
                ojosSVG = `<circle cx="50" cy="46" r="15" fill="white" stroke="#111" stroke-width="3"/>
                           <circle cx="50" cy="46" r="6" fill="black"/>
                           <circle cx="47" cy="43" r="2" fill="white"/>`;
            } else {
                ojosSVG = `<circle cx="36" cy="46" r="12" fill="white" stroke="#111" stroke-width="3"/>
                           <circle cx="36" cy="46" r="5" fill="black"/>
                           <circle cx="64" cy="46" r="12" fill="white" stroke="#111" stroke-width="3"/>
                           <circle cx="64" cy="46" r="5" fill="black"/>`;
            }

            const svgCompleto = `
                <svg viewBox="0 0 100 100" style="width:100%; height:100%;">
                    ${brazosSVG}
                    ${patasSVG}
                    ${cuernosSVG}
                    <ellipse cx="50" cy="58" rx="28" ry="26" fill="${colorCuerpo}" stroke="#111" stroke-width="3.5"/>
                    <path d="M 44 33 L 50 25 L 56 33" fill="${colorCuerpo}" stroke="#111" stroke-width="2.5"/>
                    ${ojosSVG}
                    <path d="M 38 66 Q 50 76 62 66" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round"/>
                    <path d="M 43 67 L 45 72 L 47 67 Z M 53 67 L 55 72 L 57 67 Z" fill="white"/>
                </svg>
            `;
            document.getElementById(idContenedor).innerHTML = svgCompleto;
        }

        const canvas = document.getElementById('confetti-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        window.addEventListener('resize', resizeCanvas); resizeCanvas();

        function lanzarConfeti() {
            for (let i = 0; i < 35; i++) {
                particles.push({
                    x: window.innerWidth / 2, y: window.innerHeight / 2,
                    angle: Math.random() * Math.PI * 2, speed: Math.random() * 6 + 4,
                    color: `hsl(${Math.random() * 360}, 100%, 60%)`, r: Math.random() * 4 + 3, d: 25
                });
            }
        }
        function drawParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach((p, idx) => {
                p.x += Math.cos(p.angle) * p.speed; p.y += Math.sin(p.angle) * p.speed + 1.5; p.d--;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fillStyle = p.color; ctx.fill();
                if (p.d <= 0) particles.splice(idx, 1);
            });
            requestAnimationFrame(drawParticles);
        }
        drawParticles();

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function sonar(tipo) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            if (tipo === 'correcto') {
                osc.type = 'triangle'; osc.frequency.setValueAtTime(587.33, audioCtx.currentTime);
                osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.05);
                gain.gain.setValueAtTime(0.12, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.18);
            } else if (tipo === 'incorrecto') {
                osc.type = 'sawtooth'; osc.frequency.setValueAtTime(140, audioCtx.currentTime);
                osc.frequency.linearRampToValueAtTime(60, audioCtx.currentTime + 0.12);
                gain.gain.setValueAtTime(0.12, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.12);
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
            opciones = Array.from(falsos); opciones.push(respuestaCorrecta);
            opciones.sort(() => Math.random() - 0.5);

            for(let i=0; i<4; i++) { 
                document.getElementById(`opt-${i}`).innerText = opciones[i]; 
                generarMonsterSVG(`avatar-${i}`); 
            }
        }

        function iniciarTiempo() {
            cronometro = setInterval(() => {
                if (!juegoActActive) return;
                tiempo--; document.getElementById('timer').innerText = tiempo;
                if (tiempo <= 0) { juegoActActive = false; document.getElementById('final-puntos').innerText = puntos; document.getElementById('pantalla-fin').style.display = 'flex'; }
            }, 1000);
        }
        let juegoActActive = true;

        function tocarMonstruo(indice) {
            if (!juegoActActive) return;
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

        function reiniciarJuego() {
            puntos = 0; tiempo = 30; juegoActActive = true;
            document.getElementById('puntos').innerText = puntos; document.getElementById('timer').innerText = tiempo;
            document.getElementById('pantalla-fin').style.display = 'none';
            generarReto();
        }

        generarReto();
        iniciarTiempo();
    </script>
</body>
</html>
"""

# AQUÍ ESTÁ EL CAMBIO CLAVE: Subimos a 640 para dar espacio libre abajo
st.components.v1.html(juego_html, height=640, scrolling=False)
