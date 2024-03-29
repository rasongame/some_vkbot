from inspect import isclass, ismodule
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from .BasePlug import BasePlug

# iterate through the modules in the current package
package_dir = str(Path(__file__).resolve().parent)
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if issubclass(type(attribute), BasePlug):
            globals()[attribute_name] = attribute
