# Panduan Menggunakan Fitur Simpan dan Upload di Admin Panel

## 1. Tombol Simpan Profil

### Alur Kerja:
1. Klik tombol **"+ Tambah Profil"** di halaman Profil admin
2. Isi semua field yang diperlukan:
   - **Nama Lengkap** (wajib) - gunakan nama lengkap Anda
   - **Title/Jabatan** - misalnya "Mahasiswa S1 Sistem Informasi"
   - **Bio** - ceritakan sedikit tentang diri Anda
   - **Email** - alamat email Anda
   - **Telepon** - nomor telepon Anda
   - **Lokasi** - kota/provinsi tempat tinggal
   - **GitHub URL** - link profil GitHub (opsional)
   - **LinkedIn URL** - link profil LinkedIn (opsional)
   - **URL Foto** - bisa di-copy dari hasil upload Cloudinary

3. Klik tombol **"Simpan"** untuk menyimpan data
4. Jika berhasil, akan muncul notifikasi hijau "Profil berhasil ditambahkan"
5. Modal akan tertutup otomatis dan tabel profil akan di-refresh
6. Data akan langsung muncul di halaman utama website Anda

### Catatan:
- Nama adalah field yang wajib diisi
- Data disimpan langsung ke database TiDB
- Setiap klik simpan akan membuat profil baru (untuk edit, klik tombol "Edit" di tabel)

---

## 2. Tombol Upload Gambar ke Cloudinary

### Alur Kerja:
1. Di section **"Upload Foto ke Cloudinary"**, klik **"Choose File"**
2. Pilih file gambar dari komputer Anda (format: PNG, JPG, JPEG, GIF, WebP)
3. Klik tombol **"Upload Gambar"**
4. Tunggu proses upload (akan ada tulisan "Mengupload...")
5. Jika berhasil:
   - Akan muncul notifikasi "Gambar berhasil diupload ke Cloudinary"
   - URL gambar akan otomatis muncul di field "URL Foto (dari Cloudinary)"
   - Preview gambar akan ditampilkan di bawah
6. Klik **"+ Tambah Profil"** dan paste URL foto ke field "URL Foto"
7. Klik **"Simpan"** untuk menyimpan profil dengan foto

### Catatan:
- Format file yang didukung: PNG, JPG, JPEG, GIF, WebP
- Gambar akan disimpan di Cloudinary (cloud storage)
- URL gambar yang dihasilkan bisa digunakan untuk profil, proyek, atau pengalaman
- Jika upload gagal, cek koneksi internet dan kredensial Cloudinary di .env

---

## 3. Integrasi dengan Halaman Utama

Setelah data disimpan:
- **Profil**: Data akan langsung muncul di bagian "Tentang Saya" halaman utama
- **Foto Profil**: Akan ditampilkan di hero section
- **Skill**: Jika sudah menambahkan skill, akan muncul di section "Skill & Teknologi"
- **Proyek**: Akan muncul di section "Karya Terbaik"
- **Pengalaman**: Akan muncul di section "Riwayat Pendidikan dan Pengalaman"

### Endpoint yang Digunakan:
- `POST /api/admin/profiles` - Tambah profil baru
- `PUT /api/admin/profiles/<id>` - Edit profil existing
- `POST /api/admin/upload` - Upload gambar ke Cloudinary
- `GET /api/profile` - Ambil profil (digunakan halaman utama)

---

## 4. Troubleshooting

### Jika tombol Simpan tidak berfungsi:
1. Pastikan sudah login dengan username: `admin` dan password: `admin123`
2. Buka browser Developer Console (F12 atau Ctrl+Shift+I)
3. Cari pesan error di tab "Console"
4. Lihat tab "Network" untuk melihat request yang dikirim

### Jika Upload Gambar gagal:
1. Cek file format (harus PNG, JPG, JPEG, GIF, atau WebP)
2. Pastikan file tidak lebih dari 100MB (standar Cloudinary gratis)
3. Periksa kredensial Cloudinary di file `.env`:
   ```
   CLOUDINARY_CLOUD_NAME=...
   CLOUDINARY_API_KEY=...
   CLOUDINARY_API_SECRET=...
   ```
4. Jika masih gagal, cek koneksi internet Anda

### Jika data tidak muncul di halaman utama:
1. Refresh halaman utama (Ctrl+F5 untuk hard refresh)
2. Buka browser Developer Console dan lihat response `/api/profile`
3. Pastikan sudah menekan "Simpan" dan muncul notifikasi hijau

