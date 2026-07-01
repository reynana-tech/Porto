let profiles = [];

async function loadProfiles() {
    const res = await apiCall('/api/admin/profiles');
    profiles = res.data || [];
    renderTable();
}

function renderTable() {
    const tbody = document.getElementById('profileBody');
    if (!profiles.length) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#a09ab8;padding:24px;">Belum ada data profil</td></tr>';
        return;
    }
    tbody.innerHTML = profiles.map(p => `
        <tr>
            <td>${p.photo_url ? `<img src="${p.photo_url}" class="img-thumb" onerror="this.style.display='none'">` : '—'}</td>
            <td><strong>${p.name}</strong></td>
            <td>${p.title || '—'}</td>
            <td>${p.email || '—'}</td>
            <td>${p.location || '—'}</td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="editProfile(${p.id})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="confirmDelete(() => deleteProfile(${p.id}))">Hapus</button>
            </td>
        </tr>
    `).join('');
}

function resetForm() {
    document.getElementById('profileId').value = '';
    document.getElementById('modalTitle').textContent = 'Tambah Profil';
    ['pName','pTitle','pBio','pEmail','pPhone','pLocation','pGithub','pLinkedin','pInstagram','pPhoto'].forEach(id => {
        document.getElementById(id).value = '';
    });
}

function editProfile(id) {
    const p = profiles.find(x => x.id === id);
    if (!p) return;
    document.getElementById('profileId').value = p.id;
    document.getElementById('modalTitle').textContent = 'Edit Profil';
    document.getElementById('pName').value = p.name || '';
    document.getElementById('pTitle').value = p.title || '';
    document.getElementById('pBio').value = p.bio || '';
    document.getElementById('pEmail').value = p.email || '';
    document.getElementById('pPhone').value = p.phone || '';
    document.getElementById('pLocation').value = p.location || '';
    document.getElementById('pGithub').value = p.github || '';
    document.getElementById('pLinkedin').value = p.linkedin || '';
    document.getElementById('pInstagram').value = p.instagram || '';
    document.getElementById('pPhoto').value = p.photo_url || '';
    openModal('profileModal');
}

async function saveProfile() {
    const id = document.getElementById('profileId').value;
    const body = {
        name: document.getElementById('pName').value.trim(),
        title: document.getElementById('pTitle').value.trim(),
        bio: document.getElementById('pBio').value.trim(),
        email: document.getElementById('pEmail').value.trim(),
        phone: document.getElementById('pPhone').value.trim(),
        location: document.getElementById('pLocation').value.trim(),
        github: document.getElementById('pGithub').value.trim(),
        linkedin: document.getElementById('pLinkedin').value.trim(),
        instagram: document.getElementById('pInstagram').value.trim(),
        photo_url: document.getElementById('pPhoto').value.trim()
    };
    if (!body.name) { alert('Nama wajib diisi'); return; }

    const url = id ? `/api/admin/profiles/${id}` : '/api/admin/profiles';
    const method = id ? 'PUT' : 'POST';
    const res = await apiCall(url, method, body);
    if (res.success) {
        showToast(res.message, 'success');
        closeModal('profileModal');
        loadProfiles();
    } else {
        showToast(res.message || 'Gagal menyimpan', 'error');
    }
}

async function deleteProfile(id) {
    const res = await apiCall(`/api/admin/profiles/${id}`, 'DELETE');
    if (res.success) {
        showToast(res.message, 'success');
        loadProfiles();
    }
}

// Cloudinary Upload
async function uploadImage() {
    const file = document.getElementById('imageFile').files[0];
    if (!file) { showToast('Pilih file terlebih dahulu', 'error'); return; }

    const formData = new FormData();
    formData.append('file', file);

    document.getElementById('uploadResult').textContent = 'Mengupload...';

    const res = await fetch('/api/admin/upload', { method: 'POST', body: formData });
    const data = await res.json();

    if (data.success) {
        document.getElementById('uploadResult').textContent = 'Upload berhasil!';
        document.getElementById('pPhoto').value = data.url;
        document.getElementById('uploadPreview').style.display = 'block';
        document.getElementById('uploadedImg').src = data.url;
        document.getElementById('uploadedUrl').textContent = data.url;
        showToast('Gambar berhasil diupload ke Cloudinary', 'success');
    } else {
        document.getElementById('uploadResult').textContent = data.message;
        showToast(data.message, 'error');
    }
}

loadProfiles();
