# 🌙 LunaRemote Pro v3.0

> Control your laptop with the power of AI from your phone.

**LunaRemote Pro** is a high-end, mobile-optimized remote control for your Mac. It transforms your phone's browser into a professional-grade touchpad, application launcher, and AI control hub.

---

## 🚀 Features

- **🦾 Pro Touchpad Gestures**:
  - Precision relative movement.
  - **Double-Tap** to Double Click.
  - **Long Press** for Right Click.
  - **Drag & Drop Mode**: Toggle "Grab" to move windows/files.
  - **Two-Finger Scroll**: Natural scrolling through documents and web pages.

- **🤖 AI Force Hub**:
  - One-tap access to **ChatGPT**, **Siri**, **Gemini**, and **Claude**.
  - **"Ask AI" Button**: Triggers global shortcuts for instant prompting.

- **📂 App Launchpad**:
  - Instant launch buttons for **Chrome**, **Spotify**, **Finder**, **Music**, and **Terminal**.

- **⚙️ Complete OS Controls**:
  - Media Playback (Play/Pause, Next/Prev).
  - Volume Up/Down/Mute.
  - Screen Brightness.
  - System Sleep & Screen Lock.
  - Remote Keyboard Input.

- **✨ Premium UI**:
  - Dark Mode Glassmorphism.
  - Glowing AI Themes.
  - Responsive Tabbed Navigation.

---

## 🛠️ Setup & Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/LunaRemote.git
    cd LunaRemote
    ```

2.  **Install Dependencies**:
    ```bash
    pip install flask flask-socketio eventlet pynput qrcode pillow
    ```

3.  **Run the Server**:
    ```bash
    python server.py
    ```

4.  **Connect Your Phone**:
    Scan the **QR Code** that appears in your terminal or type the displayed IP address into your mobile browser.

---

## 🔒 Permissions (macOS)

For the gestures and app-launcher to work, you **must** grant the following permissions in **System Settings > Privacy & Security**:
1.  **Accessibility**: Grant to `Terminal.app` (or your preferred IDE).
2.  **Screen Recording**: Grant to `Terminal.app`.

---

## 📦 Tech Stack

- **Backend**: Python (Flask, Socket.IO, pynput, osascript)
- **Frontend**: HTML5, Vanilla CSS3, JavaScript (Socket.IO-client)
- **Networking**: Real-time WebSockets.

---

*Built with ❤️ and Precision Control.*
