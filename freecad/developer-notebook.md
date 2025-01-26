# FreeCAD Developer Notebook

## Overview
This notebook outlines the process of integrating custom Python functionality with FreeCAD, focusing on creating parametric parts linked to custom configurations. Key topics include Python script placement, initialization routines, UI integration, and module installation.

---

## 1. Integration with FreeCAD

### Creating Parts with Custom Data
#### Steps to Integrate Custom Data:
1. **Define and Store Configuration Parameters**: Use a custom `Configuration` class to store parameters such as dimensions, material properties, and more.
2. **Link Configurations to FreeCAD Parts**: Associate configurations with FreeCAD parts using custom properties.

#### Example: Create a Part and Link it to a Configuration
```python
import FreeCAD

def create_part_from_configuration(config):
    doc = FreeCAD.ActiveDocument
    part = doc.addObject("Part::Box", f"{config.config_name}_Part")
    part.Length = config.length
    part.Width = config.width
    part.Height = 10
    part.addProperty("App::PropertyString", "ConfigName").ConfigName = config.config_name
    doc.recompute()
```

---

## 2. Script Placement and Initialization

### Directory Structure
- **Scripts Directory**:
  - Place reusable scripts such as `part-creator.py` and `config-wizard.py` in the `scripts` directory within your module.
- **Initialization Scripts**:
  - Place `Init.py` and `InitGui.py` in the root of the module directory to handle global initialization and GUI setup.

### Required Files and Their Roles
| File Name          | Description                                                                           |
|--------------------|---------------------------------------------------------------------------------------|
| `Init.py`          | Handles global initialization tasks when the module is loaded.                       |
| `InitGui.py`       | Defines and registers GUI commands.                                                  |
| `part-creator.py`  | Script to create FreeCAD parts from configurations.                                   |
| `config-wizard.py` | Defines a PyQt-based dialog for creating and managing configurations.                 |
| `install.py`       | Automates the installation of the module into FreeCAD's Mod directory.                |
| `setup.py`         | Package metadata and dependencies for the module.                                     |

### Script Execution During Launch
- **`Init.py`** and **`InitGui.py`** are executed automatically when FreeCAD starts, provided the module is located in FreeCAD’s `Mod` directory.

---

## 3. User Interface Integration

### Configuration Wizard
#### Example: `ConfigWizard` Class
```python
from PySide2.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QSpinBox

class ConfigWizard(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Part Configuration Wizard")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.config_name_input = QLineEdit()
        form_layout.addRow(QLabel("Configuration Name:"), self.config_name_input)

        self.length_input = QSpinBox()
        self.length_input.setRange(10, 1000)
        form_layout.addRow(QLabel("Length (mm):"), self.length_input)

        self.width_input = QSpinBox()
        self.width_input.setRange(10, 1000)
        form_layout.addRow(QLabel("Width (mm):"), self.width_input)

        self.diameter_input = QSpinBox()
        self.diameter_input.setRange(1, 100)
        form_layout.addRow(QLabel("Hole Diameter (mm):"), self.diameter_input)

        layout.addLayout(form_layout)
        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.save_configuration)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_configuration(self):
        config_name = self.config_name_input.text()
        length = self.length_input.value()
        width = self.width_input.value()
        diameter = self.diameter_input.value()
        print(f"Saved Configuration: {config_name}, {length}x{width}, Hole: {diameter}mm")
        self.accept()
```

#### Launching the Wizard
- Register a command in `InitGui.py` to launch the wizard.
```python
class ConfigWizardCommand:
    def GetResources(self):
        return {
            'Pixmap': 'path/to/icon.png',  
            'MenuText': 'Open Configuration Wizard',
            'ToolTip': 'Launch the configuration wizard for creating parts.'
        }

    def Activated(self):
        wizard = ConfigWizard()
        wizard.exec_()

    def IsActive(self):
        return not FreeCADGui.ActiveDocument is None

FreeCADGui.addCommand('OpenConfigWizard', ConfigWizardCommand())
```

---

## 4. Module Installation

### Installation Script: `install.py`
Automates the copying of the module to FreeCAD's `Mod` directory.

#### Example: `install.py`
```python
import os
import sys
import shutil
import logging

FREECAD_MOD_DIR = {
    "Windows": r"C:\\Program Files\\FreeCAD\\Mod",
    "Linux": "/usr/lib/freecad/Mod",
    "MacOS": "/Applications/FreeCAD.app/Contents/Resources/Mod"
}

MODULE_NAME = "jaackd-freecad"

# Define paths and copy the module
...
```

---

## 5. Data Persistence

### JSON Configuration Storage
#### Functions for Saving and Loading Configurations
```python
import json

def save_configurations_to_json(configs, file_path):
    with open(file_path, 'w') as file:
        json.dump([config.to_dict() for config in configs], file)

def load_configurations_from_json(file_path):
    with open(file_path, 'r') as file:
        return [Configuration.from_dict(data) for data in json.load(file)]
```

---

## Conclusion
This setup provides:
- A modular, scalable system for managing parametric parts in FreeCAD.
- User-friendly interfaces for creating and managing configurations.
- Robust data persistence with JSON.
- Seamless integration with FreeCAD's document and GUI systems.

By following this guide, developers can extend FreeCAD's capabilities for custom applications.

