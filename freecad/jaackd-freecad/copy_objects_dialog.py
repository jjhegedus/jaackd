from PySide2.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QListView, QComboBox, QAbstractItemView, QListWidget, QListWidgetItem
from PySide2.QtCore import Signal
from object_model import ObjectModel
import os, FreeCAD
import logging

class CopyObjectsDialog(QDialog):
    finished = Signal()

    def __init__(self, object_type=None, include_active_doc=False, parent=None):
        super(CopyObjectsDialog, self).__init__(parent)
        self.setWindowTitle("Copy Objects from External Files")

        # Set the default position relative to the parent window
        if parent:
            parent_geometry = parent.geometry()
            x = parent_geometry.right() + 20
            y = parent_geometry.top() + 20
            self.setGeometry(x, y, 600, 400)
        else:
            self.setGeometry(300, 300, 600, 400)

        self.layout = QVBoxLayout(self)

        self.folder_label = QLabel("Selected Projects:")
        self.layout.addWidget(self.folder_label)

        self.projects_list = QListWidget()
        self.layout.addWidget(self.projects_list)

        self.add_folder_button = QPushButton("Add Folder")
        self.add_folder_button.clicked.connect(self.add_folder)
        self.layout.addWidget(self.add_folder_button)

        self.add_project_button = QPushButton("Add Project")
        self.add_project_button.clicked.connect(self.add_project)
        self.layout.addWidget(self.add_project_button)

        self.object_type_label = QLabel("Object Type:")
        self.layout.addWidget(self.object_type_label)

        self.object_type_combo = QComboBox()
        self.layout.addWidget(self.object_type_combo)

        self.objects_view = QListView()
        self.objects_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.layout.addWidget(self.objects_view)

        self.copy_button = QPushButton("Copy Selected Objects")
        self.copy_button.clicked.connect(self.copy_selected_objects)
        self.layout.addWidget(self.copy_button)

        self.selected_folder = None
        self.objects_to_copy = []
        self.object_type = object_type
        self.include_active_doc = include_active_doc

        self.model = ObjectModel(object_type=self.object_type, parent=self.objects_view)
        self.objects_view.setModel(self.model)

        if self.include_active_doc:
            self.model.load_objects_from_document(FreeCAD.ActiveDocument)

        self.logger = logging.getLogger(__name__)

        # Connect the finished signal to the cleanup slot
        self.finished.connect(self.cleanup)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", "C:/p/gh/jjhegedus/jaackd/models")
        if folder:
            self.projects_list.addItem(folder)
            object_types = self.model.load_objects_from_folder(folder)
            self.object_type_combo.addItems(object_types)
            if self.object_type:
                self.object_type_combo.setCurrentText(self.object_type)

    def add_project(self):
        project, _ = QFileDialog.getOpenFileName(self, "Select Project", "C:/p/gh/jjhegedus/jaackd/models", "FreeCAD Files (*.FCStd)")
        if project:
            self.projects_list.addItem(project)
            doc = FreeCAD.open(project)
            self.model.load_objects_from_document(doc)
            object_types = set(obj.TypeId for obj in doc.Objects)
            self.object_type_combo.addItems(sorted(object_types))
            if self.object_type:
                self.object_type_combo.setCurrentText(self.object_type)

    def copy_selected_objects(self):
        self.objects_to_copy = self.model.get_selected_objects()
        self.accept()

    def get_selected_objects(self):
        return self.objects_to_copy

    def cleanup(self):
        self.logger.info("Cleaning up Copy Objects dialog")
        selected_docs = {obj.Document for obj in self.objects_to_copy}
        for index in range(self.projects_list.count()):
            project_path = self.projects_list.item(index).text()
            doc = FreeCAD.getDocument(os.path.basename(project_path).replace('.FCStd', ''))
            if doc and doc not in selected_docs:
                FreeCAD.closeDocument(doc.Name)
        self.model.unload_documents()

    def closeEvent(self, event):
        self.logger.info("Closing Copy Objects dialog")
        self.finished.emit()
        super(CopyObjectsDialog, self).closeEvent(event)