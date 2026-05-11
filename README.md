# 🤖 Bot Kelas Automation (v3.0.0 - Improved)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-3.0.0--Improved-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()

Bot Kelas Automation adalah asisten cerdas berbasis CLI untuk mengelola informasi harian kelas (Jadwal, Seragam, Piket, dan Tugas) dan mempublikasikannya ke WhatsApp secara otomatis.

**Versi 3.0.0 Improvements**: Robust error handling, centralized logging, config management, task preview, auto backup, dan unit tests.

---

## 🎯 Fitur Utama

### 🆕 **v3.0.0 New Features**

- ✅ **Robust Error Handling**: Try-catch di semua fungsi kritis untuk prevent crash
- ✅ **Centralized Logging System**: Track semua event dengan timestamp dan level
- ✅ **Configuration Management**: Pisahkan hardcoded values ke config file
- ✅ **Input Validation**: Validasi ketat untuk semua input user
- ✅ **Task Preview Before Send**: Konfirmasi pesan sebelum dikirim ke WhatsApp
- ✅ **Multi-Group Support**: Siap untuk support multiple groups (future)
- ✅ **Automatic Backup**: Auto backup data.json setiap startup
- ✅ **Unit Tests**: Test suite lengkap untuk semua core functions
- ✅ **Enhanced UX**: Better error messages & interactive menu

### 📦 **Core Features**

- **🕒 Smart Scheduling**: Otomatis deteksi waktu. Jika jam >= 17:00, prepare info untuk besok hari
- **💻 Cross-Platform Paste**: Support Windows, Linux, macOS (auto-detect `Ctrl+V` vs `Cmd+V`)
- **👕 Dual-Cycle Uniform**: Sistem seragam otomatis untuk minggu ganjil/genap
- **🧹 Auto-Cleanup 2.0**: Tugas expired otomatis dihapus setiap startup
- **🔗 WhatsApp Desktop Integration**: Kirim langsung ke WhatsApp Desktop (Windows)
- **📋 Task Management**: CRUD operations untuk tugas (Tambah, Edit, Lihat, Hapus)

---

## 🛠️ Instalasi

### 1. Prerequisites
- Python 3.8+
- WhatsApp Web (login di browser default) atau WhatsApp Desktop (Windows)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Optional untuk window control lebih baik:**
```bash
pip install pygetwindow --only-binary :all:
```

### 3. Setup Configuration
Edit `data.json` dengan:
- Group ID WhatsApp
- Jadwal kelas
- Info seragam & piket
- Data apapun yang diperlukan

---

## 📖 Cara Penggunaan

### Quick Start
```bash
python main.py
```

### Menu Utama

```
1. 📋 Copy Template Info       - Copy pesan ke clipboard manual
2. 🚀 Kirim Otomatis          - Auto send ke WhatsApp Desktop
3. 📖 Lihat Daftar Tugas      - View semua tasks
4. ➕ Tambah Tugas            - Add new task
5. ✏️  Edit Tugas             - Edit existing task
6. 🗑️  Hapus Tugas            - Delete task
7. ❌ Keluar                   - Exit
```

### Mode 1: Copy Manual
- Klik menu 1
- Bot generate pesan
- Copy otomatis ke clipboard
- Paste manual dengan `Ctrl+V` (or `Cmd+V`)

### Mode 2: Auto Send (WhatsApp Desktop)
- Klik menu 2
- **Preview** pesan sebelum dikirim
- Bot otomatis:
  1. Buka WhatsApp Desktop
  2. Fokus window
  3. Buka group chat via link
  4. Klik input area
  5. Paste & send
  6. Done! ✅

### Task Management
```
Menu 4: Tambah Tugas
  - Input mapel (e.g., "Matematika")
  - Input deskripsi (e.g., "Kerjakan soal halaman 50")
  - Input deadline (format: YYYY-MM-DD)
  - Validasi otomatis

Menu 3: Lihat Daftar Tugas
  - Display semua active tasks
  - Color-coded berdasarkan urgency
  - Sorting by deadline

Menu 5: Edit Tugas
  - Pilih task dari list
  - Edit field yang diperlukan
  - Leave empty untuk keep value lama

Menu 6: Hapus Tugas
  - Pilih task dari list
  - Confirmation before delete
```

---

## ⚙️ Konfigurasi

### Config Structure (`data.json`)

```json
{
  "config": {
    "group_id": "YOUR_GROUP_ID",
    "group_name": "Nama Grup",
    "bot_name": "Bot Name"
  },
  "app_settings": {
    "auto_cleanup_expired_tasks": true,
    "preview_before_send": true,
    "backup_on_startup": true,
    "whatsapp_launch_wait_seconds": 4,
    "group_open_wait_seconds": 5,
    "paste_wait_seconds": 0.5
  },
  "jadwal": { ... },
  "seragam": { ... },
  "piket": { ... },
  "tugas": []
}
```

