import time
import logging
import os

import FreeCAD, FreeCADGui
App = FreeCAD
Gui = FreeCADGui

from PySide2 import QtWidgets

from config.config_manager import ConfigManager

def setup_logging(config_manager):
    """
    Set up logging using the ConfigManager.

    Args:
        config_manager: The ConfigManager instance.
    """
    config_manager.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting test_copy_parts.py")

def run_test():
    logger = logging.getLogger(__name__)

    # Activate the jaackd workbench
    Gui.ActivateWorkbench("JaackdFreecad")
    logger.info("Activated JaackdFreecad workbench")

    # Run the CopyExternalParts command
    Gui.runCommand("CopyParts")
    logger.info("Ran CopyParts command")

    # Wait for the dialog to open
    time.sleep(2)

    # Get the dialog
    dialog = FreeCADGui.getMainWindow().findChild(QtWidgets.QDialog, "CopyObjectsDialog")
    if not dialog:
        logger.error("CopyObjectsDialog not found")
        return

    # Select the default folder
    default_folder = "C:/p/gh/jjhegedus/jaackd/models"
    dialog.selected_folder = default_folder
    dialog.load_objects_from_folder(default_folder)
    logger.info(f"Selected default folder: {default_folder}")

    # Wait for parts to load
    time.sleep(2)

    # Select the first four available parts
    parts_list = dialog.findChild(QtWidgets.QListWidget, "parts_list")
    for i in range(min(4, parts_list.count())):
        item = parts_list.item(i)
        checkbox = parts_list.itemWidget(item)
        checkbox.setChecked(True)
    logger.info("Selected the first four available parts")

    # Copy the selected objects
    dialog.copy_selected_objects()
    logger.info("Copied the selected objects")

    # Close the dialog
    dialog.accept()
    logger.info("Closed the dialog")

    print("Test completed successfully")

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "../test_config.yaml")
    config_manager = ConfigManager(config_path)
    setup_logging(config_manager)

    run_test()
    FreeCAD.closeDocument(FreeCAD.ActiveDocument.Name)
    FreeCADGui.getMainWindow().close()