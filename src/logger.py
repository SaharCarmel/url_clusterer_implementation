import os
from datetime import datetime

class Logger:
    _instance = None
    _log_file = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Logger()
        return cls._instance

    @classmethod
    def initialize(cls, log_dir="logs"):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cls._log_file = os.path.join(log_dir, f"tree_log_{timestamp}.txt")
        with open(cls._log_file, 'w') as f:
            f.write(f"Tree clustering started at {timestamp}\n")

    @classmethod
    def log(cls, message, level=0):
        if cls._log_file:
            indent = "  " * level
            with open(cls._log_file, 'a') as f:
                f.write(f"{indent}{message}\n")
