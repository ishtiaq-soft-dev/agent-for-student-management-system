// students.js - handles modal forms and direct student REST operations
const opsEl = document.getElementById('ops');

function createElementFromHTML(htmlString) {
    const div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    return div.firstChild;
}

function showModal(contentHtml) {
    // remove existing modal if any
    const existing = document.getElementById('sb-modal');
    if (existing) existing.remove();
    const modal = createElementFromHTML(`
    <div id="sb-modal" class="sb-modal">
      <div class="sb-modal-backdrop"></div>
      <div class="sb-modal-content">${contentHtml}</div>
    </div>
  `);
    document.body.appendChild(modal);
    // close handlers
    modal.querySelectorAll('[data-close]').forEach(btn => btn.addEventListener('click', () => modal.remove()));
}

async function listStudents() {
    appendMessage('bot', 'Fetching students...');
    const res = await fetch('/api/students');
    const data = await res.json();
    if (!data || data.length === 0) {
        appendMessage('bot', 'No students found.');
        return;
    }
    // render table
    let html = '<table class="students-table"><tr><th>ID</th><th>Name</th><th>Email</th><th>Department</th><th>Age</th></tr>';
    data.forEach(s => { html += `<tr><td>${s.id}</td><td>${s.name}</td><td>${s.email}</td><td>${s.department}</td><td>${s.age}</td></tr>` });
    html += '</table>';
    appendMessage('bot', html);
}

function showCreateForm() {
    const form = `
    <h3>Create Student</h3>
    <form id="create-student-form">
      <label>Name <input name="name" required></label>
      <label>Email <input name="email" required type="email"></label>
      <label>Department <input name="department" required></label>
      <label>Age <input name="age" required type="number"></label>
      <div class="row">
        <button type="submit">Create</button>
        <button type="button" data-close>Cancel</button>
      </div>
    </form>
  `;
    showModal(form);
    document.getElementById('create-student-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const payload = Object.fromEntries(fd.entries());
        payload.age = Number(payload.age);
        appendMessage('user', `Create student: ${payload.name}`);
        const res = await fetch('/api/students', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        const data = await res.json();
        if (res.status === 201) {
            appendMessage('bot', `Student created: ID ${data.id} — ${data.name}`);
        } else {
            appendMessage('bot', `Error: ${data.error || JSON.stringify(data)}`);
        }
        document.getElementById('sb-modal')?.remove();
    });
}

function showUpdateForm() {
    const form = `
    <h3>Update Student</h3>
    <form id="update-student-form">
      <label>Student ID <input name="id" required type="number"></label>
      <label>Name <input name="name"></label>
      <label>Email <input name="email" type="email"></label>
      <label>Department <input name="department"></label>
      <label>Age <input name="age" type="number"></label>
      <div class="row">
        <button type="submit">Update</button>
        <button type="button" data-close>Cancel</button>
      </div>
    </form>
  `;
    showModal(form);
    document.getElementById('update-student-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const payload = Object.fromEntries(fd.entries());
        const id = payload.id;
        delete payload.id;
        if (payload.age) payload.age = Number(payload.age);
        appendMessage('user', `Update student ID ${id}`);
        const res = await fetch(`/api/students/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        const data = await res.json();
        if (res.ok) appendMessage('bot', `Student updated: ${data.id} — ${data.name}`);
        else appendMessage('bot', `Error: ${data.error || JSON.stringify(data)}`);
        document.getElementById('sb-modal')?.remove();
    });
}

function showDeleteForm() {
    const form = `
    <h3>Delete Student</h3>
    <form id="delete-student-form">
      <label>Student ID <input name="id" required type="number"></label>
      <div class="row">
        <button type="submit">Delete</button>
        <button type="button" data-close>Cancel</button>
      </div>
    </form>
  `;
    showModal(form);
    document.getElementById('delete-student-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const { id } = Object.fromEntries(fd.entries());
        appendMessage('user', `Delete student ID ${id}`);
        const confirmed = confirm(`Are you sure you want to delete student ID ${id}?`);
        if (!confirmed) {
            appendMessage('bot', 'Deletion cancelled.');
            document.getElementById('sb-modal')?.remove();
            return;
        }
        const res = await fetch(`/api/students/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (res.ok) appendMessage('bot', `Deleted student ID ${id}`);
        else appendMessage('bot', `Error: ${data.error || JSON.stringify(data)}`);
        document.getElementById('sb-modal')?.remove();
    });
}

async function getCount() {
    appendMessage('bot', 'Fetching count...');
    const res = await fetch('/api/students/count');
    const data = await res.json();
    appendMessage('bot', `Total students: ${data.count}`);
}

opsEl.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    const action = btn.getAttribute('data-action');
    if (!action) return;
    switch (action) {
        case 'list':
            listStudents();
            break;
        case 'create':
            showCreateForm();
            break;
        case 'update':
            showUpdateForm();
            break;
        case 'delete':
            showDeleteForm();
            break;
        case 'clear':
            const chatContainer = document.getElementById('chat');
            if (chatContainer) chatContainer.innerHTML = '';
            appendMessage('bot', 'Chat cleared.');
            break;
        case 'count':
            getCount();
            break;
    }
});