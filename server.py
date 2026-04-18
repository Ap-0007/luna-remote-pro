import os
import socket
import subprocess
import threading
import time
import re
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit

try:
    from pynput.mouse import Controller as MouseController, Button
    from pynput.keyboard import Controller as KeyboardController, Key
    mouse = MouseController()
    keyboard = KeyboardController()
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False
    print("Warning: pynput not found. Mouse/Keyboard control will be disabled until installed.")

try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global Access Security v5.0
AUTH_PIN = "909090"
authenticated_sessions = set()
global_url = "Initializing..."

# Sensitivity for mouse movement
SENSITIVITY = 1.8

def run_osascript(script):
    try:
        subprocess.run(["osascript", "-e", script], check=True)
    except Exception as e:
        print(f"OSAScript Error: {e}")

def check_auth():
    if request.sid not in authenticated_sessions:
        emit('auth_required')
        return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('static', 'sw.js')

@app.route('/download')
def download_project():
    return send_from_directory('.', 'LunaRemote_v3.1.zip', as_attachment=True)

# Authentication Handshake
@socketio.on('auth')
def handle_auth(data):
    pin = data.get('pin')
    if pin == AUTH_PIN:
        authenticated_sessions.add(request.sid)
        emit('auth_success')
        print(f"Client authenticated: {request.sid}")
    else:
        emit('auth_fail', {'msg': 'Invalid PIN'})

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in authenticated_sessions:
        authenticated_sessions.remove(request.sid)

# Mouse & Keyboard Events (Wrapped in check_auth)
@socketio.on('mouse_move')
def handle_mouse_move(data):
    if not check_auth() or not HAS_PYNPUT: return
    dx = data.get('dx', 0) * SENSITIVITY
    dy = data.get('dy', 0) * SENSITIVITY
    mouse.move(dx, dy)

@socketio.on('mouse_click')
def handle_mouse_click(data):
    if not check_auth() or not HAS_PYNPUT: return
    btn = data.get('button', 'left')
    count = data.get('count', 1)
    click_btn = Button.left if btn == 'left' else Button.right
    mouse.click(click_btn, count)

@socketio.on('mouse_press')
def handle_mouse_press(data):
    if not check_auth() or not HAS_PYNPUT: return
    btn = data.get('button', 'left')
    press_btn = Button.left if btn == 'left' else Button.right
    mouse.press(press_btn)

@socketio.on('mouse_release')
def handle_mouse_release(data):
    if not check_auth() or not HAS_PYNPUT: return
    btn = data.get('button', 'left')
    release_btn = Button.left if btn == 'left' else Button.right
    mouse.release(release_btn)

@socketio.on('volume')
def handle_volume(data):
    if not check_auth(): return
    action = data.get('action')
    if action == 'up':
        run_osascript('set volume output volume ((output volume of (get volume settings)) + 6)')
    elif action == 'down':
        run_osascript('set volume output volume ((output volume of (get volume settings)) - 6)')
    elif action == 'mute':
        run_osascript('set volume output muted (not (output muted of (get volume settings)))')

@socketio.on('media')
def handle_media(data):
    if not check_auth(): return
    action = data.get('action')
    if action == 'playpause':
        run_osascript('tell application "System Events" to key code 49')
    elif action == 'next':
        run_osascript('tell application "System Events" to key code 124')
    elif action == 'prev':
        run_osascript('tell application "System Events" to key code 123')

@socketio.on('system')
def handle_system(data):
    if not check_auth(): return
    action = data.get('action')
    if action == 'sleep':
        run_osascript('tell application "System Events" to sleep')
    elif action == 'lock':
        subprocess.run(["pmset", "displaysleepnow"])

@socketio.on('keyboard')
def handle_keyboard(data):
    if not check_auth() or not HAS_PYNPUT: return
    text = data.get('text', '')
    if text == 'BACKSPACE':
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
    elif text == 'ENTER':
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    else:
        keyboard.type(text)

@socketio.on('mouse_scroll')
def handle_mouse_scroll(data):
    if not check_auth() or not HAS_PYNPUT: return
    dy = data.get('dy', 0)
    mouse.scroll(0, dy)

@socketio.on('launch_app')
def handle_launch_app(data):
    if not check_auth(): return
    app_name = data.get('app')
    if app_name:
        subprocess.run(["open", "-a", app_name])

@socketio.on('brightness')
def handle_brightness(data):
    if not check_auth(): return
    action = data.get('action')
    if action == 'up':
        run_osascript('tell application "System Events" to key code 144')
    elif action == 'down':
        run_osascript('tell application "System Events" to key code 145')

@socketio.on('key_combo')
def handle_key_combo(data):
    if not check_auth(): return
    combo = data.get('combo')
    if combo == 'spotlight':
        run_osascript('tell application "System Events" to keystroke space using {command down}')
    elif combo == 'tab':
        run_osascript('tell application "System Events" to key code 48 using {command down}')

@socketio.on('ai_command')
def handle_ai_command(data):
    if not check_auth(): return
    cmd = data.get('command')
    if cmd == 'siri':
        run_osascript('tell application "Siri" to activate')
    elif cmd == 'chatgpt':
        subprocess.run(["open", "-a", "ChatGPT"])
    elif cmd == 'gemini':
        subprocess.run(["open", "https://gemini.google.com"])
    elif cmd == 'claude':
        subprocess.run(["open", "https://claude.ai"])
    elif cmd == 'ask_ai':
        subprocess.run(["open", "-a", "ChatGPT"])
        run_osascript('tell application "System Events" to key code 49 using {option down}')

@socketio.on('panic')
def handle_panic(data=None):
    if not check_auth(): return
    run_osascript('set volume output muted true')
    subprocess.run(["pmset", "displaysleepnow"])

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def start_tunnel():
    global global_url
    print("\n📡 INITIALIZING GLOBAL TUNNEL...")
    try:
        # Start SSH tunnel to Pinggy.io
        # -R 80:localhost:5001 forward local 5001 to remote 80
        tunnel_process = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:5001", "a.pinggy.io"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Parse link from output
        for line in tunnel_process.stdout:
            # Look for patterns like https://xxxx.pinggy.link or .online
            match = re.search(r'https://[a-zA-Z0-9-]+\.pinggy\.(link|online)', line)
            if match:
                global_url = match.group(0)
                print("\n" + "*"*50)
                print(f"🌍 GLOBAL ACCESS READY!")
                print(f"URL: {global_url}")
                print(f"PIN: {AUTH_PIN}")
                print("*"*50 + "\n")
                break
    except Exception as e:
        print(f"Tunnel Error: {e}")
        global_url = "ERROR: Could not establish tunnel."

if __name__ == '__main__':
    ip_addr = get_local_ip()
    port = 5001
    local_url = f"http://{ip_addr}:{port}"
    
    print("\n" + "="*50)
    print(" LUNAREMOTE PRO v5.0 (GLOBAL EDITION) ")
    print("="*50)
    print(f"\nLocal (Wi-Fi): {local_url}")
    
    # Start the global tunnel in a separate thread
    threading.Thread(target=start_tunnel, daemon=True).start()
    
    if HAS_QRCODE:
        qr = qrcode.QRCode()
        qr.add_data(local_url)
        qr.print_ascii(invert=True)
    
    print("\nSECURITY: Standard access requires PIN: 909090")
    print("="*50 + "\n")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
