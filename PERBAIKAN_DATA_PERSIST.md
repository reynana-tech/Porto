# 🔧 Perbaikan Data Persistence

## Masalah yang Diperbaiki
❌ **Sebelumnya**: Data selalu hilang setelah program di-close dan dibuka kembali
✅ **Sekarang**: Data akan tersimpan permanen di database

## Root Cause
Fungsi `init_db()` di `model.py` melakukan **DROP TABLE** setiap kali aplikasi restart:
```python
# ❌ TIDAK BOLEH - menghapus semua data!
cur.execute("DROP TABLE IF EXISTS contacts")
cur.execute("DROP TABLE IF EXISTS profiles")
# ... dll
```

## Solusi yang Diterapkan
✅ **Menghapus semua DROP TABLE statement** dari `init_db()` sehingga:
- Table hanya dibuat jika belum ada (`CREATE TABLE IF NOT EXISTS`)
- Data existing tetap aman
- Data default hanya di-insert jika table kosong

## Alur Kerja Sekarang

### Saat Pertama Kali Aplikasi Dijalankan:
1. `init_db()` membuat tabel jika belum ada
2. Insert data default (Shafa Reyna Nugrahani) karena table kosong
3. Data ditampilkan di homepage

### Saat Edit Data di Admin Panel:
1. Edit profil/skill/project/experience
2. Data **berhasil disimpan ke database**
3. Database secara otomatis update

### Saat Aplikasi Di-close dan Dibuka Kembali:
1. `init_db()` run lagi
2. Table sudah ada, jadi tidak dibuat ulang
3. **Data yang terakhir diedit tetap ada** di database
4. Homepage menampilkan data yang terakhir diedit ✅

## Testing Checklist

Lakukan langkah berikut untuk memastikan semuanya berjalan:

- [ ] 1. Jalankan aplikasi: `python app.py`
- [ ] 2. Buka browser: http://localhost:5000
- [ ] 3. Login ke admin panel: http://localhost:5000/admin/login
- [ ] 4. Edit Profil → ubah nama, email, atau data lainnya
- [ ] 5. Klik "Simpan" → pastikan tersimpan
- [ ] 6. **Close aplikasi** (Ctrl+C di terminal)
- [ ] 7. **Jalankan aplikasi lagi**: `python app.py`
- [ ] 8. **Buka browser lagi** → Homepage harus menampilkan **data yang sudah diedit**, bukan data awal!

## File yang Dimodifikasi

- ✏️ `model.py` - Menghapus DROP TABLE statements dari `init_db()`

## Catatan Penting

- Jangan menjalankan `database.sql` secara manual, karena itu akan reset database
- Semua data tersimpan di TiDB cloud, bukan local
- Pastikan koneksi internet stabil saat menggunakan aplikasi
