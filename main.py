# -*- coding: utf-8 -*-
"""
🤖 BOT KELAS AUTOMATION - IMPROVED VERSION
Developer: irkham & Team support
Version: 3.0.0-Improved

Features:
- Robust error handling & validation
- Centralized logging system
- Configuration management
- Task preview before sending
- Multi-group support
- Automatic backup
- Unit tests included
"""
import json
import pyperclip
import time
import os
import platform
from datetime import datetime, timedelta

# Import modules baru
from config import ConfigManager
from logger import log_info, log_error, log_warning, log_event, log_debug
from validators import Validator
from whatsapp_handler import WhatsAppHandler

# ==============================
# CONFIG & VERSIONING
# ==============================
VERSION = "3.0.0-Improved"
HARI_INDONESIA = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# Terminal Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

# ==============================
# UTILITY FUNCTIONS
# ==============================
def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title, subtitle=""):
    """Print formatted header"""
    print(f"{CYAN}{'='*55}{RESET}")
    print(f"{BOLD}{YELLOW}   {title.upper()}{RESET}")
    if subtitle:
        print(f"{CYAN}   {subtitle}{RESET}")
    print(f"{CYAN}   v{VERSION}{RESET}")
    print(f"{CYAN}{'='*55}{RESET}")

def print_separator():
    """Print separator line"""
    print(f"{CYAN}{'-'*55}{RESET}")

def print_success(message):
    """Print success message"""
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    """Print error message"""
    print(f"{RED}❌ {message}{RESET}")

def print_warning(message):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {message}{RESET}")

def print_info(message):
    """Print info message"""
    print(f"{CYAN}ℹ️  {message}{RESET}")

def print_menu_item(number, emoji, text):
    """Print formatted menu item"""
    print(f"{BOLD}{number}.{RESET} {emoji} {text}")

def safe_input(prompt, allow_cancel=False):
    """
    Safe input dengan handling error
    Return: tuple (input_value, is_cancelled)
    """
    try:
        result = input(f"{YELLOW}{prompt}{RESET}").strip()
        
        if allow_cancel and result.lower() == 'b':
            return None, True
        
        return result, False
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Operasi dibatalkan.{RESET}")
        return None, True
    except Exception as e:
        log_error(f"Input error: {e}")
        print_error(f"Input error: {e}")
        return None, True

def wait_for_key(seconds=1.5):
    """Wait dengan option untuk lanjut"""
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        pass

# ==============================
# CORE LOGIC - Task Management
# ==============================
def cleanup_expired_tasks(data):
    """Bersihkan task yang sudah expired"""
    tugas_lama = data.get("tugas", [])
    hari_ini = datetime.now().date()
    
    tugas_baru = []
    removed_count = 0
    
    for task in tugas_lama:
        try:
            deadline_date = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
            if deadline_date >= hari_ini:
                tugas_baru.append(task)
            else:
                removed_count += 1
                log_debug(f"Removed expired task: {task.get('mapel', 'Unknown')}")
        except (ValueError, KeyError) as e:
            log_warning(f"Invalid task format: {task}")
            tugas_baru.append(task)  # Keep anyway untuk safety
    
    if removed_count > 0:
        data['tugas'] = tugas_baru
        print_info(f"Auto-Cleanup: {removed_count} task yang sudah expired dihapus")
        log_event("Auto cleanup executed", f"Removed {removed_count} expired tasks")
    
    return data

def get_next_school_day(data):
    """
    Dapatkan hari sekolah berikutnya
    Smart scheduling: jika jam >= 17:00, ambil besok hari
    Return: (hari_name, date_obj) atau (None, None)
    """
    now = datetime.now()
    start_offset = 1 if now.hour >= 17 else 0
    
    log_debug(f"Looking for next school day (offset={start_offset})")
    
    for i in range(start_offset, 8):
        check_date = now + timedelta(days=i)
        day_name = HARI_INDONESIA[check_date.weekday()]
        
        if day_name in data.get("jadwal", {}):
            log_info(f"Found school day: {day_name} ({check_date.strftime('%d/%m/%Y')})")
            return day_name, check_date
    
    log_warning("No school day found in next 8 days")
    return None, None

def get_seragam(hari, tanggal_obj, data):
    """Get seragam untuk hari tertentu (support minggu ganjil/genap)"""
    aturan = data.get("seragam", {}).get(hari)
    
    if not aturan:
        return "Bebas/Olahraga"
    
    # Jika aturan adalah string, return langsung
    if isinstance(aturan, str):
        return aturan
    
    # Jika dict, gunakan logika minggu ganjil/genap
    if isinstance(aturan, dict):
        try:
            week_num = tanggal_obj.isocalendar()[1]
            status = "seragam" if week_num % 2 == 0 else "bebas"
            return aturan.get(f"minggu_{status}", "Bebas")
        except Exception as e:
            log_warning(f"Error calculating week: {e}")
            return "Bebas"
    
    return "Bebas/Olahraga"

