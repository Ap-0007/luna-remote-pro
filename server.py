import os
import socket
import subprocess
from flask import Flask, render_template, request
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

# Sensitivity for mouse movement
SENSITIVITY = 1.8

def run_osascript(script):
    try:
        subprocess.run(["osascript", "-e", script], check=True)
    except Exception as e:
        print(f"OSAScript Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('mouse_move')
def handle_mouse_move(data):
    if not HAS_PYNPUT: return
    dx = data.get('dx', 0) * SENSITIVITY
    dy = data.get('dy', 0) * SENSITIVITY
    mouse.move(dx, dy)

@socketio.on('mouse_click')
def handle_mouse_click(data):
    if not HAS_PYNPUT: return
    btn = data.get('button', 'left')
    count = data.get('count', 1)
    click_btn = Button.left if btn == 'left' else Button.right
    mouse.click(click_btn, count)

@socketio.on('mouse_press')
def handle_mouse_press(data):
    if not HAS_PYNPUT: return
    btn = data.get('button', 'left')
    press_btn = Button.left if btn == 'left' else Button.right
    mouse.press(press_btn)

@socketio.on('mouse_release')
def handle_mouse_release(data):
    if not HAS_PYNPUT: return
    btn = data.get('button', 'left')
    release_btn = Button.left if btn == 'left' else Button.right
    mouse.release(release_btn)

@socketio.on('volume')
def handle_volume(data):
    action = data.get('action')
    if action == 'up':
        run_osascript('set volume output volume ((output volume of (get volume settings)) + 6)')
    elif action == 'down':
        run_osascript('set volume output volume ((output volume of (get volume settings)) - 6)')
    elif action == 'mute':
        run_osascript('set volume output muted (not (output muted of (get volume settings)))')

@socketio.on('media')
def handle_media(data):
    action = data.get('action')
    if action == 'playpause':
        run_osascript('tell application "System Events" to key code 49') # Space
    elif action == 'next':
        run_osascript('tell application "System Events" to key code 124') # Right arrow
    elif action == 'prev':
        run_osascript('tell application "System Events" to key code 123') # Left arrow

@socketio.on('system')
def handle_system(data):
    action = data.get('action')
    if action == 'sleep':
        run_osascript('tell application "System Events" to sleep')
    elif action == 'lock':
        run_osascript('tell application "System Events" to keystroke "q" using {control down, command down}')

@socketio.on('keyboard')
def handle_keyboard(data):
    if not HAS_PYNPUT: return
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
    if not HAS_PYNPUT: return
    dy = data.get('dy', 0)
    mouse.scroll(0, dy)

@socketio.on('launch_app')
def handle_launch_app(data):
    app_name = data.get('app')
    if app_name:
        subprocess.run(["open", "-a", app_name])

@socketio.on('brightness')
def handle_brightness(data):
    action = data.get('action')
    if action == 'up':
        run_osascript('tell application "System Events" to key code 144')
    elif action == 'down':
        run_osascript('tell application "System Events" to key code 145')

@socketio.on('key_combo')
def handle_key_combo(data):
    combo = data.get('combo')
    if combo == 'spotlight':
        run_osascript('tell application "System Events" to keystroke space using {command down}')
    elif combo == 'tab':
        run_osascript('tell application "System Events" to key code 48 using {command down}')

@socketio.on('ai_command')
def handle_ai_command(data):
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

if __name__ == '__main__':
    ip_addr = get_local_ip()
    port = 5001
    url = f"http://{ip_addr}:{port}"
    
    print("\n" + "="*50)
    print(" LUNAREMOTE SERVER STARTING ")
    print("="*50)
    print(f"\nConnect your phone to: {url}")
    
    if HAS_QRCODE:
        qr = qrcode.QRCode()
        qr.add_data(url)
        qr.print_ascii(invert=True)
    
    # Pre-checks for macOS
    print("\nIMPORTANT: Grant Accessibility permissions to Terminal/Python if mouse control fails.")
    print("="*50 + "\n")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
