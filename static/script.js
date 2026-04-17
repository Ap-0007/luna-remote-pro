// Dynamic Socket Initialization
let currentTarget = window.location.origin;
if (currentTarget.includes('vercel.app') || currentTarget.includes('github.io')) {
    currentTarget = localStorage.getItem('last_ip') || prompt("Enter Mac IP (e.g. http://192.168.1.10:5001)");
}
const socket = io(currentTarget);

function showConnectionModal() { document.getElementById('conn-modal').classList.add('active'); }
function hideConnectionModal() { document.getElementById('conn-modal').classList.remove('active'); }
function connectToMac() {
    const ip = document.getElementById('manual-ip').value;
    if (ip) {
        localStorage.setItem('last_ip', ip);
        window.location.reload();
    }
}

const trackpad = document.getElementById('trackpad');
const status = document.getElementById('connection-status');
const kbInput = document.getElementById('kb-input');

// Trackpad & Input State
let lastX = 0, lastY = 0;
const SCROLL_SENSITIVITY = 1.0;
let isMoving = false, isScrolling = false;
let lastScrollY = 0;

// Pro Features State
let isDragActive = false;
let lastTapTime = 0;
let longPressTimer = null;

// v4.3 Premium Hub Logic
const planToggle = document.getElementById('plan-toggle');
const proPriceText = document.getElementById('pro-price');
const sparklesContainer = document.getElementById('sparkles-container');

if (planToggle && proPriceText) {
    planToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            proPriceText.innerHTML = '$39.99<span class="period">/yr</span>';
            triggerHaptic('heavy');
        } else {
            proPriceText.innerHTML = '$4.99<span class="period">/mo</span>';
            triggerHaptic('medium');
        }
    });
}

// Sparkle Generator for Premium Tab
const generateSparkles = () => {
    if (!sparklesContainer) return;
    const sparkle = document.createElement('div');
    sparkle.className = 'sparkle';
    sparkle.style.left = Math.random() * 100 + '%';
    sparkle.style.top = Math.random() * 100 + '%';
    sparkle.style.width = Math.random() * 4 + 'px';
    sparkle.style.height = sparkle.style.width;
    sparkle.style.animationDuration = Math.random() * 2 + 2 + 's';
    sparklesContainer.appendChild(sparkle);
    setTimeout(() => sparkle.remove(), 4000);
};

setInterval(() => {
    if (document.getElementById('premium-view')?.classList.contains('active')) {
        generateSparkles();
    }
}, 300);

// Mechanical Haptics Helper
const triggerHaptic = (type = 'light') => {
    if (!window.navigator.vibrate) return;
    if (type === 'light') window.navigator.vibrate(15);
    else if (type === 'medium') window.navigator.vibrate(40);
    else if (type === 'heavy') window.navigator.vibrate([100, 50, 100]);
};

// 5-Tab Navigation Logic
document.querySelectorAll('.tab-link').forEach(tab => {
    tab.addEventListener('click', () => {
        const target = tab.dataset.tab;
        document.querySelectorAll('.tab-link').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(target).classList.add('active');
        triggerHaptic('light');
    });
});

// Panic Slider Logic v4.3
const panicSlider = document.getElementById('panic-slider');
const panicHandle = document.getElementById('panic-handle');
let isSliding = false;
let startX = 0;
let threshold = 0;

if (panicSlider && panicHandle) {
    panicHandle.addEventListener('touchstart', (e) => {
        isSliding = true;
        startX = e.touches[0].clientX;
        threshold = panicSlider.offsetWidth - panicHandle.offsetWidth - 10;
        panicHandle.style.transition = 'none';
        triggerHaptic('medium');
    });

    window.addEventListener('touchmove', (e) => {
        if (!isSliding) return;
        let deltaX = e.touches[0].clientX - startX;
        deltaX = Math.max(0, Math.min(deltaX, threshold));
        panicHandle.style.transform = `translateX(${deltaX}px)`;
        if (deltaX >= threshold) {
            isSliding = false;
            triggerPanic();
            resetSlider();
        }
    });

    window.addEventListener('touchend', () => {
        if (!isSliding) return;
        isSliding = false;
        resetSlider();
    });

    const resetSlider = () => {
        panicHandle.style.transition = 'transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        panicHandle.style.transform = 'translateX(0px)';
    };

    const triggerPanic = () => {
        socket.emit('panic');
        triggerHaptic('heavy');
        document.body.style.backgroundColor = '#7c002a';
        setTimeout(() => document.body.style.backgroundColor = '', 500);
    };
}

// Pro Controls
document.getElementById('pro-drag')?.addEventListener('click', () => {
    isDragActive = !isDragActive;
    document.getElementById('pro-drag').classList.toggle('active', isDragActive);
    socket.emit(isDragActive ? 'mouse_press' : 'mouse_release', { button: 'left' });
    triggerHaptic('medium');
});

