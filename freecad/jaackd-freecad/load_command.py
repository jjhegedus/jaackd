import sys
import os
import FreeCADGui
from PySide2 import QtWidgets

# Add the directory containing the commands module to the Python path
module_path = "C:\p\gh\jjhegedus\jaackd\freecad\jaackd-freecad\commands"
if module_path not in sys.path:
    print(f"Adding {module_path} to sys.path")
    sys.path.append(module_path)

from spreadsheet_varset_migrator import SpreadsheetVarsetMigrator
from test_runners import run_all_tests

def install_spreadsheet_varset_migrator():
    FreeCADGui.addCommand('MigrateToVarSet', SpreadsheetVarsetMigrator())
    print("SpreadsheetVarsetMigrator command installed successfully.")

if __name__ == "__main__":
    install_spreadsheet_varset_migrator()