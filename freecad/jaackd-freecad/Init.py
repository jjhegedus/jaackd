import logging

# Register your module and set up any global initialization tasks
def initialize():
    pass  # Add any initialization code here

log_file_path = r"C:/Logs/jaackd-freecad/Init.log"

logger = logging.getLogger(__name__)
logger.info("jaackd-freecad: sucessfully ran Init.py")