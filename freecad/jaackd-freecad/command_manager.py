import os
import logging
import importlib.util
import FreeCADGui as Gui
from icommand import ICommand
from utils import has_interface_methods

class CommandManager:
    def __init__(self, subfolder, callback):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing CommandManager with subfolder: {subfolder}")
        self.subfolder = subfolder
        self.callback = callback

    def load_commands(self):
        self.logger.info(f"Loading commands from {self.subfolder}")
        commands_path = os.path.join(os.path.dirname(__file__), self.subfolder)
        command_names = []
        for filename in os.listdir(commands_path):
            if filename.endswith('.py'):
                self.logger.info(f"Loading command: {filename}")
                module_name = filename[:-3]
                module_path = os.path.join(commands_path, filename)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                command_names.extend(self.register_commands_from_module(module))
        self.logger.info(f"Loaded commands: {command_names}")
        self.callback(command_names)

    def register_commands_from_module(self, module):
        command_names = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and has_interface_methods(attr(), ICommand):
                self.logger.info(f"Registering command: {attr_name}")
                command_name = attr_name
                Gui.addCommand(command_name, attr())
                command_names.append(command_name)
        self.logger.info(f"Registered commands: {command_names}")
        return command_names