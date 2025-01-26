import os
import subprocess
import sys
import logging
from pathlib import Path

workingFolder = os.getcwd()

sys.path.append(workingFolder)
from config.config_manager import ConfigManager

logger = logging.getLogger(__name__)

def setup_logging(config_manager):
    """
    Set up logging using the ConfigManager.

    Args:
        config_manager: The ConfigManager instance.
    """
    config_manager.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting test_runner.py")

def run_test_script(test_script_path):
    """
    Run the specified test script as a macro in FreeCAD.

    Args:
        test_script_path: The path to the test script.
    """
    freecad_executable = r"C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe"
    # working_folder = os.getcwd()
    working_folder = "C:\\Users\\jeff\\AppData\\Roaming\\FreeCAD\\Mod\\jaackd-freecad"

    if not os.path.exists(freecad_executable):
        logger.error(f"FreeCAD executable not found at {freecad_executable}")
        return

    if not os.path.exists(test_script_path):
        logger.error(f"Test script not found at {test_script_path}")
        return

    # Run FreeCAD with the specified macro
    try:
        test_script_path = Path(test_script_path).resolve()
        subprocess.run([freecad_executable, test_script_path], check=True, cwd=working_folder)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running FreeCAD: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python test_runner.py <path_to_test_script1> <path_to_test_script2> ...")
        sys.exit(1)

    config_path = os.path.join(os.path.dirname(__file__), "test_config.yaml")
    config_manager = ConfigManager(config_path)
    setup_logging(config_manager)

    test_script_paths = sys.argv[1:]
    for test_script_path in test_script_paths:
        logger.info(f"Running test: {test_script_path}")
        try:
            run_test_script(test_script_path)
        except Exception as e:
            logger.error(f"Error running test {test_script_path}: {e}")