# -*- coding: utf-8 -*-
import logging, os
from datetime import datetime

class Logger:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.logger = logging.getLogger('BotKelas')
        self.logger.setLevel(logging.DEBUG)
        if not os.path.exists('logs'): os.makedirs('logs')
        dt = datetime.now().strftime('%Y%m%d')
        fh = logging.FileHandler(f"logs/bot_{dt}.log", encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        eh = logging.FileHandler(f"logs/errors_{dt}.log", encoding='utf-8')
        eh.setLevel(logging.ERROR)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        for h in (fh, eh, ch): h.setFormatter(fmt)
        for h in (fh, eh, ch): self.logger.addHandler(h)

logger = Logger().logger

def log_info(msg): logger.info(msg)
def log_warning(msg): logger.warning(msg)
def log_error(msg): logger.error(msg)
def log_debug(msg): logger.debug(msg)
def log_event(event, details=""):
    m = f"EVENT: {event}"
    if details: m += f" - {details}"
    logger.info(m)
