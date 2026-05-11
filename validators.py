# -*- coding: utf-8 -*-
from datetime import datetime
import re
from logger import log_warning

class Validator:
    @staticmethod
    def validate_date(s, fmt="%Y-%m-%d"):
        try:
            d = datetime.strptime(s.strip(), fmt)
            return True, d
        except ValueError:
            return False, f"Format tanggal salah, gunakan {fmt}"

    @staticmethod
    def validate_group_id(gid):
        gid = gid.strip()
        if not gid: return False, "Group ID kosong"
        if len(gid) < 15: return False, "Group ID terlalu pendek (min 15 char)"
        if not re.match(r'^[a-zA-Z0-9-_]+$', gid): return False, "Group ID hanya boleh huruf, angka, -, _"
        return True, gid

    @staticmethod
    def validate_string(text, name="field", min_len=1, max_len=500):
        text = text.strip()
        if not text: return False, f"{name} tidak boleh kosong"
        if len(text) < min_len: return False, f"{name} minimal {min_len} karakter"
        if len(text) > max_len: return False, f"{name} maksimal {max_len} karakter"
        return True, text

    @staticmethod
    def validate_task(mapel, deskripsi, deadline):
        ok, val = Validator.validate_string(mapel, "Mapel", 2, 100)
        if not ok: return False, val
        mapel = val
        ok, val = Validator.validate_string(deskripsi, "Deskripsi", 3, 500)
        if not ok: return False, val
        deskripsi = val
        ok, val = Validator.validate_date(deadline)
        if not ok: return False, val
        return True, {"mapel": mapel, "deskripsi": deskripsi, "deadline": val.strftime("%Y-%m-%d")}

    @staticmethod
    def validate_menu_choice(c, min=1, max=7):
        c = c.strip().lower()
        if c == 'b': return True, 'cancel'
        try:
            n = int(c)
            if min <= n <= max: return True, str(n)
            return False, f"Pilih antara {min}-{max}"
        except:
            return False, "Masukkan angka atau b (batal)"

    @staticmethod
    def validate_yes_no(c):
        c = c.strip().lower()
        if c in ('y','yes','ya'): return True, True
        if c in ('n','no','tidak'): return True, False
        return False, "Ketik y/n"

    @staticmethod
    def validate_index(idx, length):
        try:
            i = int(idx) - 1
            if 0 <= i < length: return True, i
            return False, f"Nomor antara 1-{length}"
        except:
            return False, "Harus angka"
