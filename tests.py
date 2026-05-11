# -*- coding: utf-8 -*-
"""
Unit Tests untuk Bot Kelas Automation
Test core functions untuk memastikan semua berjalan dengan baik
"""
import unittest
from datetime import datetime, timedelta
from validators import Validator
from config import ConfigManager

class TestValidator(unittest.TestCase):
    """Test suite untuk Validator"""
    
    def test_validate_date_valid(self):
        """Test validasi date yang valid"""
        is_valid, result = Validator.validate_date("2026-12-25")
        self.assertTrue(is_valid)
        self.assertIsInstance(result, datetime)
    
    def test_validate_date_invalid_format(self):
        """Test validasi date dengan format salah"""
        is_valid, result = Validator.validate_date("25/12/2026")
        self.assertFalse(is_valid)
        self.assertIsInstance(result, str)  # Error message
    
    def test_validate_date_invalid_values(self):
        """Test validasi date dengan nilai invalid"""
        is_valid, result = Validator.validate_date("2026-13-32")
        self.assertFalse(is_valid)
    
    def test_validate_group_id_valid(self):
        """Test validasi group ID yang valid"""
        is_valid, result = Validator.validate_group_id("JQhpAAr7VbP783synfnW7Z")
        self.assertTrue(is_valid)
    
    def test_validate_group_id_empty(self):
        """Test validasi group ID kosong"""
        is_valid, result = Validator.validate_group_id("")
        self.assertFalse(is_valid)
    
    def test_validate_group_id_too_short(self):
        """Test validasi group ID terlalu pendek"""
        is_valid, result = Validator.validate_group_id("abc123")
        self.assertFalse(is_valid)
    
    def test_validate_group_id_invalid_chars(self):
        """Test validasi group ID dengan karakter invalid"""
        is_valid, result = Validator.validate_group_id("JQhpAAr7VbP783synfnW7Z@#$")
        self.assertFalse(is_valid)
    
    def test_validate_string_valid(self):
        """Test validasi string yang valid"""
        is_valid, result = Validator.validate_string("Matematika", "Mapel")
        self.assertTrue(is_valid)
        self.assertEqual(result, "Matematika")
    
    def test_validate_string_empty(self):
        """Test validasi string kosong"""
        is_valid, result = Validator.validate_string("", "Mapel")
        self.assertFalse(is_valid)
    
    def test_validate_string_too_long(self):
        """Test validasi string terlalu panjang"""
        long_text = "a" * 600
        is_valid, result = Validator.validate_string(long_text, "Mapel")
        self.assertFalse(is_valid)
    
    def test_validate_task_valid(self):
        """Test validasi task yang valid"""
        is_valid, result = Validator.validate_task(
            "Matematika",
            "Kerjakan soal halaman 50",
            "2026-12-25"
        )
        self.assertTrue(is_valid)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['mapel'], "Matematika")
    
    def test_validate_task_invalid_mapel(self):
        """Test validasi task dengan mapel invalid"""
        is_valid, result = Validator.validate_task(
            "",  # Empty mapel
            "Kerjakan soal",
            "2026-12-25"
        )
        self.assertFalse(is_valid)
    
    def test_validate_task_invalid_date(self):
        """Test validasi task dengan date invalid"""
        is_valid, result = Validator.validate_task(
            "Matematika",
            "Kerjakan soal",
            "25/12/2026"  # Wrong format
        )
        self.assertFalse(is_valid)
    
    def test_validate_menu_choice_valid(self):
        """Test validasi menu choice yang valid"""
        for choice in ['1', '2', '3', '4', '5', '6']:
            is_valid, result = Validator.validate_menu_choice(choice, 1, 6)
            self.assertTrue(is_valid)
            self.assertEqual(result, choice)
    
    def test_validate_menu_choice_cancel(self):
        """Test validasi menu choice batal"""
        is_valid, result = Validator.validate_menu_choice('b', 1, 6)
        self.assertTrue(is_valid)
        self.assertEqual(result, 'cancel')
    
    def test_validate_menu_choice_invalid(self):
        """Test validasi menu choice invalid"""
        is_valid, result = Validator.validate_menu_choice('9', 1, 6)
        self.assertFalse(is_valid)
    
    def test_validate_yes_no_yes(self):
        """Test validasi yes/no - yes"""
        for choice in ['y', 'yes', 'ya', 'Y', 'YES']:
            is_valid, result = Validator.validate_yes_no(choice)
            self.assertTrue(is_valid)
            self.assertTrue(result)
    
    def test_validate_yes_no_no(self):
        """Test validasi yes/no - no"""
        for choice in ['n', 'no', 'tidak', 'N', 'NO']:
            is_valid, result = Validator.validate_yes_no(choice)
            self.assertTrue(is_valid)
            self.assertFalse(result)
    
    def test_validate_yes_no_invalid(self):
        """Test validasi yes/no invalid"""
        is_valid, result = Validator.validate_yes_no('maybe')
        self.assertFalse(is_valid)
    
    def test_validate_index_valid(self):
        """Test validasi index yang valid"""
        is_valid, result = Validator.validate_index('1', 5)
        self.assertTrue(is_valid)
        self.assertEqual(result, 0)  # 1-indexed to 0-indexed
    
    def test_validate_index_invalid_format(self):
        """Test validasi index dengan format invalid"""
        is_valid, result = Validator.validate_index('abc', 5)
        self.assertFalse(is_valid)
    
    def test_validate_index_out_of_range(self):
        """Test validasi index di luar range"""
        is_valid, result = Validator.validate_index('10', 5)
        self.assertFalse(is_valid)


