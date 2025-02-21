import logging
import os
import inspect
import platform

class DynamicFileHandler(logging.FileHandler):
    def __init__(self, *args, **kwargs):
        # Set the base directory based on the operating system
        if platform.system() == 'Windows':
            self.base_dir = 'C:/Logs/jaackd-freecad'
        else:
            self.base_dir = '/var/log/jaackd-freecad'
        
        # Ensure the base directory exists
        os.makedirs(self.base_dir, exist_ok=True)
        
        super().__init__(self._get_log_file(), *args, **kwargs)

    def _get_log_file(self):
        # Get the name of the file that called the logging function
        frame = inspect.currentframe()
        while frame:
            # Skip frames from this file and the logging module
            if (frame.f_code.co_filename != __file__ and 
                'logging' not in frame.f_code.co_filename and 
                'config_manager' not in frame.f_code.co_filename):
                current_file = os.path.basename(frame.f_code.co_filename)
                break
            
            frame = frame.f_back
        else:
            current_file = 'default.log'
        
        log_file = os.path.join(self.base_dir, f"{current_file}.log")
        return log_file

    def emit(self, record):
        # Update the log file name before emitting the log record
        self.baseFilename = self._get_log_file()
        super().emit(record)