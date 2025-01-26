import sys
import pandas as pd
from PySide2 import QtWidgets
from view_model import ViewModel
from table_model import TableModel
import sys

class ParameterMapper(QtWidgets.QWidget):
    def __init__(self, spreadsheet_path):
        super().__init__()
        self.view_model = ViewModel(spreadsheet_path)
        self.df = self.view_model.get_dataframe()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Parameter Mapper')
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()

        self.table_model = TableModel(self.df)
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.table_model)

        layout.addWidget(self.table)

        self.saveButton = QtWidgets.QPushButton('Save Mapping')
        self.saveButton.clicked.connect(self.saveMapping)
        layout.addWidget(self.saveButton)

        self.setLayout(layout)

    def saveMapping(self):
        mapping_df = self.table_model.df
        mapping_df.to_excel('parameter_mapping.xlsx', index=False)
        QtWidgets.QMessageBox.information(self, 'Saved', 'Mapping saved to parameter_mapping.xlsx')

        # Create VarSet in FreeCAD
        self.view_model.save_mapping(mapping_df)
        QtWidgets.QMessageBox.information(self, 'VarSet Created', 'VarSet created and populated with parameters')

def main():
    app = QtWidgets.QApplication(sys.argv)
    spreadsheet_path = QtWidgets.QFileDialog.getOpenFileName(None, 'Open Spreadsheet', '', 'Excel Files (*.xlsx)')[0]
    if spreadsheet_path:
        mapper = ParameterMapper(spreadsheet_path)
        mapper.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()