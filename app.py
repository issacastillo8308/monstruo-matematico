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

# --- MOTOR DE JUEGO ULTRA-DYNAMIC CON MONSTRUOS CON PELO Y MUTACIONES ---
juego_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monstruos Mutantes Arcade</title>
    <style>
        body {
            font-family: 'Arial Rounded MT Bold', sans-serif;
            background-color: #09070f;
            background-image: 
                linear-gradient(rgba(0, 255, 204, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 204, 0.05) 1px, transparent 1px);
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
            padding: 12px 5px;
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

        /* Contenedor del Monstruo Animado */
        .svg-container {
            width: 110px;
            height: 110px;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: bounce 1.8s infinite ease-in-out;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
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
            <p class="operacion-titulo" id="operacion-texto">RETO: 6 + 6</p>
        </div>

        <div class="grid-monstruos">
            <div class="tarjeta-arcade" onclick="tocarMonstruo(0)">
                <div class="svg-container" id="avatar-0"></div>
                <div class="badge-numero" id="opt-0">?</div>
            </div>
            <div class="tarjeta-arcade" onclick="tocarMonstruo(1)">
                <div class="svg-container" id="avatar-1" style="animation-delay: 0.3s;"></div>
                <div class="badge-numero" id="opt-1">?</div>
            </div>
            <div class="tarjeta-arcade" onclick="tocarMonstruo(2)">
                <div class="svg-container" id="avatar-2" style="animation-delay: 0.6s;"></div>
                <div class="badge-numero" id="opt-2">?</div>
            </div>
            <div class="tarjeta-arcade" onclick="tocarMonstruo(3)">
                <div class="svg-container" id="avatar-3" style="animation-delay: 0.9s;"></div>
                <div class="badge-numero" id="opt-3">?</div>
            </div>
        </div>
    </div>

    <script>
        let puntos = 0, record = 0, tiempo = 30;
        let respuestaCorrecta = 0, opciones = [], juegoActivo = true, cronometro;
        
        // Paletas de colores neón e hilos para simular pelaje
        const coloresMonster = ['#ff007f', '#2ecc71', '#3498db', '#f1c40f', '#9b59b6', '#e67e22', '#00ffcc'];
        
        // --- GENERADOR DE MONSTRUOS CON PELO Y CUERNOS MUTANTES ---
        function generarMonsterSVG(idContenedor) {
            const colorCuerpo = coloresMonster[Math.floor(Math.random() * coloresMonster.length)];
            const colorCuernos = coloresMonster[Math.floor(Math.random() * coloresMonster.length)];
            const tipoOjos = Math.random() > 0.5 ? 2 : 1; // 1 ojo o 2 ojos locos
            const estiloCuernos = Math.floor(Math.random() * 3); // 3 formas de cuernos distintos
            
            let cuernosSVG = '';
            if (estiloCuernos === 0) {
                // Cuernos puntiagudos hacia arriba
                cuernosSVG = `<path d="M 22 35 L 12 12 Q 25 20 28 32 Z M 78 35 L 88 12 Q 75 20 72 32 Z" fill="${colorCuernos}" stroke="#111" stroke-width="3"/>`;
            } else if (estiloCuernos === 1) {
                // Cuernos curveados de toro
                cuernosSVG = `<path d="M 20 40 Q -2 20 10 5 L 18 20 Z M 80 40 Q 102 20 90 5 L 82 20 Z" fill="${colorCuernos}" stroke="#111" stroke-width="3"/>`;
            } else {
                // Antenitas con esferas
                cuernosSVG = `<rect x="25" y="10" width="6" height="25" rx="3" fill="${colorCuernos}" stroke="#111" stroke-width="2"/>
                              <circle cx="28" cy="8" r="7" fill="#fff" stroke="#111" stroke-width="2"/>
                              <rect x="69" y="10" width="6" height="25" rx="3" fill="${colorCuernos}" stroke="#111" stroke-width="2"/>
                              <circle cx="72" cy="8" r="7" fill="#fff" stroke="#111" stroke-width="2"/>`;
            }

            // Generar picos/pelos en el borde de la silueta del cuerpo
            let pelosSilueta = '';
            for(let a=0; a<360; a+=15) {
                let rad = a * Math.PI / 180;
                let x1 = 50 + Math.cos(rad) * 34;
                let y1 = 58 + Math.sin(rad) * 32;
                let x2 = 50 + Math.cos(rad) * 42;
                let y2 = 58 + Math.sin(rad) * 39;
                pelosSilueta += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${colorCuerpo}" stroke-width="5" stroke-linecap="round"/>`;
            }

            // Ojos
            let ojosSVG = '';
            if (tipoOjos === 1) {
                ojosSVG = `<circle cx="50" cy="48" r="15" fill="white" stroke="#111" stroke-width="3"/>
                           <circle cx="50" cy="48" r="6" fill="black"/>
                           <circle cx="47" cy="45" r="2" fill="white"/>`;
            } else {
                ojosSVG = `<circle cx="36" cy="48" r="11" fill="white" stroke="#111" stroke-width="2.5"/>
                           <circle cx="36" cy="48" r="4.5" fill="black"/>
                           <circle cx="64" cy="48" r="11" fill="white" stroke="#111" stroke-width="2.5"/>
                           <circle cx="64" cy="48" r="4.5" fill="black"/>`;
            }

            const svgCompleto = `
                <svg viewBox="0 0 100 100" style="width:100%; height:100%;">
                    ${cuernosSVG}
                    ${pelosSilueta}
                    <ellipse cx="50" cy="58" rx="34" ry="31" fill="${colorCuerpo}" stroke="#111" stroke-width="3"/>
                    <path d="M 35 55 L 40 60 M 60 55 L 55 60 M 45 70 L 50 75" stroke="rgba(255,255,255,0.4)" stroke-width="3" stroke-linecap="round"/>
                    ${ojosSVG}
                    <path d="M 36 70 Q 50 82 64 70" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round"/>
                    <path d="M 42 71 L 44 76 L 46 71 Z M 54 71 L 56 76 L 58 71 Z" fill="white"/>
                </svg>
            `;
            document.getElementById(idContenedor).innerHTML = svgCompleto;
        }

        // --- CONFETI ---
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

        // --- SONIDOS ---
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

        // --- JUEGO ---
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
                generarMonsterSVG(`avatar-${i}`); // ¡Mutación de monstruos en cada ronda!
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

st.components.v1.html(juego_html, height=560, scrolling=False)
