# 📦 Spec Checker v1.0

**Spec Checker v1.0 adalah aplikasi desktop berbasis Python-Tkinter yang digunakan untuk menampilkan spesifikasi perangkat Windows secara lengkap.**  
Aplikasi ini dilengkapi fitur untuk menyimpan hasil spesifikasi ke file `.txt` dalam satu klik.

---

## 📌 Fitur Utama

- Menampilkan detail spesifikasi hardware & sistem:
  - CPU, GPU, RAM
  - Drive storage (jenis & model)
  - Serial Number BIOS
  - Merk & Model Laptop/PC
  - MAC Address LAN & Wi-Fi
  - IP Address lokal
  - OS version & CPU Core Count
  - System uptime (jam, menit, detik)
  - Tahun pembuatan BIOS
- Tombol **Cek Spesifikasi** untuk mengambil data realtime
- Tombol **Simpan ke File** untuk export hasil ke `device_specs.txt`
- Tampilan GUI sederhana menggunakan Tkinter
- Support **Multiple GPU**
- IP Address akurat via koneksi aktif

---

## 📥 Instalasi & Cara Pakai

### Clone repository ini:

```bash
git clone https://github.com/Gilang222/spec-checker.git

cd spec-checker

pip install -r requirements.txt

python spec_checker.py