document.getElementById('pro-rclick')?.addEventListener('click', () => {
    socket.emit('mouse_click', { button: 'right' });
    triggerHaptic('medium');
});

// Trackpad Interaction Logic
trackpad.addEventListener('touchstart', (e) => {
    const now = Date.now();
    if (e.touches.length === 1) {
        if (now - lastTapTime < 300) {
            socket.emit('mouse_click', { button: 'left', count: 2 });
            lastTapTime = 0;
        } else { lastTapTime = now; }
        longPressTimer = setTimeout(() => {
            socket.emit('mouse_click', { button: 'right' });
            triggerHaptic('medium');
        }, 600);
    }
    if (e.touches.length === 1) {
        const touch = e.touches[0];
        lastX = touch.clientX; lastY = touch.clientY;
        isMoving = true; isScrolling = false;
    } else if (e.touches.length === 2) {
        const touch1 = e.touches[0], touch2 = e.touches[1];
        lastScrollY = (touch1.clientY + touch2.clientY) / 2;
        isScrolling = true; isMoving = false;
        clearTimeout(longPressTimer);
    }
});

trackpad.addEventListener('touchmove', (e) => {
    clearTimeout(longPressTimer);
    if (e.touches.length === 1 && isMoving) {
        const touch = e.touches[0];
        const dx = touch.clientX - lastX, dy = touch.clientY - lastY;
        socket.emit('mouse_move', { dx, dy });
        lastX = touch.clientX; lastY = touch.clientY;
    } else if (e.touches.length === 2 && isScrolling) {
        const touch1 = e.touches[0], touch2 = e.touches[1];
        const currentY = (touch1.clientY + touch2.clientY) / 2;
        const dy = (lastScrollY - currentY) * SCROLL_SENSITIVITY;
        if (Math.abs(dy) > 1) {
            socket.emit('mouse_scroll', { dy: Math.round(dy) });
            lastScrollY = currentY;
        }
    }
    e.preventDefault();
}, { passive: false });

trackpad.addEventListener('touchend', () => {
    isMoving = false; isScrolling = false;
    clearTimeout(longPressTimer);
});

trackpad.addEventListener('click', () => {
    socket.emit('mouse_click', { button: 'left' });
});

// Socket Bindings
const bindVibrant = (id, eventName, data) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('click', () => {
        socket.emit(eventName, data);
        triggerHaptic('light');
    });
};

bindVibrant('ai-siri', 'ai_command', { command: 'siri' });
bindVibrant('ai-chatgpt', 'ai_command', { command: 'chatgpt' });
bindVibrant('ai-gemini', 'ai_command', { command: 'gemini' });
bindVibrant('ai-claude', 'ai_command', { command: 'claude' });
bindVibrant('ai-ask', 'ai_command', { command: 'ask_ai' });

document.querySelectorAll('.app-card').forEach(card => {
    card.addEventListener('click', () => {
        if (card.classList.contains('pro-locked')) {
            alert("This is an Ultra feature. Upgrade now at the Premium tab!");
            triggerHaptic('medium');
            return;
        }
        socket.emit('launch_app', { app: card.dataset.app });
        triggerHaptic('medium');
    });
});

bindVibrant('vol-up', 'volume', { action: 'up' });
bindVibrant('vol-down', 'volume', { action: 'down' });
bindVibrant('vol-mute', 'volume', { action: 'mute' });
bindVibrant('media-play', 'media', { action: 'playpause' });
bindVibrant('media-prev', 'media', { action: 'prev' });
bindVibrant('media-next', 'media', { action: 'next' });
bindVibrant('bright-up', 'brightness', { action: 'up' });
bindVibrant('bright-down', 'brightness', { action: 'down' });
bindVibrant('sys-lock', 'system', { action: 'lock' });
bindVibrant('sys-sleep', 'system', { action: 'sleep' });
bindVibrant('key-spotlight', 'key_combo', { combo: 'spotlight' });
bindVibrant('key-tab', 'key_combo', { combo: 'tab' });

kbInput.addEventListener('input', (e) => { if (e.data) socket.emit('keyboard', { text: e.data }); });
kbInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') { socket.emit('keyboard', { text: 'ENTER' }); kbInput.value = ''; kbInput.blur(); } });
document.getElementById('kb-backspace')?.addEventListener('click', () => { socket.emit('keyboard', { text: 'BACKSPACE' }); triggerHaptic('light'); });

// Ultra CTA Animation
document.getElementById('unlock-btn')?.addEventListener('click', () => {
    triggerHaptic('heavy');
    alert("Subscription API coming soon! For now, enjoy the Ultra Preview.");
});
