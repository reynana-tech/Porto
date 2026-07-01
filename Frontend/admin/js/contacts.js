async function loadContacts() {
    const res = await apiCall('/api/admin/contacts');
    const contacts = res.data || [];
    const tbody = document.getElementById('contactBody');
    if (!contacts.length) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#a09ab8;padding:24px;">Belum ada pesan masuk</td></tr>';
        return;
    }
    tbody.innerHTML = contacts.map(c => `
        <tr>
            <td><strong>${c.name}</strong></td>
            <td><a href="mailto:${c.email}" style="color:#8b78b8; text-decoration:none;">${c.email}</a></td>
            <td>${c.subject || '—'}</td>
            <td style="max-width:240px; color:#6b6480;">${c.message}</td>
            <td style="color:#a09ab8; font-size:12px; white-space:nowrap;">${formatDate(c.created_at)}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="confirmDelete(() => deleteContact(${c.id}))">Hapus</button>
            </td>
        </tr>
    `).join('');
}

function formatDate(dt) {
    if (!dt) return '—';
    const d = new Date(dt);
    return d.toLocaleDateString('id-ID', { day:'numeric', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });
}

async function deleteContact(id) {
    const res = await apiCall(`/api/admin/contacts/${id}`, 'DELETE');
    if (res.success) { showToast(res.message, 'success'); loadContacts(); }
}

loadContacts();
