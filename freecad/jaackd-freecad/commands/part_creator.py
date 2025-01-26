import logging
import FreeCAD
import FreeCADGui as Gui

class CreatePartCommand:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def GetResources(self):
        return {
            'Pixmap': './resources/icons/create_part.svg',  # Path to the icon
            'MenuText': 'Create Part',
            'ToolTip': 'Create a part from configuration'
        }

    def Activated(self):
        # Example configuration, replace with actual configuration retrieval
        config = type('Config', (object,), {'config_name': 'Example', 'length': 10, 'width': 20})()
        self.create_part_from_configuration(config)

    def IsActive(self):
        return True
    
    def create_part_from_configuration(self, config):
        self.logger.info(f"Creating part from configuration: {config.config_name}")
        doc = FreeCAD.ActiveDocument
        part = doc.addObject("Part::Box", f"{config.config_name}_Part")
        part.Length = config.length
        part.Width = config.width
        part.Height = 10
        part.addProperty("App::PropertyString", "ConfigName").ConfigName = config.config_name
        doc.recompute()