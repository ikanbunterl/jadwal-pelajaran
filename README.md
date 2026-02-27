# 🤖 Bot Kelas Automation (Beta)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-BETA-orange.svg)]()

Bot Kelas Automation adalah asisten berbasis **Command Line Interface (CLI)** yang dirancang untuk mempermudah manajemen informasi harian kelas. Bot ini mengotomatisasi pembuatan template pesan WhatsApp yang rapi dan mengirimkannya secara instan.



---

## ✨ Fitur Unggulan

* **⚡ Auto-Paste Sender**: Menggunakan metode *simulated paste* (Ctrl+V) untuk menjaga integritas emoji dan format teks agar tidak berantakan.
* **👕 Smart Uniform System**: Mendukung aturan seragam mingguan (Ganjil/Genap) secara otomatis berdasarkan kalender.
* **📅 Intelligent Deadline**: Memberikan label status pada tugas (HARI INI, BESOK, H-3, dll.) untuk meningkatkan kewaspadaan siswa.
* **🧹 Auto-Cleanup**: Menghapus tugas yang sudah melewati deadline secara otomatis setiap kali aplikasi dijalankan.
* **📜 Activity Logs**: Mencatat setiap aksi (tambah/edit/kirim) ke dalam `log.txt` untuk pemantauan sistem.

---

## 🛠️ Instalasi

1.  **Clone atau Download** repository ini.
2.  Pastikan sudah terinstall **Python 3.x**.
3.  Install library yang dibutuhkan via terminal:
    ```bash
    pip install pyperclip pyautogui
    ```

---

## ⚙️ Konfigurasi (data.json)

Edit file `data.json` untuk menyesuaikan identitas kelasmu:
```json
{
  "config": {
    "group_id": "KODE_INVITE_GRUP",
    "bot_name": "Bot Kelas X-TKJ"
  },
  "seragam": {
    "Selasa": {
      "minggu_seragam": "Batik Sekolah",
      "minggu_bebas": "Batik Bebas"
    }
  }
}
```
---

🕒 Update Log (Beta Version)
[2.0.0-Beta] - 2026-02-27
Added:
Logging System: Semua aktivitas kini tercatat di log.txt.
Smart Validation: Input tanggal tugas kini diverifikasi (Anti-Crash).
Auto-Cleanup: Fungsi pembersihan tugas kadaluarsa secara otomatis.
Improved UI: Tampilan terminal lebih berwarna dan rapi.
Fixed:
Double Text Bug: Menghapus duplikasi pada jadwal pelajaran (seperti Upacara ganda).
Symbol Distortion: Beralih ke metode Paste untuk menjamin emoji & bullet point tampil sempurna di WhatsApp.
👥 Tim Pengembang
irkham - Lead Developer & Architect
Team Support - Logic & Testing
Catatan: Bot ini menggunakan automasi layar. Pastikan tab WhatsApp Web sudah siap sebelum memilih opsi "Kirim Otomatis".
