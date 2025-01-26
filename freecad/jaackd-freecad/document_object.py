import FreeCAD
import logging

logger = logging.getLogger(__name__)

def copy_selected_objects(target_doc, objects_to_copy):
    """
    Copy selected objects to the target document.

    Args:
        target_doc: The target FreeCAD document.
        objects_to_copy: List of objects to copy.
    """
    try:
        target_doc.copyObject(objects_to_copy, True)
        target_doc.recompute()
        return True
    except Exception as e:
        FreeCAD.Console.PrintError(f"Failed to copy objects: {e}\n")
        return False
    

def get_unique_documents(objects):
    """
    Get a list of unique documents that contain the given objects.

    Args:
        objects: List of FreeCAD objects.

    Returns:
        List of unique FreeCAD documents.
    """
    unique_docs = set()
    for obj in objects:
        doc = obj.Document
        unique_docs.add(doc)
    return list(unique_docs)    

def have_unsaved_changes(documents):
    """
    Check if any of the given documents have unsaved changes.

    Args:
        documents: List of FreeCAD documents.

    Returns:
        bool: True if any document has unsaved changes, False otherwise.
    """
    for doc in documents:
        if doc.isTouched():
            return True
    return False