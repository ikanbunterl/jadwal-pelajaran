# -*- coding: utf-8 -*-
import pyautogui, webbrowser, platform, subprocess, os, time
from logger import log_info, log_error, log_warning, log_event

class WhatsAppHandler:
    CYAN='\033[96m'; YELLOW='\033[93m'; RED='\033[91m'; GREEN='\033[92m'; RESET='\033[0m'

    def __init__(self, config):
        self.config = config
        self.is_win = platform.system() == "Windows"
        self.paste_key = 'command' if platform.system()=='Darwin' else 'ctrl'

    def open_whatsapp_desktop(self):
        if not self.is_win:
            log_warning("Hanya Windows, fallback ke Web")
            webbrowser.open("https://web.whatsapp.com")
            time.sleep(6)
            return False
        for method in [lambda: os.startfile("whatsapp://"),
                       lambda: subprocess.Popen(["explorer.exe","shell:AppsFolder\\WhatsAppDesktop_cv1g1gvanyjgm!App"]),
                       lambda: os.startfile(os.path.join(os.getenv("LOCALAPPDATA",""),"WhatsApp","WhatsApp.exe"))]:
            try:
                method()
                time.sleep(self.config.get('app_settings.whatsapp_launch_wait_seconds',4))
                log_info("WhatsApp Desktop launched")
                return True
            except: continue
        webbrowser.open("https://web.whatsapp.com")
        return False

    def focus_whatsapp_window(self):
        try:
            import pygetwindow as gw
            wins = [w for w in gw.getWindowsWithTitle("WhatsApp") if w.visible and not w.isMinimized]
            if wins:
                wins[0].activate()
                time.sleep(1.5)
                return True
        except:
            log_warning("pygetwindow not available")
        return True  # proceed anyway

    def click_chat_input(self):
        w, h = pyautogui.size()
        pyautogui.click(w//2, int(h*0.92), clicks=2, interval=0.3)
        time.sleep(0.8)
        return True

    def open_group(self, group_id):
        os.startfile(f"https://chat.whatsapp.com/{group_id}")
        time.sleep(self.config.get('app_settings.group_open_wait_seconds',5))
        return True

    def paste_and_send(self):
        pyautogui.hotkey(self.paste_key, 'v')
        time.sleep(self.config.get('app_settings.paste_wait_seconds',0.5))
        pyautogui.press('enter')
        time.sleep(0.5)
        return True

    def send_automated(self, text):
        steps = [
            ("Buka WA", self.open_whatsapp_desktop),
            ("Fokus window", self.focus_whatsapp_window),
            ("Buka grup", lambda: self.open_group(self.config.get('config.group_id'))),
            ("Klik input", self.click_chat_input),
            ("Paste & kirim", self.paste_and_send),
        ]
        for name, func in steps:
            if not func():
                log_error(f"Gagal di step: {name}")
                return False, f"Gagal di: {name}"
        return True, "Pesan terkirim!"

    def get_paste_key_display(self):
        return self.paste_key.upper() + "+V"
