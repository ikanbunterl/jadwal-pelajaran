# 🚀 Bot Kelas v3.0.0 - Feature Documentation

## Table of Contents
1. [Robust Error Handling](#robust-error-handling)
2. [Logging System](#logging-system)
3. [Configuration Management](#configuration-management)
4. [Input Validation](#input-validation)
5. [Task Preview](#task-preview)
6. [Automatic Backup](#automatic-backup)
7. [Unit Tests](#unit-tests)
8. [Usage Examples](#usage-examples)

---

## Robust Error Handling

### How It Works

Setiap operasi kritis di-wrap dengan try-catch blocks:

```python
try:
    # Operasi yang mungkin error
    data = load_data()
    process_data(data)
except SpecificException as e:
    # Handle specific error
    log_error(f"Specific error: {e}")
    show_user_friendly_message()
except Exception as e:
    # Fallback untuk unexpected errors
    log_error(f"Unexpected error: {e}")
    return default_value
```

### Benefits
- ✅ App tidak pernah crash karena invalid input
- ✅ User-friendly error messages
- ✅ Semua error ter-log untuk debugging
- ✅ Graceful degradation untuk missing features

### Examples

**File I/O**
```
❌ Sebelum: App crash jika file corrupted
✅ Sesudah: Show error & use default config
```

**User Input**
```
❌ Sebelum: Crash jika input format salah
✅ Sesudah: Ask user untuk input ulang
```

**WhatsApp Automation**
```
❌ Sebelum: Fail silently jika window tidak fokus
✅ Sesudah: Try multiple methods, fallback to web
```

---

## Logging System

### File Structure

```
logs/
├── bot_20260512.log       # Semua events (DEBUG+)
└── errors_20260512.log    # Hanya errors (ERROR+)
```

### Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| DEBUG | Technical details | "Looking for next school day (offset=1)" |
| INFO | Important events | "Config loaded from data.json" |
| WARNING | Non-critical issues | "Missing pygetwindow library" |
| ERROR | Serious problems | "Error loading config: JSON decode error" |

### Logging Methods

```python
from logger import log_info, log_error, log_warning, log_debug, log_event

# Info event
log_info("Bot started successfully")

# Error dengan context
log_error(f"Failed to load config: {error_details}")

# Warning untuk caution
log_warning("Missing optional library: pygetwindow")

# Debug untuk technical info
log_debug("Looking for school day with offset=1")

# Named event dengan detail
log_event("Task added", f"Math - due 2026-05-15")
```

### Accessing Logs

1. **Terminal**: Real-time view of INFO+ level messages
2. **File**: Complete history untuk debug
3. **Analysis**: Grep/search logs untuk patterns

```bash
# View today's logs
cat logs/bot_$(date +%Y%m%d).log

# View only errors
cat logs/errors_$(date +%Y%m%d).log

# Search for specific event
grep "Message sent" logs/bot_*.log

# View last 10 entries
tail -10 logs/bot_$(date +%Y%m%d).log
```

---

## Configuration Management

### ConfigManager Class

```python
from config import ConfigManager

# Load config
config = ConfigManager()

# Get values dengan nested key support
bot_name = config.get('config.bot_name')
auto_cleanup = config.get('app_settings.auto_cleanup_expired_tasks')

# Set values
config.set('config.bot_name', 'New Bot Name')
config.set('app_settings.auto_cleanup_expired_tasks', False)

# Save changes
config.save()

# Create backup
config.backup()

# Reload from file
config.reload()

# Get all config
all_data = config.get_all()

# Validate required fields
is_valid, missing_fields = config.validate_required_fields()
```

### Config File Updates

Konfigurasi sekarang terstruktur lebih baik:

```json
{
  "config": {
    "group_id": "...",
    "bot_name": "..."
  },
  "app_settings": {
    "auto_cleanup_expired_tasks": true,
    "preview_before_send": true,
    "backup_on_startup": true,
    "whatsapp_launch_wait_seconds": 4
  },
  "jadwal": { ... },
  "seragam": { ... },
  "piket": { ... },
  "tugas": []
}
```

### Features

- **Auto-merge with defaults**: Missing keys otomatis diisi dari default
- **Type-safe access**: Nested key support dengan fallback value
- **Automatic backup**: Before save, backup dibuat di `backups/` folder
- **Validation**: Check required fields pada startup

---

## Input Validation

### Validator Class

```python
from validators import Validator

# Validate date
is_valid, result = Validator.validate_date("2026-12-25")
# Result: (True, datetime_object) atau (False, error_message)

# Validate group ID
is_valid, result = Validator.validate_group_id("JQhpAAr7VbP...")
# Check: not empty, min 15 char, alphanumeric+dash+underscore

# Validate string
is_valid, result = Validator.validate_string(text, "Mapel", min_length=2, max_length=100)
# Check: not empty, length between min-max

# Validate task
is_valid, result = Validator.validate_task(mapel, deskripsi, deadline)
# Return: (True, cleaned_dict) atau (False, error_msg)

# Validate menu choice
is_valid, choice = Validator.validate_menu_choice(input_str, min_choice=1, max_choice=6)
# Support: number 1-6 atau 'b' untuk batal

# Validate yes/no
is_valid, answer = Validator.validate_yes_no(input_str)
# Support: y/yes/ya/n/no/tidak (case-insensitive)

# Validate index
is_valid, idx = Validator.validate_index("3", list_length=5)
# Return: (True, 0-indexed_int) atau (False, error_msg)
```

### Validation Examples

```python
# Valid date
is_valid, result = Validator.validate_date("2026-05-15")
# Returns: (True, datetime(2026, 5, 15, 0, 0))

# Invalid date
is_valid, result = Validator.validate_date("15/05/2026")
# Returns: (False, "Invalid date format: 15/05/2026. Expected: %Y-%m-%d")

# Valid task
is_valid, result = Validator.validate_task("MTK", "Soal hal 50", "2026-05-15")
# Returns: (True, {'mapel': 'MTK', 'deskripsi': 'Soal hal 50', 'deadline': '2026-05-15'})

# Invalid task (empty mapel)
is_valid, result = Validator.validate_task("", "Soal", "2026-05-15")
# Returns: (False, "Mapel tidak boleh kosong!")
```

---

## Task Preview

### Feature

Sebelum mengirim pesan otomatis ke WhatsApp, bot menampilkan preview untuk confirmation.

### Flow

```
1. User pilih Menu 2 (Kirim Otomatis)
   ↓
2. Bot generate message untuk hari berikutnya
   ↓
3. Tampilkan PREVIEW of message
   ↓
4. Ask confirmation: "Pesan ini sudah benar? (y/n)"
   ↓
5. If YES → lanjut ke WhatsApp
   If NO → kembali ke menu
```

### Contoh Preview

```
═════════════════════════════════════════════════════════════
   PREVIEW PESAN - SENIN
═════════════════════════════════════════════════════════════

*INFO KELAS - SENIN*
📅 12/05/2026
👕 Seragam: *Putih Abu*

*📚 JADWAL:*
• KJD & SISKOM
• MTK
• JARINGAN DASAR

*🧹 PIKET:*
• adalah pokoknya

*📝 TUGAS:*
• Matematika: Kerjakan soal hal 50 (⏳ 2 HARI LAGI)

_Generated by Bot Kelas Automation v3_

═════════════════════════════════════════════════════════════

Apakah pesan ini sudah benar?
Lanjutkan? (y/n, b untuk batal):
```

### Benefits

- ✅ Avoid mistakes before sending
- ✅ User dapat verify content
- ✅ Opportunity untuk cancel jika ada error

---

## Automatic Backup

### When?

Backup otomatis dibuat:
- ✅ Setiap startup (jika `backup_on_startup=true`)
- ✅ Manual via `config.backup()`

### Where?

```
backups/
├── data_backup_20260512_103045.json
├── data_backup_20260512_100000.json
└── data_backup_20260511_173000.json
```

Format: `data_backup_YYYYMMDD_HHMMSS.json`

### How to Restore?

```bash
# 1. Find backup you want
ls -la backups/

# 2. Copy backup to main location
cp backups/data_backup_20260512_103045.json data.json

# 3. Restart bot
python main.py
```

### Code

```python
from config import ConfigManager

config = ConfigManager()

# Backup otomatis pada startup
if config.get('app_settings.backup_on_startup'):
    config.backup()

# Manual backup
config.backup()
# → backups/data_backup_YYYYMMDD_HHMMSS.json dibuat
```

---

## Unit Tests

### Running Tests

```bash
python tests.py
```

### Test Output

```
test_validate_date_invalid_format (__main__.TestValidator) ... ok
test_validate_date_invalid_values (__main__.TestValidator) ... ok
test_validate_date_valid (__main__.TestValidator) ... ok
test_validate_group_id_empty (__main__.TestValidator) ... ok
test_validate_group_id_invalid_chars (__main__.TestValidator) ... ok
test_validate_group_id_too_short (__main__.TestValidator) ... ok
test_validate_group_id_valid (__main__.TestValidator) ... ok
...

Ran 28 tests in 0.150s
OK
```

### Test Coverage

**Validators (15 tests)**
- ✅ Date validation (valid, invalid format, invalid values)
- ✅ Group ID validation (valid, empty, too short, invalid chars)
- ✅ String validation (valid, empty, too long)
- ✅ Task validation (valid, invalid mapel, invalid date)
- ✅ Menu choice validation (valid, cancel, invalid)
- ✅ Yes/No validation (yes, no, invalid)
- ✅ Index validation (valid, invalid format, out of range)

**Config Manager (5 tests)**
- ✅ Default config structure
- ✅ Get/Set config values
- ✅ Nested config access
- ✅ Get non-existent config dengan default

**Data Cleanup (1 test)**
- ✅ Expired task removal

### Adding Custom Tests

```python
import unittest
from validators import Validator

class MyCustomTests(unittest.TestCase):
    def test_something(self):
        is_valid, result = Validator.validate_string("test")
        self.assertTrue(is_valid)
    
    def test_something_else(self):
        is_valid, result = Validator.validate_date("2026-05-15")
        self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()
```

---

## Usage Examples

### Example 1: Custom Configuration Setup

```python
from config import ConfigManager

# Load existing config
config = ConfigManager()

# Customize settings
config.set('config.bot_name', 'Bot Kelas XYZ')
config.set('app_settings.auto_cleanup_expired_tasks', True)
config.set('app_settings.preview_before_send', True)

# Update jadwal
config.data['jadwal']['Senin'] = ['MTK', 'IPA', 'Bahasa']
config.data['seragam']['Senin'] = 'Putih Abu'

# Save changes
config.save()
```

### Example 2: Logging Custom Events

```python
from logger import log_event, log_info, log_error

# Log important event
log_event("Class info sent", "Senin 2026-05-12")

# Log info
log_info("Bot started with config: data.json")

# Log error (dengan context)
try:
    result = some_operation()
except Exception as e:
    log_error(f"Operation failed: {e}")
```

### Example 3: Manual Task Management

```python
from config import ConfigManager
from validators import Validator

config = ConfigManager()

# Add task
is_valid, task = Validator.validate_task("MTK", "Soal hal 50", "2026-05-20")
if is_valid:
    config.data['tugas'].append(task)
    config.save()
    print("✅ Task added!")

# View all tasks
for task in config.data['tugas']:
    print(f"- {task['mapel']}: {task['deskripsi']} ({task['deadline']})")
```

### Example 4: WhatsApp Integration

```python
from whatsapp_handler import WhatsAppHandler
from config import ConfigManager
import pyperclip

config = ConfigManager()
handler = WhatsAppHandler(config)

# Copy text to clipboard
message = "Info Kelas Senin..."
pyperclip.copy(message)

# Send via WhatsApp
success, result = handler.send_automated(message)
if success:
    print("✅ Message sent!")
else:
    print(f"❌ Failed: {result}")
```

---

## Best Practices

### 1. Always Validate Input
```python
# ✅ GOOD
is_valid, result = Validator.validate_string(user_input, "Field Name")
if is_valid:
    process(result)

# ❌ BAD
process(user_input)  # Might crash
```

### 2. Use ConfigManager for Settings
```python
# ✅ GOOD
bot_name = config.get('config.bot_name', 'Default Bot')

# ❌ BAD
bot_name = "Hardcoded Bot Name"  # Not maintainable
```

### 3. Log All Important Events
```python
# ✅ GOOD
log_event("Task added", f"{mapel} - due {deadline}")
log_error(f"Failed to send message: {error}")

# ❌ BAD
print("Task added")  # Not tracked
```

### 4. Create Backups Before Major Changes
```python
# ✅ GOOD
config.backup()
config.set('important_setting', new_value)
config.save()

# ❌ BAD
config.set('important_setting', new_value)  # No backup
```

---

**Last Updated**: 2026-05-12  
**Version**: 3.0.0-Improved
