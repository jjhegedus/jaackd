import os
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import Qt
import FreeCAD

class ObjectModel(QStandardItemModel):
    def __init__(self, object_type=None, parent=None):
        super(ObjectModel, self).__init__(parent)
        self.object_type = object_type
        self.loaded_docs = {}

    def add_object(self, doc_label, obj):
        item = QStandardItem(f"{doc_label}: {obj.Label}")
        item.setData(obj, Qt.UserRole)
        item.setCheckable(True)
        self.appendRow(item)

    def get_selected_objects(self):
        selected_objects = []
        for index in range(self.rowCount()):
            item = self.item(index)
            if item.checkState() == Qt.Checked:
                obj = item.data(Qt.UserRole)
                selected_objects.append(obj)
        return selected_objects

    def load_objects_from_folder(self, folder):
        self.clear()
        object_types = set()
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".FCStd"):
                    file_path = os.path.join(root, file)
                    doc = FreeCAD.open(file_path)
                    self.loaded_docs[file_path] = doc
                    self.load_objects_from_document(doc)
                    object_types.update(obj.TypeId for obj in doc.Objects)
        return sorted(object_types)

    def load_objects_from_document(self, doc):
        for obj in doc.Objects:
            if self.object_type in obj.TypeId:
                self.add_object(doc.Label, obj)

    def unload_documents(self):
        for doc in self.loaded_docs.values():
            FreeCAD.closeDocument(doc.Name)
        self.loaded_docs.clear()