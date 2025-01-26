import logging.config
import yaml, os
from dynamic_file_handler import DynamicFileHandler
from file_watcher import FileWatcher

workingFolder = os.getcwd()

class ConfigManager:
    def __init__(self, config_path='./config/config.yaml'):
        self.config_path = config_path
        self.config = self.load_config()
        self.file_watcher = FileWatcher(self.config_path, self.on_config_modified)
        self.file_watcher.start()

    def load_config(self):
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError as e:
            print(f"Configuration file not found: {self.config_path}")
            logging.error(f"Configuration file not found: {self.config_path}")
            raise e

    def save_config(self):
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(self.config, file)

    def modify_config(self, section, key, value):
        self.config[section][key] = value
        self.save_config()

    def delete_config_key(self, section, key):
        if key in self.config[section]:
            del self.config[section][key]
            self.save_config()

    def setup_logging(self):
        logging.config.dictConfig(self.config['logging'])

    def get_jobs(self):
        return self.config.get('jobs', [])

    def update_jobs(self, jobs):
        self.config['jobs'] = jobs
        self.save_config()

    def on_config_modified(self, event):
        if event.src_path == self.config_path:
            logging.info(f"Configuration file {event.src_path} modified. Reloading configuration.")
            self.config = self.load_config()
            # Notify other components if necessary