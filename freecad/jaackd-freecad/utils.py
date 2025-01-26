def has_interface_methods(obj, interface):
    """
    Check if an object has the methods identified in an interface.

    Args:
        obj: The object to check.
        interface: The interface class with abstract methods.

    Returns:
        bool: True if the object has all methods of the interface, False otherwise.
    """
    for method_name in dir(interface):
        if callable(getattr(interface, method_name, None)) and not method_name.startswith('__'):
            if not callable(getattr(obj, method_name, None)):
                return False
    return True