# LunaRemote Pro 🌙✨

> **Control your laptop from your phone with a premium, AI-powered remote interface.**

LunaRemote is a high-end web-based remote control system for macOS. It transforms your mobile browser into a professional precision trackpad, media controller, and AI dashboard.

![LunaRemote UI Concept](https://raw.githubusercontent.com/Ap-0007/LunaRemote/main/static/preview.png) *(Placeholder for after you upload)*

## 🌟 Key Features

### 🖱️ Pro Precision Trackpad
- **Smooth Cursor Movement**: Low-latency mouse tracking.
- **Advanced Gestures**: Double-tap to click, Long-press for Right-Click.
- **Two-Finger Scroll**: Natural scrolling through pages.
- **Drag Mode**: Dedicated toggle to "Grab & Drop" windows or files.

### 🧠 AI Force Hub
- **Universal Siri**: Invoke Siri with a single tap.
- **ChatGPT Desktop**: Deep integration with the ChatGPT Mac app.
- **Gemini & Claude**: Instant access to your favorite AI models.
- **Ask AI Button**: Trigger global shortcuts to start chatting immediately.

### 🍱 Productivity Suite
- **App Launcher**: Quick-launch Chrome, Spotify, Finder, Music, and more.
- **Media Center**: Volume, Play/Pause, and track skipping.
- **System Controls**: Remote Sleep, Lock Screen, and Brightness adjustment.
- **Remote Keyboard**: Type on your laptop using your mobile device.

## 🚀 Quick Start (macOS)

### 1. Requirements
- Python 3.9+
- A mobile phone on the same Wi-Fi network.

### 2. Installation
```bash
git clone https://github.com/Ap-0007/LunaRemote.git
cd LunaRemote
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python server.py
```
Scan the **QR Code** printed in your terminal to connect instantly!

## 🛠️ Essential Setup (Privacy)
To allow LunaRemote to control your inputs, you must grant permissions to your terminal:
1. **System Settings > Privacy & Security > Accessibility** -> Enable `Terminal`.
2. **System Settings > Privacy & Security > Screen Recording** -> Enable `Terminal`.

## 🎨 Tech Stack
- **Backend**: Python, Flask, Socket.IO, Pynput.
- **Frontend**: Modern Vanilla HTML/CSS/JS (Glassmorphic Design).
- **Communication**: Real-time WebSockets.

---
Built with ❤️ by **Ap-0007**
