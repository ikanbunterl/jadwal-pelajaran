# -*- coding: utf-8 -*-
"""
Input Validators untuk Bot Kelas Automation
Mencegah crash dan invalid data
"""
from datetime import datetime
import re
from logger import log_warning, log_error

class Validator:
    """Centralized validation system"""
    
    @staticmethod
    def validate_date(date_string, format="%Y-%m-%d"):
        """
        Validasi format tanggal
        Return: (is_valid, datetime_obj atau error_message)
        """
        try:
            date_obj = datetime.strptime(date_string.strip(), format)
            return True, date_obj
        except ValueError as e:
            error_msg = f"Invalid date format: {date_string}. Expected: {format}"
            log_warning(error_msg)
            return False, error_msg
    
    @staticmethod
    def validate_group_id(group_id):
        """
        Validasi WhatsApp group ID
        Format: alphanumeric strings, biasanya 20+ char
        """
        group_id = group_id.strip()
        
        if not group_id:
            log_warning("Group ID is empty")
            return False, "Group ID tidak boleh kosong!"
        
        if len(group_id) < 15:
            log_warning(f"Group ID terlalu pendek: {group_id}")
            return False, "Group ID terlalu pendek (min 15 karakter)"
        
        if not re.match(r'^[a-zA-Z0-9-_]+$', group_id):
            log_warning(f"Group ID contains invalid characters: {group_id}")
            return False, "Group ID hanya boleh alphanumeric, dash, dan underscore"
        
        return True, group_id
    
    @staticmethod
    def validate_string(text, field_name="field", min_length=1, max_length=500):
        """
        Validasi string umum
        """
        text = text.strip()
        
        if not text:
            log_warning(f"{field_name} is empty")
            return False, f"{field_name} tidak boleh kosong!"
        
        if len(text) < min_length:
            log_warning(f"{field_name} terlalu pendek: {len(text)} < {min_length}")
            return False, f"{field_name} minimal {min_length} karakter"
        
        if len(text) > max_length:
            log_warning(f"{field_name} terlalu panjang: {len(text)} > {max_length}")
            return False, f"{field_name} maksimal {max_length} karakter"
        
        return True, text
    
    @staticmethod
    def validate_task(mapel, deskripsi, deadline):
        """
        Validasi data tugas secara keseluruhan
        Return: (is_valid, error_message atau dict dengan data yang sudah valid)
        """
        # Validasi mapel
        is_valid, result = Validator.validate_string(
            mapel, "Mapel", min_length=2, max_length=100
        )
        if not is_valid:
            return False, result
        mapel = result
        
        # Validasi deskripsi
        is_valid, result = Validator.validate_string(
            deskripsi, "Deskripsi", min_length=3, max_length=500
        )
        if not is_valid:
            return False, result
        deskripsi = result
        
        # Validasi deadline
        is_valid, result = Validator.validate_date(deadline)
        if not is_valid:
            return False, result
        
        deadline_obj = result
        now = datetime.now().date()
        
        # Cek apakah deadline di masa lalu (hanya warning, bukan error)
        if deadline_obj.date() < now:
            log_warning(f"Deadline sudah lewat: {deadline}")
        
        return True, {
            'mapel': mapel,
            'deskripsi': deskripsi,
            'deadline': deadline_obj.strftime("%Y-%m-%d")
        }
    
    @staticmethod
    def validate_menu_choice(choice, min_choice=1, max_choice=6):
        """
        Validasi pilihan menu
        """
        choice = choice.strip().lower()
        
        # Check jika input adalah huruf 'b' (batal)
        if choice == 'b':
            return True, 'cancel'
        
        try:
            num = int(choice)
            if min_choice <= num <= max_choice:
                return True, str(num)
            else:
                log_warning(f"Menu choice out of range: {choice}")
                return False, f"Pilihan harus antara {min_choice}-{max_choice}"
        except ValueError:
            log_warning(f"Invalid menu choice format: {choice}")
            return False, "Pilihan harus berupa angka atau 'b' (batal)"
    
    @staticmethod
    def validate_yes_no(choice, field_name="Confirmation"):
        """
        Validasi yes/no input
        """
        choice = choice.strip().lower()
        
        if choice in ['y', 'yes', 'ya']:
            return True, True
        elif choice in ['n', 'no', 'tidak']:
            return True, False
        else:
            log_warning(f"Invalid yes/no input: {choice}")
            return False, f"{field_name}: Ketik 'y' atau 'n'"
    
    @staticmethod
    def validate_index(index, list_length):
        """
        Validasi array index
        """
        try:
            idx = int(index) - 1  # User input 1-indexed
            if 0 <= idx < list_length:
                return True, idx
            else:
                return False, f"Nomor harus antara 1-{list_length}"
        except ValueError:
            return False, "Nomor harus berupa angka"
