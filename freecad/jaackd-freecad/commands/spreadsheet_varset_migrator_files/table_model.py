from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex

class TableModel(QAbstractTableModel):
    def __init__(self, df):
        super().__init__()
        self.df = df

    def rowCount(self, parent=QModelIndex()):
        return len(self.df)

    def columnCount(self, parent=QModelIndex()):
        return len(self.df.columns) + 1  # Adding one column for 'Purpose'

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            if index.column() < len(self.df.columns):
                return str(self.df.iloc[index.row(), index.column()])
            else:
                return None
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            if index.column() < len(self.df.columns):
                self.df.iloc[index.row(), index.column()] = value
            else:
                self.df.at[index.row(), 'Purpose'] = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
            return True
        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.df.columns):
                    return self.df.columns[section]
                else:
                    return 'Purpose'
            else:
                return str(section)
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled