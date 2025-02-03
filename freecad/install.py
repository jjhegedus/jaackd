import logging
import os
import sys
import shutil
from pathlib import Path

log_folder = r""
log_file_path = r""
    
if sys.platform.startswith("win"):
    log_folder = r"C:/Logs/jaackd-freecad"
    log_file_path = r"C:/Logs/jaackd-freecad/install.log"
elif sys.platform.startswith("linux"):
    log_folder = r"/var/log/jaackd-freecad"
    log_file_path = r"/var/log/jaackd-freecad/install.log"
elif sys.platform.startswith("darwin"):
    log_folder = r"/var/log/jaackd-freecad"
    log_file_path = r"/var/log/jaackd-freecad/install.log"
else:
    raise OSError("Unsupported OS")

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file_path,
    format="%(asctime)s - %(pathname)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s")

# Add console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger = logging.getLogger(__name__)
logger.addHandler(console_handler)

logger.info("Starting install.py")

# Define paths
FREECAD_MOD_DIR = {
    "Windows": r"C:\Program Files\FreeCAD 1.0\Mod",
    "Linux": "/usr/share/freecad-daily/Mod",
    "MacOS": "/Applications/FreeCAD.app/Contents/Resources/Mod"
}

MODULE_NAME = "jaackd-freecad" 
CLONED_MODULE_DIR = "./freecad"  

def get_freecad_mod_dir():
    if sys.platform.startswith("win"):
        return os.path.join(os.getenv('APPDATA'), 'FreeCAD', 'Mod')
    elif sys.platform.startswith("linux"):
        return FREECAD_MOD_DIR["Linux"]
    elif sys.platform.startswith("darwin"):
        return FREECAD_MOD_DIR["MacOS"]
    else:
        raise OSError("Unsupported OS")
    
def copy_module_to_freecad(source_dir, target_dir):
    source_folder = Path(MODULE_NAME).resolve()
    target_path = os.path.join(target_dir, MODULE_NAME)
    
    logger.info(f"Copying module to FreeCAD directory: {target_path}")
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    else:
        logger.info("target path {target_path} does not exist")
    shutil.copytree(source_folder, target_path)


def main():
    try:
        # Determine FreeCAD Mod directory
        logger.info("Get the mod dir")
        freecad_mod_dir = get_freecad_mod_dir()
        logger.info("mod_dir: {freecad_mod_dir}")
        if not os.path.exists(freecad_mod_dir):
            raise FileNotFoundError(f"FreeCAD Mod directory not found: {freecad_mod_dir}")

        logger.info("Preparing to copy")
        # Copy the module to the FreeCAD directory
        copy_module_to_freecad(CLONED_MODULE_DIR, freecad_mod_dir)

        logger.info("Installation completed successfully!")
    except Exception as e:
        logger.info(f"An error occurred: {e}")

if __name__ == "__main__":
    logger.info("Preparing to run main")
    main()
else:
    logger.info("Unable to run main")
    