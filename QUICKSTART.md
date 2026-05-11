# ⚡ Bot Kelas v3.0.0 - Quick Start Guide

## 5 Menit Setup

### Step 1: Install Dependencies (1 menit)
```bash
# Navigate to project folder
cd bot-kelas-automation

# Install required packages
pip install -r requirements.txt
```

### Step 2: Get Your Group ID (2 menit)

**Method A: From Invite Link**
1. Buka WhatsApp → Klik grup → Info grup
2. Scroll down → "Tambahkan kontak"
3. Copy link (format: `https://chat.whatsapp.com/XXXXX...`)
4. Group ID = bagian setelah `/` (contoh: `JQhpAAr7VbP783synfnW7Z`)

**Method B: Manual**
- Group ID terletak di profile group chat
- Atau check file `group.md` yang sudah ada

### Step 3: Configure data.json (1 menit)

Edit `data.json`:

```json
{
  "config": {
    "group_id": "PASTE_YOUR_GROUP_ID_HERE",
    "group_name": "Grup Kelas",
    "bot_name": "Bot Kelas Automation"
  },
  ...rest of config
}
```

### Step 4: Update Jadwal (1 menit)

Edit jadwal sesuai kelas mu:

```json
"jadwal": {
  "Senin": ["Pelajaran 1", "Pelajaran 2"],
  "Selasa": ["Pelajaran 1", "Pelajaran 2"],
  ...
}
```

### Step 5: Run Bot! (30 detik)

```bash
python main.py
```

**Done! 🎉**

---

## First Time Usage

### Mode 1: Copy Manual (Safe)
```
Menu → 1 → Copy Template Info
↓
Pesan di-copy ke clipboard
↓
Paste ke WhatsApp manual (Ctrl+V)
```

**Cocok untuk**: Test pertama kali, familiarize dengan output

### Mode 2: Auto Send (Convenient)
```
Menu → 2 → Kirim Otomatis
↓
Preview pesan
↓
Confirm kirim
↓
Bot otomatis buka WA & kirim
```

**Cocok untuk**: Penggunaan sehari-hari (Windows + WhatsApp Desktop)

---

## Common Tasks

### ➕ Tambah Task Baru
```
Menu → 4 → Tambah Tugas
↓
Input:
  Mapel: Matematika
  Deskripsi: Kerjakan soal hal 50
  Deadline: 2026-05-20
↓
✅ Task added!
```

### 📖 Lihat Semua Task
```
Menu → 3 → Lihat Daftar Tugas
↓
Display semua task dengan deadline
↓
Color-coded: 🔥 (today) ⚠️ (besok) ⏳ (nanti)
```

### ✏️ Edit Task
```
Menu → 5 → Edit Tugas
↓
Pilih task dari list
↓
Edit yang ingin diubah
↓
✅ Updated!
```

### 🗑️ Hapus Task
```
Menu → 6 → Hapus Tugas
↓
Pilih task
↓
Confirm
↓
✅ Deleted!
```

---

## Troubleshooting

### ❌ "Group ID is empty"
**Solution**: 
- Edit `data.json`
- Copy group ID ke `config.group_id`
- Save & restart

### ❌ "WhatsApp Desktop not found"
**Solution**:
- Gunakan Mode 1 (copy manual)
- Atau install WhatsApp Desktop dari Microsoft Store

### ❌ "Invalid date format"
**Solution**:
- Gunakan format `YYYY-MM-DD`
- Contoh: `2026-05-20` (bukan `20/05/2026`)

### ❌ "Message not sending"
**Solution**:
- Check WhatsApp login (Web or Desktop)
- Try Mode 1 first untuk debug
- Check logs folder: `logs/bot_YYYYMMDD.log`

---

## File Explanations

| File | Purpose |
|------|---------|
| `main.py` | Main application logic |
| `config.py` | Configuration management |
| `logger.py` | Logging system |
| `validators.py` | Input validation |
| `whatsapp_handler.py` | WhatsApp automation |
| `tests.py` | Unit tests |
| `data.json` | Your config & data |
| `requirements.txt` | Python dependencies |

---

## Tips & Tricks

### 💡 Tip 1: Schedule Bot Daily
Use Windows Task Scheduler / Linux Cron untuk auto-run bot setiap pagi

**Windows Task Scheduler**:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 6:00 AM
4. Action: `python main.py` di project folder

### 💡 Tip 2: Quick Backup
Backup `data.json` regularly ke cloud storage (Google Drive, OneDrive, dll)

### 💡 Tip 3: Customize Messages
Edit format pesan di `main.py` function `format_message()` sesuai preferensi

### 💡 Tip 4: Multi-Group Support
Duplikasi `data.json` → `data_group2.json` untuk grup berbeda

---

## Next Steps

1. ✅ **Setup selesai** → Baca `README.md` untuk detail lengkap
2. 📖 **Belajar features baru** → Check `FEATURES.md`
3. 🧪 **Test semua function** → Run `python tests.py`
4. 🚀 **Go production** → Schedule bot untuk daily use
5. 💬 **Feedback** → Report issues atau feature request

---

## Support

Jika ada masalah:
1. Check logs: `logs/bot_YYYYMMDD.log`
2. Check `README.md` troubleshooting section
3. Check `FEATURES.md` untuk detail features
4. Report issue dengan logs attached

---

**Happy Automating! 🚀**

Version: 3.0.0-Improved  
Last Updated: 2026-05-12
