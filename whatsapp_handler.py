# -*- coding: utf-8 -*-
"""
WhatsApp Handler untuk Bot Kelas Automation
Abstraksi WhatsApp Desktop automation logic
"""
import pyautogui
import webbrowser
import platform
import subprocess
import os
import time
from logger import log_info, log_error, log_warning, log_event

class WhatsAppHandler:
    """Handle semua interaksi dengan WhatsApp"""
    
    # Color codes untuk terminal
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    
    def __init__(self, config):
        self.config = config
        self.is_desktop_available = platform.system() == "Windows"
        self.paste_key = self._get_paste_key()
    
    @staticmethod
    def _get_paste_key():
        """Deteksi paste key berdasarkan OS"""
        system = platform.system()
        if system == 'Darwin':  # macOS
            return 'command'
        else:
            return 'ctrl'
    
    def open_whatsapp_desktop(self):
        """
        Buka WhatsApp Desktop (Windows only)
        Return: True jika berhasil
        """
        if not self.is_desktop_available:
            log_warning("WhatsApp Desktop hanya tersedia di Windows")
            return False
        
        try:
            # Method 1: URI Scheme (whatsapp://)
            log_info("Launching WhatsApp Desktop via URI scheme...")
            print(f"{self.CYAN}🔓 Launching WhatsApp Desktop...{self.RESET}")
            os.startfile("whatsapp://")
            time.sleep(self.config.get('app_settings.whatsapp_launch_wait_seconds', 4))
            return True
        except Exception as e:
            log_warning(f"URI scheme failed: {e}")
        
        try:
            # Method 2: Launch via Shell AppsFolder (UWP)
            log_info("Launching WhatsApp Desktop via AppsFolder...")
            print(f"{self.CYAN}🔓 Launching via AppsFolder...{self.RESET}")
            subprocess.Popen(
                ["explorer.exe", "shell:AppsFolder\\WhatsAppDesktop_cv1g1gvanyjgm!App"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(self.config.get('app_settings.whatsapp_launch_wait_seconds', 4))
            return True
        except Exception as e:
            log_warning(f"AppsFolder method failed: {e}")
        
        try:
            # Method 3: Direct EXE path
            log_info("Launching WhatsApp Desktop via EXE...")
            wa_paths = [
                os.path.join(os.getenv("LOCALAPPDATA", ""), "WhatsApp", "WhatsApp.exe"),
                os.path.join(os.getenv("PROGRAMFILES", ""), "WhatsApp", "WhatsApp.exe"),
            ]
            for path in wa_paths:
                if os.path.exists(path):
                    print(f"{self.CYAN}🔓 Launching via EXE...{self.RESET}")
                    os.startfile(path)
                    time.sleep(self.config.get('app_settings.whatsapp_launch_wait_seconds', 4))
                    return True
        except Exception as e:
            log_warning(f"EXE method failed: {e}")
        
        # Fallback: Web WhatsApp
        log_info("Fallback to WhatsApp Web")
        print(f"{self.YELLOW}⚠️  Fallback ke WhatsApp Web...{self.RESET}")
        webbrowser.open("https://web.whatsapp.com")
        time.sleep(6)
        return False
    
    def focus_whatsapp_window(self):
        """Fokus window WhatsApp Desktop"""
        try:
            import pygetwindow as gw
            log_info("Attempting to focus WhatsApp window...")
            
            wins = [w for w in gw.getWindowsWithTitle("WhatsApp") 
                   if w.visible and not w.isMinimized]
            
            if wins:
                win = wins[0]
                if win.isMinimized:
                    win.restore()
                win.activate()
                time.sleep(1.5)
                log_info("WhatsApp window focused")
                return True
            
            log_warning("No visible WhatsApp window found")
            return False
        
        except ImportError:
            log_warning("pygetwindow not installed for window control")
            print(f"{self.YELLOW}💡 Untuk window control lebih baik, install:{self.RESET}")
            print(f"   pip install pygetwindow --only-binary :all:{self.RESET}")
            return False
        
        except Exception as e:
            log_error(f"Window focus error: {e}")
            return False
    
    def click_chat_input(self):
        """Klik area input chat WhatsApp"""
        try:
            log_info("Clicking chat input area...")
            print(f"{self.CYAN}🖱️  Fokus ke input chat...{self.RESET}")
            
            screen_w, screen_h = pyautogui.size()
            x = screen_w // 2
            y = int(screen_h * 0.92)  # 92% dari tinggi
            
            pyautogui.click(x, y, clicks=2, interval=0.3)
            time.sleep(0.8)
            log_info(f"Clicked at ({x}, {y})")
            return True
        
        except Exception as e:
            log_error(f"Auto-click error: {e}")
            print(f"{self.YELLOW}⚠️  Auto-click error: {e}{self.RESET}")
            return False
    
    def open_group(self, group_id):
        """Buka grup WhatsApp via link"""
        try:
            log_info(f"Opening group: {group_id}")
            print(f"{self.CYAN}🔗 Membuka grup...{self.RESET}")
            
            link = f"https://chat.whatsapp.com/{group_id}"
            os.startfile(link)
            
            wait_time = self.config.get('app_settings.group_open_wait_seconds', 5)
            time.sleep(wait_time)
            log_info(f"Group opened, waited {wait_time}s")
            return True
        
        except Exception as e:
            log_error(f"Error opening group: {e}")
            print(f"{self.RED}❌ Gagal buka grup: {e}{self.RESET}")
            return False
    
    def paste_and_send(self):
        """Paste teks dan kirim pesan"""
        try:
            log_info(f"Pasting text with {self.paste_key}+V...")
            print(f"{self.CYAN}📤 Mengirim...{self.RESET}")
            
            paste_wait = self.config.get('app_settings.paste_wait_seconds', 0.5)
            pyautogui.hotkey(self.paste_key, 'v')
            time.sleep(paste_wait)
            
            pyautogui.press('enter')
            time.sleep(0.5)
            
            log_event("Message sent via WhatsApp")
            print(f"{self.GREEN}🚀 Terkirim ke WhatsApp Desktop!{self.RESET}")
            return True
        
        except Exception as e:
            log_error(f"Paste and send error: {e}")
            print(f"{self.RED}❌ Error mengirim: {e}{self.RESET}")
            return False
    
    def send_automated(self, text):
        """
        Workflow otomatis untuk mengirim pesan
        Return: (success, message)
        """
        steps = [
            ("Launch WhatsApp", self.open_whatsapp_desktop),
            ("Focus window", self.focus_whatsapp_window),
            ("Open group", lambda: self.open_group(self.config.get('config.group_id'))),
            ("Click input", self.click_chat_input),
            ("Paste and send", self.paste_and_send),
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    log_error(f"Failed at step: {step_name}")
                    return False, f"Failed at: {step_name}"
                time.sleep(0.5)
            except Exception as e:
                log_error(f"Error at {step_name}: {e}")
                return False, f"Error at {step_name}: {str(e)}"
        
        return True, "Message sent successfully"
    
    def get_paste_key_display(self):
        """Return paste key untuk display"""
        return self.paste_key.upper() + "+V"
