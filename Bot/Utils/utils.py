def load_class(full_class_string):
    """
    dynamically load a class from a string
    """
    from importlib import import_module
    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)
