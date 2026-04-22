import threading, keyboard, socket, time, mouse
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

spike_state = {"status": "idle", "id": 0}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spike Timer Ultime</title>
    <style>
        body { 
            background: #0f1923; color: white; display: flex; flex-direction: column; 
            justify-content: center; align-items: center; height: 100vh; 
            font-family: 'Segoe UI', sans-serif; margin: 0; overflow: hidden; 
            transition: background 0.2s; user-select: none; cursor: pointer;
        }
        #timer { font-size: 35vw; font-weight: 900; }
        #status { font-size: 5vw; text-transform: uppercase; letter-spacing: 5px; }
        
        .normal { background: #0f1923; }
        .planted { background: #1a2e35; }
        .critical { background: #ff4655 !important; }
        .danger { animation: pulse 0.2s infinite; background: #ff4655 !important; }
        
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body class="normal">
    <div id="status">PRÊT (Touche O ou Clic)</div>
    <div id="timer">45.0</div>

    <script>
        let currentId = 0;
        let count = 45;
        let interval;

        async function checkSpike() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                if (data.status === "running" && data.id !== currentId) {
                    currentId = data.id;
                    startChrono();
                } 
                else if (data.status === "idle" && currentId !== 0) {
                    currentId = 0;
                    resetDisplay();
                }
            } catch (e) {}
        }

        function startChrono() {
            clearInterval(interval);
            count = 45;
            document.body.className = 'planted';
            document.getElementById('status').innerText = "SPIKE PLANTÉ";
            
            interval = setInterval(() => {
                count -= 0.1;
                if (count <= 0) {
                    explode();
                } else {
                    document.getElementById('timer').innerText = count.toFixed(1);
                    if (count <= 7 && count > 2) {
                        document.body.className = 'critical';
                        document.getElementById('status').innerText = "TROP TARD SANS KIT";
                    } else if (count <= 2) {
                        document.body.className = 'danger';
                        document.getElementById('status').innerText = "COURS !!!";
                    }
                }
            }, 100);
        }

        function explode() {
            clearInterval(interval);
            document.getElementById('timer').innerText = "💥";
            document.getElementById('status').innerText = "BOOM";
            document.body.className = 'normal'; 
            
            setTimeout(() => {
                if (currentId !== 0) fetch('/reset', { method: 'POST' });
            }, 3000);
        }

        function resetDisplay() {
            clearInterval(interval);
            count = 45;
            document.getElementById('timer').innerText = "45.0";
            document.getElementById('status').innerText = "PRÊT (Touche O ou Clic)";
            document.body.className = 'normal';
        }

        // LE CLIC SUR L'ÉCRAN : Lancer ou Arrêter
        document.body.addEventListener('click', () => {
            if (currentId !== 0) { 
                fetch('/reset', { method: 'POST' }); // Si en cours -> Arrête
            } else {
                fetch('/start', { method: 'POST' }); // Si arrêté -> Lance
            }
        });

        setInterval(checkSpike, 300);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/status')
def get_status():
    return jsonify(spike_state)

# Nouveau : Le téléphone dit au PC de lancer le chrono
@app.route('/start', methods=['POST'])
def start_state():
    spike_state["status"] = "running"
    spike_state["id"] = time.time()
    print("<<< CHRONO LANCÉ DEPUIS LE TÉLÉPHONE !")
    return jsonify(success=True)

@app.route('/reset', methods=['POST'])
def reset_state():
    spike_state["status"] = "idle"
    spike_state["id"] = 0
    print("<<< CHRONO ANNULÉ / RESET !")
    return jsonify(success=True)

def on_key_press(event):
    spike_state["status"] = "running"
    spike_state["id"] = time.time()
    print(">>> TOUCHE 'O' PRESSÉE !")

def listen_kb():
    keyboard.on_press_key('o', on_key_press)
    keyboard.wait()

def on_mouse_click():
    if spike_state["status"] != "running":
        spike_state["status"] = "running"
        spike_state["id"] = time.time()
     w   print(">>> TOUCHE SOURIS PRESSÉE !")

def listen_mouse():
    # mouse.on_button(callback=on_mouse_click, buttons=("x"), types=("down"))
    mouse.on_button(callback=on_mouse_click, buttons=("x2"), types=("down"))


if __name__ == '__main__':
    local_ip = socket.gethostbyname(socket.gethostname())
    print(f"\n--- SYSTÈME OPÉRATIONNEL ---")
    print(f"URL : http://{local_ip}:5000")
    print(f"- Lancer : Touche 'O' en jeu OU Clic sur le téléphone.")
    print(f"- Annuler : Clic sur le téléphone.")
    # threading.Thread(target=listen_kb, daemon=True).start()
    threading.Thread(target=listen_mouse, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, threaded=True)