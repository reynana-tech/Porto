// Toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => { toast.className = 'toast'; }, 3200);
}

// Open/close modal
function openModal(id) {
    document.getElementById(id).classList.add('open');
}
function closeModal(id) {
    document.getElementById(id).classList.remove('open');
}

// Generic API call
async function apiCall(url, method = 'GET', body = null) {
    const opts = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) opts.body = JSON.stringify(body);
    try {
        const res = await fetch(url, opts);
        const data = await res.json();
        if (!res.ok && !data.success) {
            data.success = false;
        }
        return data;
    } catch (err) {
        console.error('API call error:', err);
        return { success: false, message: 'Koneksi gagal' };
    }
}

// Confirm delete
function confirmDelete(callback) {
    if (confirm('Yakin ingin menghapus data ini?')) callback();
}
