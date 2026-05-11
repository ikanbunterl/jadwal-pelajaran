# -*- coding: utf-8 -*-
"""
Logging System untuk Bot Kelas Automation
"""
import logging
import os
from datetime import datetime

class Logger:
    """Centralized logging dengan format yang konsisten"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._init_logger()
        return cls._instance
    
    def _init_logger(self):
        """Inisialisasi logger configuration"""
        self.logger = logging.getLogger('BotKelas')
        self.logger.setLevel(logging.DEBUG)
        
        # Buat logs directory jika belum ada
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # File handler - semua log
        log_file = f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Error file handler - hanya error ke atas
        error_file = f"logs/errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.FileHandler(error_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        
        # Console handler - ke terminal
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Format konsisten untuk semua handler
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Tambah handlers ke logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """Return logger instance"""
        return self.logger

# Global logger instance
logger = Logger().get_logger()

def log_info(message):
    """Log info level"""
    logger.info(message)

def log_warning(message):
    """Log warning level"""
    logger.warning(message)

def log_error(message):
    """Log error level"""
    logger.error(message)

def log_debug(message):
    """Log debug level"""
    logger.debug(message)

def log_event(event_name, details=""):
    """Log event dengan deskripsi tambahan"""
    message = f"EVENT: {event_name}"
    if details:
        message += f" - {details}"
    logger.info(message)