def format_message(hari, tanggal_obj, data):
    """
    Format pesan untuk WhatsApp
    Return: formatted message string
    """
    try:
        jadwal = list(dict.fromkeys(data.get("jadwal", {}).get(hari, [])))
        piket = data.get("piket", {}).get(hari, ["-"])
        seragam = get_seragam(hari, tanggal_obj, data)
        
        # Format pesan utama
        teks = f"*INFO KELAS - {hari.upper()}*\n"
        teks += f"📅 {tanggal_obj.strftime('%d/%m/%Y')}\n"
        teks += f"👕 Seragam: *{seragam}*\n\n"
        
        # Jadwal
        teks += "*📚 JADWAL:*\n"
        if jadwal:
            teks += "\n".join([f"• {m}" for m in jadwal])
        else:
            teks += "• Libur"
        
        # Piket
        teks += f"\n\n*🧹 PIKET:*\n• {', '.join(piket)}\n\n"
        
        # Tugas
        teks += "*📝 TUGAS:*\n"
        tugas_aktif = []
        hari_ini = datetime.now().date()
        
        for task in sorted(data.get("tugas", []), key=lambda x: x.get("deadline", "9999-12-31")):
            try:
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                sisa = (deadline - hari_ini).days
                
                if sisa < 0:
                    continue
                
                # Status badge
                if sisa == 0:
                    status = "🔥 DEADLINE HARI INI"
                elif sisa == 1:
                    status = "⚠️ BESOK"
                else:
                    status = f"⏳ {sisa} HARI LAGI"
                
                tugas_text = f"• {task.get('mapel', 'Unknown')}: {task.get('deskripsi', 'N/A')} ({status})"
                tugas_aktif.append(tugas_text)
            except Exception as e:
                log_warning(f"Error processing task: {task} - {e}")
                continue
        
        if tugas_aktif:
            teks += "\n".join(tugas_aktif)
        else:
            teks += "• Tidak ada tugas"
        
        # Footer
        bot_name = data.get('config', {}).get('bot_name', 'Bot Kelas')
        teks += f"\n\n_Generated by {bot_name}_"
        
        return teks
    
    except Exception as e:
        log_error(f"Error formatting message: {e}")
        return f"Error generating message: {e}"

def preview_message(message, hari):
    """Preview pesan sebelum dikirim"""
    clear_screen()
    print_header("Preview Pesan", hari)
    print_separator()
    print(message)
    print_separator()
    
    print(f"\n{BOLD}Apakah pesan ini sudah benar?{RESET}")
    is_valid, is_cancelled = safe_input("Lanjutkan? (y/n, b untuk batal): ", allow_cancel=True)
    
    if is_cancelled:
        return False
    
    if is_valid and is_valid.lower() == 'y':
        return True
    
    return False

