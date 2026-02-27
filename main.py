# -*- coding: utf-8 -*-
"""
🤖 BOT KELAS AUTOMATION - BETA VERSION
Developer: irkham & Team support
Version: 2.0.0-Beta
"""

import json
import pyperclip
import time
import os
import pyautogui
import webbrowser
from datetime import datetime, timedelta

# --- CONFIG & VERSIONING ---
VERSION = "2.0.0-Beta"
NAMA_FILE_DATA = "data.json"
HARI_INDONESIA = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# Warna Terminal
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

# ==============================
# LOG SYSTEM
# ==============================

def log_event(pesan):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{waktu}] {pesan}\n")

# ==============================
# UTILS
# ==============================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print(f"{CYAN}{'='*45}{RESET}")
    print(f"{BOLD}{YELLOW}  {title.upper()} {CYAN}(v{VERSION}){RESET}")
    print(f"{CYAN}{'='*45}{RESET}")

def validasi_tanggal(tanggal_str):
    try:
        datetime.strptime(tanggal_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# ==============================
# DATA MANAGEMENT
# ==============================

def load_data():
    try:
        if not os.path.exists(NAMA_FILE_DATA):
            default_data = {
                "config": {"group_id": "", "bot_name": "Bot Kelas"},
                "seragam": {}, "jadwal": {}, "piket": {}, "tugas": []
            }
            save_data(default_data)
            return default_data

        with open(NAMA_FILE_DATA, "r", encoding="utf-8") as f:
            data = json.load(f)
            return bersihkan_tugas_kadaluarsa(data)
    except Exception as e:
        print(f"{RED}❌ Error load data: {e}{RESET}")
        log_event(f"ERROR load data: {e}")
        return None

def save_data(data):
    try:
        with open(NAMA_FILE_DATA, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        log_event(f"ERROR save data: {e}")
        return False

# ==============================
# AUTO CLEANUP
# ==============================

def bersihkan_tugas_kadaluarsa(data):
    tugas_lama = data.get("tugas", [])
    hari_ini = datetime.now().date()
    tugas_baru = []
    
    for t in tugas_lama:
        try:
            dl = datetime.strptime(t["deadline"], "%Y-%m-%d").date()
            if dl >= hari_ini:
                tugas_baru.append(t)
        except: continue

    if len(tugas_baru) != len(tugas_lama):
        selisih = len(tugas_lama) - len(tugas_baru)
        data["tugas"] = tugas_baru
        save_data(data)
        print(f"{YELLOW}🧹 Auto-Cleanup: {selisih} tugas kadaluarsa dihapus.{RESET}")
        log_event(f"Auto cleanup hapus {selisih} tugas")
    return data

# ==============================
# CORE LOGIC
# ==============================

def get_seragam(hari, tanggal_obj, data):
    aturan = data.get("seragam", {}).get(hari)
    if not aturan: return "Bebas"
    if isinstance(aturan, dict):
        week_num = tanggal_obj.isocalendar()[1]
        status = "seragam" if week_num % 2 == 0 else "bebas"
        return aturan.get(f"minggu_{status}", "Bebas")
    return aturan

def get_next_school_day(data):
    for i in range(1, 8):
        next_date = datetime.now() + timedelta(days=i)
        day_name = HARI_INDONESIA[next_date.weekday()]
        if day_name in data.get("jadwal", {}):
            return day_name, next_date
    return None, None

def format_teks_wa(hari, tanggal_obj, data):
    if not hari: return "❌ Jadwal tidak ditemukan."
    
    jadwal = list(dict.fromkeys(data.get("jadwal", {}).get(hari, [])))
    piket = data.get("piket", {}).get(hari, ["-"])
    tugas_list = data.get("tugas", [])
    seragam = get_seragam(hari, tanggal_obj, data)

    teks = f"*INFO KELAS - {hari.upper()}*\n"
    teks += f"📅 {tanggal_obj.strftime('%d/%m/%Y')}\n"
    teks += f"👕 Seragam: *{seragam}*\n\n"
    teks += "*📚 JADWAL:*\n" + ("\n".join([f"• {m}" for m in jadwal]) if jadwal else "• Libur")
    teks += f"\n\n*🧹 PIKET:* {', '.join(piket)}\n\n*📝 TUGAS:*\n"

    hari_ini = datetime.now().date()
    tugas_aktif = []
    for t in sorted(tugas_list, key=lambda x: x.get("deadline", "")):
        try:
            dl = datetime.strptime(t["deadline"], "%Y-%m-%d").date()
            sisa = (dl - hari_ini).days
            if sisa < 0: continue
            
            # Status Mapping
            if sisa == 0: status = "🔥 DEADLINE HARI INI"
            elif sisa == 1: status = "⚠️ BESOK"
            elif sisa <= 3: status = f"⏳ {sisa} HARI LAGI"
            else: status = f"📅 H-{sisa}"
            
            tugas_aktif.append(f"• {t['mapel']}: {t['deskripsi']} ({status})")
        except: continue

    teks += "\n".join(tugas_aktif) if tugas_aktif else "• Aman Jaya."
    teks += "\n\n_Generated by Bot irkham & Team support_"
    return teks

# ==============================
# MENUS (Diringkas untuk efisiensi)
# ==============================

def menu_tugas(data, mode="tambah"):
    clear_screen()
    print_header(f"{mode.capitalize()} Tugas")
    tugas = data.get("tugas", [])

    if mode in ["edit", "hapus"]:
        if not tugas:
            print(f"{RED}Data kosong!{RESET}"); time.sleep(1); return
        for i, t in enumerate(tugas):
            print(f"{i+1}. {t['mapel']} ({t['deadline']})")
        try:
            idx = int(input(f"\nPilih nomor: ")) - 1
            if not (0 <= idx < len(tugas)): return
        except: return

    if mode == "tambah":
        m = input("📖 Mapel: ")
        d = input("📝 Deskripsi: ")
        while True:
            dead = input("📅 Deadline (YYYY-MM-DD): ")
            if validasi_tanggal(dead): break
        tugas.append({"mapel": m, "deskripsi": d, "deadline": dead})
        log_event(f"Tambah: {m}")
    
    elif mode == "edit":
        t = tugas[idx]
        t["mapel"] = input(f"Mapel [{t['mapel']}]: ") or t["mapel"]
        t["deskripsi"] = input(f"Deskripsi [{t['deskripsi']}]: ") or t["deskripsi"]
        while True:
            new_dead = input(f"Deadline [{t['deadline']}]: ") or t["deadline"]
            if validasi_tanggal(new_dead): t["deadline"] = new_dead; break
        log_event(f"Edit: {t['mapel']}")

    elif mode == "hapus":
        m = tugas.pop(idx)["mapel"]
        log_event(f"Hapus: {m}")

    save_data(data)
    print(f"{GREEN}✅ Berhasil!{RESET}"); time.sleep(1.2)

# ==============================
# MAIN
# ==============================

def main():
    while True:
        data = load_data()
        if not data: break
        clear_screen()
        print_header(data['config'].get('bot_name', 'Bot Kelas'))
        print(f"{BOLD}1.{RESET} 📋 Copy Template")
        print(f"{BOLD}2.{RESET} 🚀 Kirim Otomatis (Paste)")
        print(f"{BOLD}3.{RESET} ➕ Tambah Tugas")
        print(f"{BOLD}4.{RESET} ✏️  Edit Tugas")
        print(f"{BOLD}5.{RESET} 🗑️  Hapus Tugas")
        print(f"{BOLD}6.{RESET} ❌ Keluar")

        p = input(f"\n{YELLOW}Pilih Menu: {RESET}")
        if p in ["1", "2"]:
            hari, tgl = get_next_school_day(data)
            if not hari: print(f"{RED}Jadwal Kosong!{RESET}"); time.sleep(1.5); continue
            teks = format_teks_wa(hari, tgl, data)
            pyperclip.copy(teks)
            if p == "2":
                webbrowser.open(f"https://web.whatsapp.com/accept?code={data['config']['group_id']}")
                print(f"{CYAN}⏳ Loading WA Web (15s)...{RESET}")
                time.sleep(15)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1)
                pyautogui.press('enter')
                log_event(f"Sent WA: {hari}")
            else:
                log_event(f"Copy: {hari}")
                print(f"{GREEN}✅ Disalin!{RESET}"); time.sleep(1)
        elif p == "3": menu_tugas(data, "tambah")
        elif p == "4": menu_tugas(data, "edit")
        elif p == "5": menu_tugas(data, "hapus")
        elif p == "6": break

if __name__ == "__main__":
    main()
