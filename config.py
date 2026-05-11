# -*- coding: utf-8 -*-
"""
Configuration Management untuk Bot Kelas Automation
Pisahkan hardcoded values dari logic
"""
import json
import os
from datetime import datetime
from logger import log_error, log_info, log_warning

class ConfigManager:
    """Manage konfigurasi aplikasi"""
    
    DEFAULT_CONFIG = {
        "config": {
            "group_id": "",
            "group_name": "Grup Kelas",
            "bot_name": "Bot Kelas Automation"
        },
        "app_settings": {
            "auto_cleanup_expired_tasks": True,
            "preview_before_send": True,
            "backup_on_startup": True,
            "schedule_check_interval_minutes": 60,
            "whatsapp_launch_wait_seconds": 4,
            "group_open_wait_seconds": 5,
            "paste_wait_seconds": 0.5
        },
        "libur_nasional": [],
        "libur_sekolah": [],
        "seragam": {},
        "jadwal": {},
        "piket": {},
        "tugas": []
    }
    
    def __init__(self, config_file="data.json"):
        self.config_file = config_file
        self.data = self.load()
    
    def load(self):
        """Load config dari file, jika tidak ada create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Merge dengan default untuk missing keys
                    data = self._merge_with_defaults(data)
                    log_info(f"Config loaded from {self.config_file}")
                    return data
            else:
                log_warning(f"Config file not found. Creating default: {self.config_file}")
                self.data = self.DEFAULT_CONFIG.copy()
                self.save()
                return self.data
        except json.JSONDecodeError as e:
            log_error(f"Invalid JSON in {self.config_file}: {e}")
            log_info("Using default config")
            return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            log_error(f"Error loading config: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_with_defaults(self, data):
        """Merge loaded data dengan default config untuk missing keys"""
        default = self.DEFAULT_CONFIG.copy()
        
        # Merge top-level keys
        for key in default:
            if key not in data:
                data[key] = default[key]
            elif isinstance(default[key], dict) and isinstance(data.get(key), dict):
                # Recursive merge untuk nested dicts
                for subkey in default[key]:
                    if subkey not in data[key]:
                        data[key][subkey] = default[key][subkey]
        
        return data
    
    def save(self):
        """Simpan config ke file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            log_info(f"Config saved to {self.config_file}")
            return True
        except Exception as e:
            log_error(f"Error saving config: {e}")
            return False
    
    def backup(self):
        """Buat backup file"""
        try:
            if not os.path.exists('backups'):
                os.makedirs('backups')
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"backups/data_backup_{timestamp}.json"
            
            with open(self.config_file, 'r', encoding='utf-8') as f_in:
                content = f_in.read()
            
            with open(backup_file, 'w', encoding='utf-8') as f_out:
                f_out.write(content)
            
            log_info(f"Backup created: {backup_file}")
            return True
        except Exception as e:
            log_error(f"Error creating backup: {e}")
            return False
    
    def get(self, key, default=None):
        """Get config value dengan nested key support"""
        keys = key.split('.')
        value = self.data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key, value):
        """Set config value dengan nested key support"""
        keys = key.split('.')
        
        try:
            config = self.data
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
            log_info(f"Config updated: {key} = {value}")
            return True
        except Exception as e:
            log_error(f"Error setting config {key}: {e}")
            return False
    
    def validate_required_fields(self):
        """Validasi field yang wajib ada"""
        required = [
            'config.group_id',
            'config.bot_name',
            'jadwal',
            'seragam',
            'piket'
        ]
        
        missing = []
        for field in required:
            if not self.get(field):
                missing.append(field)
        
        if missing:
            log_warning(f"Missing required fields: {missing}")
            return False, missing
        
        return True, []
    
    def get_all(self):
        """Return semua config"""
        return self.data
    
    def reload(self):
        """Reload config dari file"""
        self.data = self.load()
        return self.data