# ==============================
# MENU - Task Management
# ==============================
def menu_task_management(config, mode="tambah"):
    """Menu untuk manage task (tambah/edit/hapus)"""
    clear_screen()
    data = config.get_all()
    tugas_list = data.get("tugas", [])
    
    print_header(f"{mode.capitalize()} Tugas")
    
    # Untuk edit/hapus, tampilkan daftar task
    if mode in ["edit", "hapus"]:
        if not tugas_list:
            print_error("Tidak ada tugas!")
            wait_for_key(1.5)
            return
        
        print(f"\n{BOLD}Daftar Tugas Aktif:{RESET}")
        for i, task in enumerate(tugas_list, 1):
            deadline = task.get('deadline', '?')
            mapel = task.get('mapel', '?')
            deskripsi = task.get('deskripsi', '?')
            print(f"{i}. [{deadline}] {mapel} - {deskripsi}")
        
        index_input, cancelled = safe_input(f"\nPilih nomor (b untuk batal): ", allow_cancel=True)
        
        if cancelled or not index_input:
            return
        
        is_valid, idx = Validator.validate_index(index_input, len(tugas_list))
        if not is_valid:
            print_error(idx)
            wait_for_key(1)
            return
    
    # TAMBAH TASK
    if mode == "tambah":
        print("\nIsi data task baru:")
        
        # Input mapel
        while True:
            mapel_input, cancelled = safe_input("📖 Mapel: ", allow_cancel=True)
            if cancelled:
                return
            
            is_valid, mapel = Validator.validate_string(mapel_input, "Mapel", min_length=2)
            if is_valid:
                break
            print_error(mapel)
        
        # Input deskripsi
        while True:
            deskripsi_input, cancelled = safe_input("📝 Deskripsi: ", allow_cancel=True)
            if cancelled:
                return
            
            is_valid, deskripsi = Validator.validate_string(deskripsi_input, "Deskripsi", min_length=3)
            if is_valid:
                break
            print_error(deskripsi)
        
        # Input deadline
        while True:
            deadline_input, cancelled = safe_input("📅 Deadline (YYYY-MM-DD): ", allow_cancel=True)
            if cancelled:
                return
            
            is_valid, deadline = Validator.validate_date(deadline_input)
            if is_valid:
                deadline = deadline.strftime("%Y-%m-%d")
                break
            print_error("Format tidak valid. Contoh: 2026-03-15")
        
        tugas_list.append({
            "mapel": mapel,
            "deskripsi": deskripsi,
            "deadline": deadline
        })
        
        print_success("Task ditambahkan!")
        log_event("Task added", f"{mapel} - {deadline}")
    
    # EDIT TASK
    elif mode == "edit":
        task = tugas_list[idx]
        print(f"\nEdit task: {task.get('mapel')}")
        
        # Edit mapel
        mapel_input, _ = safe_input(f"Mapel [{task['mapel']}]: ")
        if mapel_input:
            is_valid, mapel = Validator.validate_string(mapel_input, "Mapel", min_length=2)
            if is_valid:
                task['mapel'] = mapel
        
        # Edit deskripsi
        deskripsi_input, _ = safe_input(f"Deskripsi [{task['deskripsi']}]: ")
        if deskripsi_input:
            is_valid, deskripsi = Validator.validate_string(deskripsi_input, "Deskripsi", min_length=3)
            if is_valid:
                task['deskripsi'] = deskripsi
        
        # Edit deadline
        deadline_input, _ = safe_input(f"Deadline [{task['deadline']}]: ")
        if deadline_input:
            is_valid, deadline = Validator.validate_date(deadline_input)
            if is_valid:
                task['deadline'] = deadline.strftime("%Y-%m-%d")
        
        print_success("Task diperbarui!")
        log_event("Task edited", f"{task.get('mapel')}")
    
    # HAPUS TASK
    elif mode == "hapus":
        task = tugas_list[idx]
        confirm_input, cancelled = safe_input(
            f"Hapus task '{task['mapel']}'? (y/n): "
        )
        
        if not cancelled and confirm_input and confirm_input.lower() == 'y':
            removed = tugas_list.pop(idx)
            print_success("Task dihapus!")
            log_event("Task deleted", f"{removed.get('mapel')}")
        else:
            print_warning("Hapus dibatalkan")
            wait_for_key(1)
            return
    
    # Simpan perubahan
    config.set('tugas', tugas_list)
    if config.save():
        wait_for_key(1)
    else:
        print_error("Gagal menyimpan perubahan")
        wait_for_key(1.5)

def menu_view_tasks(config):
    """Menu untuk melihat semua tasks"""
    clear_screen()
    print_header("Daftar Tugas Aktif")
    
    data = config.get_all()
    tugas_list = data.get("tugas", [])
    
    if not tugas_list:
        print_warning("Tidak ada tugas")
        wait_for_key(1.5)
        return
    
    hari_ini = datetime.now().date()
    
    print()
    for i, task in enumerate(sorted(tugas_list, key=lambda x: x.get("deadline", "9999-12-31")), 1):
        try:
            deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
            sisa = (deadline - hari_ini).days
            
            # Color based on urgency
            if sisa < 0:
                color = RED
                status = "❌ LEWAT"
            elif sisa == 0:
                color = RED
                status = "🔥 HARI INI"
            elif sisa == 1:
                color = YELLOW
                status = "⚠️ BESOK"
            else:
                color = GREEN
                status = f"⏳ {sisa} hari"
            
            print(f"{i}. {color}{task['mapel']}{RESET}")
            print(f"   {task['deskripsi']}")
            print(f"   Deadline: {task['deadline']} ({status})")
            print()
        except Exception as e:
            log_warning(f"Error displaying task: {e}")
            print(f"{i}. {task.get('mapel', 'Unknown')} - Error")
    
    wait_for_key(2)

