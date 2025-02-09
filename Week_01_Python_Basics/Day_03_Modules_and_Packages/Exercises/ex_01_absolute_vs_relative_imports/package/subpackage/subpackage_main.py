"""
Relative imports only work inside a package. This means directly running a file as a script (i.e., python subpackage_main.py) will result in a ModuleNotFoundError. This happens because __package__ is set to None when a script is run directly. This is important because relative imports are resolved based on the package name, which is derived from __package__. sys.path also plays a crucial role in locating modules. When a script is run using the -m flag, the current working directory (CWD) is appended to sys.path instead of the script's parent directory. This ensures that the top-level package is accessible relative to the CWD.

# Folder structure:
root/
│── parent/
│   │── package/
│   │   │── subpackage/
│   │   │   │── subpackage_main.py  # This script is being run

$ cd root/
$ python -m parent.package.subpackage.subpackage_main

This sets __package__ to parent.package.subpackage and all imports in subpackage_main are relative to this.
"""

# import sys

# print(f"\nsys.path: {sys.path}")
# print(f"\n__package__: {__package__}\n")

# from ...parent_module import say_hello as say_hello_parent_rel
# from ..package_module import say_hello as say_hello_pkg_rel
# from .subpackage_module import say_hello as say_hello_subpkg_rel

# print(say_hello_parent_rel(name="Ahan"))
# print(say_hello_pkg_rel(name="Ahan"))
# print(say_hello_subpkg_rel(name="Ahan"))

# print("")

# PS C:\Users\Ahan\Documents\GitHub\Bootcamp\Week_01_Python_Basics\Day_03_Modules_and_Packages\Exercises> python -m ex_01_absolute_vs_relative_importsdul.package.subpackage.subpackage_main

# sys.path: ['C:\\Users\\Ahan\\Documents\\GitHub\\Bootcamp\\Week_01_Python_Basics\\Day_03_Modules_and_Packages\\Exercises', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\DLLs', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages']

# __package__: ex_01_absolute_vs_relative_imports.package.subpackage

# Hello, Ahan from parent/parent_module
# Hello, Ahan from parent/package/package_module
# Hello, Ahan from parent/package/subpackage/subpackage_module


"""
If we want to run subpackage_main.py directly from anywhere, we must explicitly set __package__ to parent.package.subpackage (including as many levels of nesting as needed for imports). Additionally, we must ensure that the parent directory of parent (i.e., the directory containing the top-level package) is added to sys.path.
"""

# import sys

# # top-level package is the highest-level module required for imports - specifying a higher level is unnecessary
# __package__ = "ex_01_absolute_vs_relative_imports.package.subpackage"

# # appending to sys.path explicitly
# sys.path.append(
#     "C:\\Users\\Ahan\\Documents\\GitHub\\Bootcamp\\Week_01_Python_Basics\\Day_03_Modules_and_Packages\\Exercises\\"
# )

# print(f"\nsys.path: {sys.path}")
# print(f"\n__package__: {__package__}\n")

# from ...parent_module import say_hello as say_hello_parent_rel
# from ..package_module import say_hello as say_hello_pkg_rel
# from .subpackage_module import say_hello as say_hello_subpkg_rel

# print(say_hello_parent_rel(name="Ahan"))
# print(say_hello_pkg_rel(name="Ahan"))
# print(say_hello_subpkg_rel(name="Ahan"))

# print("")

# PS C:\Users\Ahan\Documents\GitHub\Bootcamp> & C:/Users/Ahan/AppData/Local/Programs/Python/Python312/python.exe c:/Users/Ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_03_Modules_and_Packages/Exercises/ex_01_absolute_vs_relative_imports/package/subpackage/subpackage_main.py

# sys.path: ['c:\\Users\\Ahan\\Documents\\GitHub\\Bootcamp\\Week_01_Python_Basics\\Day_03_Modules_and_Packages\\Exercises\\ex_01_absolute_vs_relative_imports\\package\\subpackage', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\DLLs', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages', 'C:\\Users\\Ahan\\Documents\\GitHub\\Bootcamp\\Week_01_Python_Basics\\Day_03_Modules_and_Packages\\Exercises\\']

# __package__: ex_01_absolute_vs_relative_imports.package.subpackage

# Hello, Ahan from parent/parent_module
# Hello, Ahan from parent/package/package_module
# Hello, Ahan from parent/package/subpackage/subpackage_module

"""
Implicit relative imports were removed in Python 3 because they caused ambiguity and made code harder to maintain.
"""

import sys

print(f"\nsys.path: {sys.path}")
print(f"\n__package__: {__package__}\n")

# does not work - ModuleNotFoundError
# from subpackage_module import say_hello as say_hello_rel

# print(say_hello_rel(name="Ahan"))

# PS C:\Users\Ahan\Documents\GitHub\Bootcamp\Week_01_Python_Basics\Day_03_Modules_and_Packages\Exercises> python -m ex_01_absolute_vs_relative_imports.package.subpackage.subpackage_main

# sys.path: ['C:\\Users\\Ahan\\Documents\\GitHub\\Bootcamp\\Week_01_Python_Basics\\Day_03_Modules_and_Packages\\Exercises', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\DLLs', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages']

# __package__: ex_01_absolute_vs_relative_imports.package.subpackage

# Traceback (most recent call last):
#   File "<frozen runpy>", line 198, in _run_module_as_main
#   File "<frozen runpy>", line 88, in _run_code
#   File "C:\Users\Ahan\Documents\GitHub\Bootcamp\Week_01_Python_Basics\Day_03_Modules_and_Packages\Exercises\ex_01_absolute_vs_relative_imports\package\subpackage\subpackage_main.py", line 93, in <module>
#     from subpackage_module import say_hello as say_hello_rel
# ModuleNotFoundError: No module named 'subpackage_module'

# works
from .subpackage_module import say_hello as say_hello_rel

print(say_hello_rel(name="Ahan"))

# PS C:\Users\Ahan\Documents\GitHub\Bootcamp\Week_01_Python_Basics\Day_03_Modules_and_Packages\Exercises> python -m ex_01_absolute_vs_relative_imports.package.subpackage.subpackage_main

# sys.path: ['C:\\Users\\Ahan\\Documents\\GitHub\\Bootcamp\\Week_01_Python_Basics\\Day_03_Modules_and_Packages\\Exercises', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\DLLs', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages']

# __package__: ex_01_absolute_vs_relative_imports.package.subpackage

# Hello, Ahan from parent/package/subpackage/subpackage_module


print("")
