import os
import sys
import logging
import subprocess

from config.config_manager import ConfigManager

def setup_logging(config_manager):
    """
    Set up logging using the ConfigManager.

    Args:
        config_manager: The ConfigManager instance.
    """
    config_manager.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting run_tests.py")

def run_all_tests(tests_dir, config_manager):
    """
    Locate all test scripts in the specified directory and pass them to the test runner.

    Args:
        tests_dir: The directory containing the test scripts.
        config_manager: The ConfigManager instance.
    """
    setup_logging(config_manager)
    logger = logging.getLogger(__name__)

    test_runner = os.path.join(os.path.dirname(__file__), "testing/test_runner.py")
    if not os.path.exists(test_runner):
        logger.error(f"Test runner not found at {test_runner}")
        return

    test_scripts = []
    for root, _, files in os.walk(tests_dir):
        for file in files:
            if file.endswith(".py"):
                test_script = os.path.join(root, file)
                test_scripts.append(test_script)

    if test_scripts:
        logger.info(f"Found {len(test_scripts)} test scripts. Running them with the test runner.")
        try:
            subprocess.run(["python", test_runner] + test_scripts, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running test scripts: {e}")
    else:
        logger.info("No test scripts found.")

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "testing/test_config.yaml")
    config_manager = ConfigManager(config_path)

    tests_dir = os.path.join(os.path.dirname(__file__), "testing/tests")
    run_all_tests(tests_dir, config_manager)