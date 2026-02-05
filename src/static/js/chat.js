const chatEl = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('message');
const ops = document.getElementById('ops');

function appendMessage(role, text) {
    const el = document.createElement('div');
    el.className = 'message ' + role;

    function escapeHtml(s) {
        return s
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#39;');
    }

    function renderMarkdownTable(md) {
        const idx = md.indexOf('|');
        if (idx === -1) return null;
        const tablePart = md.substring(idx).trim();
        const lines = tablePart.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
        const tableLines = lines.filter(l => l.includes('|'));
        if (tableLines.length === 0) return null;
        const dataLines = tableLines.filter(l => !/^\|?\s*-{2,}/.test(l.replace(/\s+/g, '')));
        if (dataLines.length < 1) return null;
        const headerLine = dataLines[0];
        const rowLines = dataLines.slice(1);

        function splitRow(line) {
            return line.split('|').map(cell => cell.trim()).filter((c, i, arr) => !(i === 0 && c === '') && !(i === arr.length - 1 && c === ''));
        }

        const headers = splitRow(headerLine);
        let html = '<table class="students-table"><thead><tr>' + headers.map(h => `<th>${escapeHtml(h)}</th>`).join('') + '</tr></thead><tbody>';
        rowLines.forEach(r => {
            const cells = splitRow(r);
            if (cells.every(c => /^-+$/.test(c))) return;
            html += '<tr>' + cells.map(c => `<td>${escapeHtml(c)}</td>`).join('') + '</tr>';
        });
        html += '</tbody></table>';
        return html;
    }

    if (role === 'bot') {
        // if the text already contains an HTML table, render it as HTML
        if (text && text.trim().startsWith('<table') || text.includes('<table')) {
            el.innerHTML = `<strong>Bot:</strong> <div class="bot-content">${text}</div>`;
        } else {
            const tableHtml = renderMarkdownTable(text);
            if (tableHtml) {
                // attempt to find trailing text after the table block
                const lastTableIdx = text.lastIndexOf('|');
                const after = text.substring(lastTableIdx + 1).replace(/[\*\u2705\u274C\u1F4CB\u1F393\u1F382\u1F31F]/g, '').trim();
                el.innerHTML = `<strong>Bot:</strong> <div class="bot-content">${tableHtml}${after ? ('<div class="bot-follow">' + escapeHtml(after) + '</div>') : ''}</div>`;
            } else {
                el.innerHTML = `<strong>Bot:</strong> <div class="bot-content">${escapeHtml(text)}</div>`;
            }
        }
    } else {
        el.innerHTML = `<strong>You:</strong> <span>${escapeHtml(text)}</span>`;
    }

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