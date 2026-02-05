const chatEl = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('message');
const ops = document.getElementById('ops');

function appendMessage(role, text) {
    const el = document.createElement('div');
    el.className = 'message ' + role;
    el.innerHTML = `<strong>${role === 'user' ? 'You' : 'Bot'}:</strong> <span>${text}</span>`;
    chatEl.appendChild(el);
    chatEl.scrollTop = chatEl.scrollHeight;
}

async function sendMessage(message) {
    appendMessage('user', message);
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await res.json();
        appendMessage('bot', data.response || '[no response]');
    } catch (err) {
        appendMessage('bot', 'Error: ' + err.message);
    }
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';
    sendMessage(msg);
});

ops.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    const msg = btn.getAttribute('data-msg');
    if (msg) sendMessage(msg);
});

// welcome
appendMessage('bot', 'Hello! I can manage student records. Use the buttons or type commands (create/update/delete/list).');