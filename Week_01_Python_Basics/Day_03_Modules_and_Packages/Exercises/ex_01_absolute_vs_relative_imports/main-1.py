from Modules_and_Packages.package.greetings_en import say_hello as say_hello_en_abs
from Modules_and_Packages.package.subpackage.greetings_de import (
    say_hello as say_hello_de_abs,
)
from .package.greetings_en import say_hello as say_hello_en_rel
from .package.subpackage.greetings_de import say_hello as say_hello_de_rel

name = "Ahan"

print(f"Hello in English: {say_hello_en_abs(name)}")
print(f"Hello in Deutsch: {say_hello_de_abs(name)}")
print(f"Hello in English: {say_hello_en_rel(name)}")
print(f"Hello in Deutsch: {say_hello_de_rel(name)}")

"""
The first thing Python will do is look up the name abc in sys.modules. This is a cache of all modules that have been previously imported. If the name isn’t found in the module cache, Python will proceed to search through a list of built-in modules. These are modules that come pre-installed with Python and can be found in the Python Standard Library. If the name still isn’t found in the built-in modules, Python then searches for it in a list of directories defined by sys.path. This list usually includes the current directory, which is searched first. When Python finds the module, it binds it to a name in the local scope. This means that abc is now defined and can be used in the current file without throwing a NameError. If the name is never found, you’ll get a ModuleNotFoundError.
"""

# python3 -m Modules_and_Packages.main works
# from .greetings_en import say_hello as say_hello_en_implicit

# name = "Ahan"
# print(f"Hello in English: {say_hello_en_implicit(name)}")

# python3 -m Modules_and_Packages.main does not work for implicit relative imports
# from greetings_en import say_hello as say_hello_en_implicit

# name = "Ahan"
# print(f"Hello in English: {say_hello_en_implicit(name)}")