# ==============================
# MAIN ENGINE
# ==============================
def main():
    """Main application loop"""
    log_info("Bot Kelas Automation started")
    
    # Initialize config
    config = ConfigManager()
    
    # Backup data on startup jika enabled
    if config.get('app_settings.backup_on_startup', True):
        config.backup()
    
    # Cleanup expired tasks
    if config.get('app_settings.auto_cleanup_expired_tasks', True):
        data = config.get_all()
        data = cleanup_expired_tasks(data)
        config.data = data
        config.save()
    
    # Validasi required fields
    is_valid, missing = config.validate_required_fields()
    if not is_valid:
        clear_screen()
        print_error("Missing required configuration fields:")
        for field in missing:
            print(f"  - {field}")
        print_info("Silakan isi data.json terlebih dahulu")
        wait_for_key(2)
        log_event("Bot stopped", "Missing config fields")
        return
    
    # Main loop
    while True:
        config.reload()  # Reload config setiap loop
        data = config.get_all()
        
        clear_screen()
        bot_name = data.get('config', {}).get('bot_name', 'Bot Kelas')
        print_header(bot_name, f"[{datetime.now().strftime('%H:%M')}]")
        
        print(f"{BOLD}Pilih Menu:{RESET}\n")
        print_menu_item("1", "📋", "Copy Template Info")
        print_menu_item("2", "🚀", "Kirim Otomatis (WhatsApp Desktop)")
        print_menu_item("3", "📖", "Lihat Daftar Tugas")
        print_menu_item("4", "➕", "Tambah Tugas")
        print_menu_item("5", "✏️", "Edit Tugas")
        print_menu_item("6", "🗑️", "Hapus Tugas")
        print_menu_item("7", "❌", "Keluar")
        
        choice_input, cancelled = safe_input("\nPilih Menu: ", allow_cancel=True)
        
        if cancelled:
            print_warning("Operasi dibatalkan")
            wait_for_key(1)
            continue
        
        is_valid, choice = Validator.validate_menu_choice(choice_input, 1, 7)
        if not is_valid:
            print_error(is_valid)
            wait_for_key(1)
            continue
        
        # MENU 1 & 2: Generate & send message
        if choice in ["1", "2"]:
            hari, tgl = get_next_school_day(data)
            
            if not hari:
                print_error("Jadwal tidak ditemukan di data.json!")
                wait_for_key(2)
                continue
            
            # Format message
            message = format_message(hari, tgl, data)
            
            # Copy to clipboard
            pyperclip.copy(message)
            log_debug(f"Message copied to clipboard for {hari}")
            
            if choice == "1":
                # Mode: Copy only
                clear_screen()
                print_header("Copy Mode")
                print(f"\n{BOLD}Teks untuk {hari.upper()} sudah disalin!{RESET}\n")
                
                # Show paste key
                wa_handler = WhatsAppHandler(config)
                print_info(f"Paste dengan {wa_handler.get_paste_key_display()}")
                
                print(f"\n{BOLD}Preview:{RESET}")
                print_separator()
                print(message)
                print_separator()
                
                wait_for_key(2)
                log_event("Message copied", hari)
            
            else:  # choice == "2"
                # Mode: Auto send
                if not preview_message(message, hari):
                    continue
                
                # Validasi group ID
                group_id = config.get('config.group_id', '').strip()
                if not group_id:
                    print_error("group_id kosong di data.json!")
                    wait_for_key(2)
                    continue
                
                is_valid, _ = Validator.validate_group_id(group_id)
                if not is_valid:
                    print_error("Group ID tidak valid!")
                    wait_for_key(2)
                    continue
                
                # Send via WhatsApp
                print("\n⏳ Mengirim pesan, mohon tunggu...")
                wa_handler = WhatsAppHandler(config)
                success, message_result = wa_handler.send_automated(message)
                
                if success:
                    print_success(message_result)
                    log_event("Auto send success", hari)
                else:
                    print_error(message_result)
                    log_error(f"Auto send failed: {message_result}")
                
                wait_for_key(2)
        
        elif choice == "3":
            menu_view_tasks(config)
        
        elif choice == "4":
            menu_task_management(config, "tambah")
        
        elif choice == "5":
            menu_task_management(config, "edit")
        
        elif choice == "6":
            menu_task_management(config, "hapus")
        
        elif choice == "7":
            clear_screen()
            print(f"{GREEN}Dahhh! 👋{RESET}\n")
            log_event("Bot closed", "User exit")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Bot dihentikan.{RESET}")
        log_event("Bot interrupted", "Keyboard interrupt")
    except Exception as e:
        print(f"{RED}Error tidak terduga: {e}{RESET}")
        log_error(f"Unexpected error: {e}")
        wait_for_key(2)
