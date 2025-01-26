import logging

import FreeCAD

from PySide2.QtWidgets import QDialog

from document_object import copy_selected_objects, get_unique_documents, have_unsaved_changes

class CopyExternalParts:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def GetResources(self):
        return {
            'Pixmap': './resources/icons/copy_parts.svg',  # Path to the icon
            'MenuText': 'Copy Parts',
            'ToolTip': 'Copy parts from an external FreeCAD file into the current file'
        }

    def Activated(self):
        current_doc = FreeCAD.ActiveDocument
        from copy_objects_dialog import CopyObjectsDialog
        dialog = CopyObjectsDialog(object_type="App::Part", include_active_doc=True)
        if dialog.exec_() == QDialog.Accepted:
            objects_to_copy = dialog.get_selected_objects()
            externalDocuments = get_unique_documents(objects_to_copy)
            if have_unsaved_changes(externalDocuments):
                self.logger.error("Cannot copy objects from unsaved documents")
                return
            print(f"Copying objects: {objects_to_copy}")
            print(dir(objects_to_copy))
            copy_selected_objects(current_doc, objects_to_copy) 
            for doc in externalDocuments:
                self.logger.info(f"Closing document: {doc.Name}")
                FreeCAD.closeDocument(doc.Name)    

    def IsActive(self):
        return True