class TestConfigManager(unittest.TestCase):
    """Test suite untuk ConfigManager"""
    
    def setUp(self):
        """Setup untuk setiap test"""
        self.config = ConfigManager("test_data.json")
    
    def tearDown(self):
        """Cleanup setelah test"""
        import os
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")
    
    def test_default_config_structure(self):
        """Test struktur default config"""
        required_keys = ['config', 'app_settings', 'jadwal', 'seragam', 'piket', 'tugas']
        for key in required_keys:
            self.assertIn(key, self.config.data)
    
    def test_get_config_value(self):
        """Test get config value"""
        value = self.config.get('config.bot_name')
        self.assertIsNotNone(value)
    
    def test_set_config_value(self):
        """Test set config value"""
        self.config.set('config.bot_name', 'Test Bot')
        value = self.config.get('config.bot_name')
        self.assertEqual(value, 'Test Bot')
    
    def test_get_nested_config(self):
        """Test get nested config value"""
        value = self.config.get('app_settings.auto_cleanup_expired_tasks')
        self.assertIsNotNone(value)
    
    def test_get_nonexistent_config(self):
        """Test get config yang tidak ada"""
        value = self.config.get('nonexistent.key', 'default_value')
        self.assertEqual(value, 'default_value')


class TestDataCleanup(unittest.TestCase):
    """Test suite untuk data cleanup logic"""
    
    def test_expired_task_removal(self):
        """Test penghapusan task yang sudah expired"""
        # Create config dengan task
        config = ConfigManager("test_data_cleanup.json")
        
        # Tambah task
        today = datetime.now().date()
        expired_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        valid_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")
        
        config.data['tugas'] = [
            {'mapel': 'MTK', 'deskripsi': 'Soal 1', 'deadline': expired_date},
            {'mapel': 'IPA', 'deskripsi': 'Soal 2', 'deadline': valid_date},
        ]
        
        # Reload config (ini akan trigger cleanup)
        from main import cleanup_expired_tasks
        config.data = cleanup_expired_tasks(config.data)
        
        # Hanya 1 task yang tersisa
        self.assertEqual(len(config.data['tugas']), 1)
        self.assertEqual(config.data['tugas'][0]['mapel'], 'IPA')
        
        # Cleanup
        import os
        if os.path.exists("test_data_cleanup.json"):
            os.remove("test_data_cleanup.json")


def run_tests():
    """Run semua tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestDataCleanup))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
