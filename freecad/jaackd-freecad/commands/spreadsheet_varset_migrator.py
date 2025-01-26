import logging
import FreeCADGui
from PySide2 import QtWidgets
# from spreadsheet_varset_migrator_files.parameter_mapper_ui import ParameterMapper

class SpreadsheetVarsetMigrator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def GetResources(self):
        return {
            'Pixmap': 'path/to/icon.svg', 
            'MenuText': 'Migrate to VarSet', 
            'ToolTip': 'Migrate parameters from a spreadsheet to a VarSet'}

    def Activated(self):
        spreadsheet_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open Spreadsheet', '', 'Excel Files (*.xlsx)')
        if spreadsheet_path:
            self.logger.info(f"Opening spreadsheet: {spreadsheet_path}")
            # mapper = ParameterMapper(spreadsheet_path)
            # mapper.show()

    def IsActive(self):
        return True

FreeCADGui.addCommand('MigrateToVarSet', SpreadsheetVarsetMigrator())