### Key Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `group_id` | String | "" | WhatsApp group ID (ambil dari invite link) |
| `auto_cleanup_expired_tasks` | Boolean | true | Hapus task expired otomatis setiap startup |
| `preview_before_send` | Boolean | true | Tampilkan preview sebelum kirim |
| `backup_on_startup` | Boolean | true | Backup data.json setiap startup |
| `whatsapp_launch_wait_seconds` | Number | 4 | Waktu tunggu WhatsApp launch |

---

## 📂 Struktur File

```
bot-kelas-automation/
├── main.py                 # Main application (improved)
├── config.py              # Configuration management
├── logger.py              # Logging system
├── validators.py          # Input validation
├── whatsapp_handler.py    # WhatsApp automation
├── tests.py              # Unit tests
├── data.json             # Config & data
├── requirements.txt      # Dependencies
├── README.md             # This file
├── logs/                 # Auto-created, contains logs
└── backups/              # Auto-created, contains backups
```

---

## 🧪 Testing

### Run Unit Tests
```bash
python tests.py
```

### Test Coverage
- ✅ Date validation
- ✅ Group ID validation
- ✅ String validation
- ✅ Task validation
- ✅ Menu choice validation
- ✅ Yes/No input validation
- ✅ Config management
- ✅ Data cleanup logic

---

## 📊 Logging

### Log Files
- `logs/bot_YYYYMMDD.log` - Semua events
- `logs/errors_YYYYMMDD.log` - Hanya error & warning

### Log Levels
- **DEBUG**: Detail teknis
- **INFO**: Event penting
- **WARNING**: Masalah yang tidak severe
- **ERROR**: Masalah yang serious

### Contoh Log
```
2026-05-12 10:30:45 - BotKelas - INFO - Bot Kelas Automation started
2026-05-12 10:30:46 - BotKelas - INFO - Config loaded from data.json
2026-05-12 10:30:47 - BotKelas - INFO - Found school day: Senin (12/05/2026)
2026-05-12 10:31:00 - BotKelas - INFO - EVENT: Message sent via WhatsApp
```

---

## 🔒 Safety & Validation

### Input Validation
- ✅ Date format checking
- ✅ String length validation
- ✅ Group ID format validation
- ✅ Menu choice range validation
- ✅ Task data integrity

### Error Prevention
- ✅ Try-catch blocks di semua I/O operations
- ✅ Graceful handling untuk invalid input
- ✅ Prevent app crash dengan validation
- ✅ Detailed error messages untuk debugging

### Data Protection
- ✅ Automatic backup setiap startup
- ✅ Backup directory: `backups/`
- ✅ Format: `data_backup_YYYYMMDD_HHMMSS.json`

---

## 🐛 Troubleshooting

### WhatsApp Desktop tidak terbuka?
1. Check apakah WhatsApp Desktop ter-install
2. Atau gunakan Mode 1 (copy manual)
3. Fallback otomatis ke WhatsApp Web

### Group ID tidak valid?
1. Ambil dari invite link group
2. Format: `JQhpAAr7VbP783synfnW7Z` (alphanumeric 20+ char)
3. Check di group.md untuk examples

### Task tidak muncul?
1. Check format date: `YYYY-MM-DD`
2. Pastikan deadline >= hari ini
3. Check logs untuk debug info

### Config file error?
1. Check JSON syntax
2. Pastikan semua required fields ada
3. Gunakan validator online jika perlu

---

## 📝 Update Log

### [3.0.0-Improved] - 2026-05-12
- **Added**: Robust error handling & validation
- **Added**: Centralized logging system dengan file rotation
- **Added**: Configuration management system
- **Added**: Task preview before send
- **Added**: Automatic backup on startup
- **Added**: Unit tests suite lengkap
- **Added**: Enhanced UX dengan better error messages
- **Improved**: Code structure & modularity
- **Improved**: Input validation untuk prevent crash
- **Improved**: Documentation & comments
- **Fixed**: All error handling edge cases

### [2.1.0-Stable] - 2026-02-28
- **Added**: Smart scheduling logic (auto detect jam)
- **Added**: Platform detection untuk paste key
- **Fixed**: IndexError pada menu edit/hapus
- **Fixed**: Logika hari yang selalu skip

---

## 🤝 Support & Contribution

Dikembangkan dengan ❤️ oleh **irkham & Team support**

Untuk bug report, feature request, atau kontribusi:
1. Buat GitHub issue
2. Atau hubungi tim support

---

## 📄 License

MIT License - Silakan gunakan & modifikasi sesuai kebutuhan

---

## 💡 Tips

1. **Otomasi Pagi Hari**: Gunakan scheduler OS (Windows Task Scheduler / cron) untuk auto-run bot setiap pagi
2. **Multi-Group**: Duplikasi config untuk grup berbeda
3. **Backup Regular**: Backup `data.json` manually ke cloud storage
4. **Monitor Logs**: Check `logs/` folder regularly untuk potential issues

---

**Last Updated**: 2026-05-12  
**Current Version**: 3.0.0-Improved
