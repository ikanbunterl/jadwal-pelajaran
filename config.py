# -*- coding: utf-8 -*-
import json, os
from datetime import datetime
from logger import log_info, log_error, log_warning

class ConfigManager:
    DEFAULT = {
        "config": {"group_id": "", "group_name": "Kelas", "bot_name": "Bot Kelas"},
        "app_settings": {
            "auto_cleanup_expired_tasks": True, "preview_before_send": True,
            "backup_on_startup": True, "whatsapp_launch_wait_seconds": 4,
            "group_open_wait_seconds": 5, "paste_wait_seconds": 0.5
        },
        "libur_nasional": [], "libur_sekolah": [],
        "seragam": {}, "jadwal": {}, "piket": {}, "tugas": []
    }

    def __init__(self, file="data.json"):
        self.file = file
        self.data = self.load()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # merge missing keys
                for k, v in self.DEFAULT.items():
                    data.setdefault(k, v)
                log_info(f"Config loaded from {self.file}")
                return data
        log_warning("Config file not found, creating default")
        self.data = self.DEFAULT.copy()
        self.save()
        return self.data

    def save(self):
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        log_info("Config saved")
        return True

    def backup(self):
        if not os.path.exists("backups"): os.makedirs("backups")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = f"backups/data_backup_{ts}.json"
        with open(self.file, 'r', encoding='utf-8') as f_in:
            with open(backup, 'w', encoding='utf-8') as f_out:
                f_out.write(f_in.read())
        log_info(f"Backup created: {backup}")
        return True

    def get(self, key, default=None):
        keys = key.split('.')
        val = self.data
        for k in keys:
            val = val.get(k, default) if isinstance(val, dict) else default
            if val == default: return default
        return val

    def set(self, key, value):
        keys = key.split('.')
        d = self.data
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value
        return True

    def validate_required_fields(self):
        required = ['config.group_id', 'config.bot_name', 'jadwal', 'seragam', 'piket']
        missing = [f for f in required if not self.get(f)]
        if missing:
            log_warning(f"Missing: {missing}")
            return False, missing
        return True, []

    def get_all(self):
        return self.data

    def reload(self):
        self.data = self.load()
        return self.data
