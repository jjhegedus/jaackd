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
