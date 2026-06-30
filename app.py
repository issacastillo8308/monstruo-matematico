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

# --- MOTOR DE JUEGO SUPREMO CON PORTADA DE LUJO Y MARCADOR DESGLOSADO ---
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
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            font-size: 13px;
            color: #fffb00;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .operacion-titulo {
            font-size: 44px;
            color: #00ffcc;
            margin: 8px 0 0 0;
            font-weight: 900;
            text-shadow: 0 0 12px #00ffcc;
        }

        .vidas-container {
            font-size: 15px;
            color: #ff3333;
            font-weight: bold;
            letter-spacing: 2px;
        }
        .x-activa {
            animation: blinkX 0.3s ease-in-out;
        }
        @keyframes blinkX {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.3); filter: drop-shadow(0 0 8px red); }
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
        .fb-icon { width: 20px; height: 20px; fill: white; margin-right: 10px; }
        .text-neon-fb { color: #00ffcc; margin-left: 5px; animation: pulse 1.2s infinite; }
        @keyframes pulse {
            0%, 100% { opacity: 0.7; text-shadow: 0 0 2px #00ffcc; }
            50% { opacity: 1; text-shadow: 0 0 8px #00ffcc; }
        }

        /* --- PANTALLAS MODALES --- */
        .pantalla-modal {
            display: flex;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(9, 7, 15, 0.99);
            z-index: 100;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
            box-sizing: border-box;
        }

        /* Estilos de la Portada Bonita */
        .caja-portada {
            border: 4px dashed #00ffcc;
            padding: 30px 20px;
            border-radius: 30px;
            background: rgba(20, 15, 45, 0.6);
            box-shadow: 0 0 25px rgba(0,255,204,0.3);
            max-width: 340px;
            position: relative;
        }
        .decoracion-monstruos {
            display: flex;
            justify-content: space-around;
            width: 100%;
            margin-bottom: 15px;
        }
        .mini-monster {
            width: 65px;
            height: 65px;
            animation: bounce 1.2s infinite ease-in-out;
        }

        /* Tarjeta de Resultados Finales */
        .tabla-resultados {
            background: #140f2d;
            border: 2px solid #ff007f;
            border-radius: 18px;
            padding: 15px 25px;
            margin: 15px 0 25px 0;
            min-width: 260px;
            box-shadow: 0 0 15px rgba(255,0,127,0.2);
        }
        .fila-res {
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            margin: 8px 0;
            border-bottom: 1px dashed rgba(255,255,255,0.1);
            padding-bottom: 4px;
        }

        .btn-grande-arcade {
            background: linear-gradient(180deg, #00ffcc 0%, #00b38f 100%);
            color: black;
            border: 3px solid white;
            padding: 16px 38px;
            font-size: 22px;
            font-weight: bold;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 0 25px #00ffcc;
            letter-spacing: 1px;
            text-transform: uppercase;
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

    <div id="pantalla-inicio" class="pantalla-modal">
        <div class="caja-portada">
            <div class="decoracion-monstruos">
                <svg class="mini-monster" viewBox="0 0 100 100" style="animation-delay:0s;">
                    <path d="M 30 36 Q 14 10 26 6 Z" fill="#ff007f" stroke="#111" stroke-width="2"/>
                    <ellipse cx="50" cy="55" rx="35" ry="32" fill="#ff007f" stroke="#111" stroke-width="3"/>
                    <circle cx="50" cy="45" r="10" fill="white" stroke="#111" stroke-width="2"/>
                    <circle cx="50" cy="45" r="4" fill="black"/>
                </svg>
                <svg class="mini-monster" viewBox="0 0 100 100" style="animation-delay:0.4s;">
                    <path d="M 70 36 Q 86 10 74 6 Z" fill="#2ecc71" stroke="#111" stroke-width="2"/>
                    <ellipse cx="50" cy="55" rx="35" ry="32" fill="#2ecc71" stroke="#111" stroke-width="3"/>
                    <circle cx="38" cy="45" r="8" fill="white" stroke="#111" stroke-width="2"/>
                    <circle cx="38" cy="45" r="3" fill="black"/>
                    <circle cx="62" cy="45" r="8" fill="white" stroke="#111" stroke-width="2"/>
                    <circle cx="62" cy="45" r="3" fill="black"/>
                </svg>
            </div>
            
            <h1 style="color: #00ffcc; font-size: 36px; margin: 0 0 5px 0; text-shadow: 0 0 15px #00ffcc; font-weight:900;">RETO<br>MONSTRUO</h1>
            <p style="font-size: 13px; color: #fffb00; margin: 0 0 25px 0; letter-spacing:1.5px; text-transform:uppercase;">Arcade Matemático</p>
            <button class="btn-grande-arcade" onclick="comenzarRondaReal()">🎮 JUGAR NOW</button>
        </div>
    </div>

    <div id="pantalla-fin" class="pantalla-modal" style="display: none;">
        <h1 id="txt-fin-titulo" style="color: #ff007f; font-size: 40px; margin: 0; text-shadow: 0 0 15px #ff007f;">❌ GAME OVER</h1>
        
        <div class="tabla-resultados">
            <div class="fila-res">
                <span style="color:#7f7f99;">⭐ NIVEL:</span>
                <span id="final-nivel" style="color:#00ffcc; font-weight:bold;">1</span>
            </div>
            <div class="fila-res">
                <span style="color:#2ecc71;">🍪 ACIERTOS:</span>
                <span id="final-aciertos" style="color:#2ecc71; font-weight:bold;">0</span>
            </div>
            <div class="fila-res" style="border-none:none;">
                <span style="color:#ff3333;">❌ ERRORES:</span>
                <span id="final-errores" style="color:#ff3333; font-weight:bold;">0</span>
            </div>
        </div>

        <button class="btn-grande-arcade" style="background: linear-gradient(180deg, #ff007f 0%, #b30059 100%); color: white; box-shadow: 0 0 25px #ff007f;" onclick="reiniciarJuego()">🔄 VOLVER A INTENTAR</button>
    </div>

    <div class="game-wrapper">
        <div class="tablero-neon">
            <div class="stats-bar">
                <div>⏱️ Reloj: <b id="timer" style="color:#ff007f; font-size:16px;">20</b>s</div>
                <div style="color: #00ffcc;">⭐ Nivel: <b id="txt-nivel" style="color:white; font-size:16px;">1</b></div>
            </div>
            <div class="stats-bar" style="border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 5px; margin-top: 5px;">
                <div>🍪 Galletas: <b id="puntos" style="color:white;">0</b></div>
                <div class="vidas-container">❌ <span id="error-slots">_ _ _</span></div>
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
        let puntos = 0, nivel = 1, tiempo = 20, errores = 0; 
        let puntosEnNivelActual = 0; 
        let respuestaCorrecta = 0, opciones = [], juegoActivo = false, cronometro;
        let contadorErroresTotales = 0; // Registro global para la ventana final
        
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

        function lanzarConfeti(cantidad) {
            for (let i = 0; i < cantidad; i++) {
                particles.push({
                    x: window.innerWidth / 2, y: window.innerHeight / 2,
                    angle: Math.random() * Math.PI * 2, speed: Math.random() * 8 + 4,
                    color: `hsl(${Math.random() * 360}, 100%, 60%)`, r: Math.random() * 4 + 3, d: cantidad > 50 ? 55 : 25
                });
            }
        }
        function drawParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach((p, idx) => {
                p.x += Math.cos(p.angle) * p.speed; p.y += Math.sin(p.angle) * p.speed + 1.2; p.d--;
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
                gain.gain.setValueAtTime(0.12, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.15);
            } else if (tipo === 'incorrecto') {
                osc.type = 'sawtooth'; osc.frequency.setValueAtTime(150, audioCtx.currentTime);
                osc.frequency.linearRampToValueAtTime(50, audioCtx.currentTime + 0.15);
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.15);
            } else if (tipo === 'victoria') {
                osc.type = 'square';
                let notas = [523.25, 659.25, 783.99, 1046.50]; 
                notas.forEach((f, i) => { osc.frequency.setValueAtTime(f, audioCtx.currentTime + (i * 0.08)); });
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.4);
            } else if (tipo === 'fin') {
                osc.type = 'square'; osc.frequency.setValueAtTime(220, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.4);
            }
        }

        function generarReto() {
            let n1 = 0, n2 = 0, op = '+';
            if (nivel === 1) { n1 = Math.floor(Math.random() * 4) + 1; n2 = Math.floor(Math.random() * 4) + 1; op = '+'; }
            else if (nivel === 2) { n1 = Math.floor(Math.random() * 7) + 1; n2 = Math.floor(Math.random() * 5) + 1; op = '+'; }
            else if (nivel === 3) { n1 = Math.floor(Math.random() * 10) + 1; n2 = Math.floor(Math.random() * 8) + 1; op = '+'; }
            else if (nivel === 4) { n1 = Math.floor(Math.random() * 10) + 1; n2 = Math.floor(Math.random() * 5) + 1; op = '-'; } 
            else if (nivel === 5) { n1 = Math.floor(Math.random() * 15) + 5; n2 = Math.floor(Math.random() * 10) + 1; op = Math.random() > 0.5 ? '+' : '-'; }
            else if (nivel === 6) { n1 = Math.floor(Math.random() * 20) + 5; n2 = Math.floor(Math.random() * 15) + 5; op = '+'; }
            else if (nivel === 7) { n1 = Math.floor(Math.random() * 25) + 10; n2 = Math.floor(Math.random() * 15) + 5; op = '-'; }
            else if (nivel === 8) { n1 = Math.floor(Math.random() * 35) + 10; n2 = Math.floor(Math.random() * 20) + 5; op = Math.random() > 0.5 ? '+' : '-'; }
            else if (nivel === 9) { n1 = Math.floor(Math.random() * 50) + 15; n2 = Math.floor(Math.random() * 30) + 10; op = Math.random() > 0.5 ? '+' : '-'; }
            else { n1 = Math.floor(Math.random() * 80) + 20; n2 = Math.floor(Math.random() * 50) + 15; op = Math.random() > 0.5 ? '+' : '-'; } 

            if (op === '-' && n1 < n2) { let t = n1; n1 = n2; n2 = t; }
            respuestaCorrecta = op === '+' ? n1 + n2 : n1 - n2;
            document.getElementById('operacion-texto').innerText = `RETO: ${n1} ${op} ${n2}`;

            let falsos = new Set();
            let rangoFalsos = nivel * 8 + 15; 
            while(falsos.size < 3) {
                let f = Math.floor(Math.random() * rangoFalsos);
                if (f !== respuestaCorrecta && f >= 0) falsos.add(f);
            }
            opciones = Array.from(falsos); opciones.push(respuestaCorrecta);
            opciones.sort(() => Math.random() - 0.5);

            for(let i=0; i<4; i++) { 
                document.getElementById(`opt-${i}`).innerText = opciones[i]; 
                generarMonsterSVG(`avatar-${i}`); 
            }
        }

        function iniciarCronometro() {
            cronometro = setInterval(() => {
                if (!juegoActivo) return;
                tiempo--;
                document.getElementById('timer').innerText = tiempo;
                if (tiempo <= 0) finalizarRonda("tiempo");
            }, 1000);
        }

        function comenzarRondaReal() {
            document.getElementById('pantalla-inicio').style.display = 'none';
            juegoActivo = true;
            tiempo = 20;
            generarReto();
            iniciarCronometro();
        }

        function actualizarVidasVisuales() {
            let str = "";
            for(let i=1; i<=3; i++) {
                if(i <= errores) str += "<span class='x-activa'>X</span> ";
                else str += "_ ";
            }
            document.getElementById('error-slots').innerHTML = str.trim();
        }

        function tocarMonstruo(indice) {
            if (!juegoActivo) return;
            let tarjeta = document.getElementsByClassName('tarjeta-arcade')[indice];
            
            if (opciones[indice] === respuestaCorrecta) {
                puntos++; 
                puntosEnNivelActual++;
                document.getElementById('puntos').innerText = puntos;
                
                if (puntosEnNivelActual >= 3) {
                    if (nivel < 10) {
                        nivel++;
                        puntosEnNivelActual = 0;
                        tiempo = 20; 
                        document.getElementById('txt-nivel').innerText = nivel;
                        document.getElementById('timer').innerText = tiempo;
                        sonar('victoria'); 
                        lanzarConfeti(120); 
                    }
                } else {
                    sonar('correcto'); lanzarConfeti(30);
                }

                tarjeta.classList.add('correcto-impacto');
                setTimeout(() => { tarjeta.classList.remove('correcto-impacto'); generarReto(); }, 120);
            } else {
                errores++;
                contadorErroresTotales++; // Registra para el desglose final
                actualizarVidasVisuales();
                sonar('incorrecto'); 
                tarjeta.classList.add('incorrecto-impacto');
                
                if (errores >= 3) {
                    setTimeout(() => { tarjeta.classList.remove('incorrecto-impacto'); finalizarRonda("errores"); }, 200);
                } else {
                    setTimeout(() => tarjeta.classList.remove('incorrecto-impacto'), 180);
                }
            }
        }

        function finalizarRonda(motivo) {
            juegoActivo = false;
            clearInterval(cronometro);
            sonar('fin');
            
            if(motivo === "errores") {
                document.getElementById('txt-fin-titulo').innerText = "❌ ¡GAME OVER!";
                document.getElementById('txt-fin-titulo').style.color = "#ff3333";
            } else {
                document.getElementById('txt-fin-titulo').innerText = "⏱️ ¡TIEMPO!";
                document.getElementById('txt-fin-titulo').style.color = "#ff007f";
            }

            // CAMBIO CLAVE: Desglose completo de resultados en la ventana
            document.getElementById('final-aciertos').innerText = puntos;
            document.getElementById('final-errores').innerText = contadorErroresTotales;
            document.getElementById('final-nivel').innerText = nivel;
            document.getElementById('pantalla-fin').style.display = 'flex';
        }

        function reiniciarJuego() {
            puntos = 0; nivel = 1; tiempo = 20; puntosEnNivelActual = 0; errores = 0; contadorErroresTotales = 0; juegoActivo = true;
            document.getElementById('puntos').innerText = puntos;
            document.getElementById('timer').innerText = tiempo;
            document.getElementById('txt-nivel').innerText = nivel;
            actualizarVidasVisuales();
            document.getElementById('pantalla-fin').style.display = 'none';
            generarReto();
            clearInterval(cronometro);
            iniciarCronometro();
        }

        generarReto();
    </script>
</body>
</html>
"""

st.components.v1.html(juego_html, height=640, scrolling=False)
