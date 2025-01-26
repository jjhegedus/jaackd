import FreeCADGui as Gui
import logging, debugpy

from PySide2 import QtWidgets

def show_freecad_message_box(title, message):
    """
    Show a message box in FreeCAD.

    :param title: The title of the message box.
    :param message: The message to display in the message box.
    """
    msg_box = QtWidgets.QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.exec_()

# Example usage within the InitGui.py context
show_freecad_message_box("Information", "This is a message box in FreeCAD.")

from config.config_manager import ConfigManager
# from background import BackgroundProcessor
# from command_manager import CommandManager


class HelloWorldCommand:
    def GetResources(self):
        return {
            'Pixmap': './resources/icons/jaackd-freecad.svg',  # Path to the icon
            'MenuText': 'Hello World',
            'ToolTip': 'Hello World'
        }

    def Activated(self):
        # Code to execute when the command is activated
        show_freecad_message_box("Hello", "Hello, World!")

    def IsActive(self):
        return True

class JaackdFreecad(Gui.Workbench):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        debugpy.listen(5678)
        print("Waiting for debugger attach")
        debugpy.wait_for_client()
        debugpy.breakpoint()
        print('break on this line')
        # self.config_manager = ConfigManager()  # Store the instance of ConfigManager
        # self.config_manager.setup_logging()

        # self.logger = logging.getLogger(__name__)
        # self.__class__.Icon = "./resources/icons/jaackd-freecad.svg"
        # self.__class__.MenuText = "Jaackd FreeCAD"
        # self.__class__.ToolTip = "Jaackd FreeCAD workbench"

    def Initialize(self):
        self.logger.info("JaackdFreecad workbench: begin initialization")
        # Gui.addCommand('HelloWorld', HelloWorldCommand())  # Register the command
        # self.appendToolbar("Jaackd Tools", ["HelloWorld"])
        # self.appendMenu("Jaackd", ["HelloWorld"])

        # self.command_manager = CommandManager('commands', self.add_commands_to_ui)
        # self.command_manager.load_commands()

        # self.processor = BackgroundProcessor(self.config_manager)  # Pass the ConfigManager instance
        # self.processor.start()

        self.logger.info("JaackdFreecad workbench: end initialization")

    def add_commands_to_ui(self, command_names):
        self.logger.info(f"Adding commands to UI: {command_names}")
        self.appendToolbar("Jaackd Tools", command_names)
        self.appendMenu("Jaackd", command_names)

    def Activated(self):
        pass

    def Deactivated(self):
        pass

Gui.addWorkbench(JaackdFreecad())