"""
when run as a script from anywhere, absolute imports work without any modification to sys.path
this is because parent_main parent directory is automatically added to sys.path which can resolve import paths directly as below
"""

# import sys

# print(f"\nsys.path: {sys.path}")

# from parent_module import say_hello as say_hello_parent_abs
# from package.package_module import say_hello as say_hello_pkg_abs
# from package.subpackage.subpackage_module import say_hello as say_hello_subpkg_abs

# print(say_hello_parent_abs(name="Ahan"))
# print(say_hello_pkg_abs(name="Ahan"))
# print(say_hello_subpkg_abs(name="Ahan"))

# print("")

# PS C:\Users\Ahan\Documents\GitHub\Bootcamp> & C:/Users/Ahan/AppData/Local/Programs/Python/Python312/python.exe c:/Users/Ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_03_Modules_and_Packages/Exercises/ex_01_absolute_vs_relative_imports/parent_main.py

# sys.path: ['c:\\Users\\Ahan\\Documents\\GitHub\\Bootcamp\\Week_01_Python_Basics\\Day_03_Modules_and_Packages\\Exercises\\ex_01_absolute_vs_relative_imports', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\DLLs', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages']

# Hello, Ahan from parent/parent_module
# Hello, Ahan from parent/package/package_module
# Hello, Ahan from parent/package/subpackage/subpackage_module

"""
however if we try to run this same script using -m flag from anywhere other than parent directory of parent_main, we will fail because this time the directory we are running the script from i.e. the current working directory gets added
to sys.path instead of residing directory
"""

# PS C:\Users\Ahan\Documents\GitHub\Bootcamp> & C:/Users/Ahan/AppData/Local/Programs/Python/Python312/python.exe -m Week_01_Python_Basics.Day_03_Modules_and_Packages.Exercises.ex_01_absolute_vs_relative_imports.parent_main

# sys.path: ['C:\\Users\\Ahan\\Documents\\GitHub\\Bootcamp', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\DLLs', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages']

# Traceback (most recent call last):
#   File "<frozen runpy>", line 198, in _run_module_as_main
#   File "<frozen runpy>", line 88, in _run_code
#   File "C:\Users\Ahan\Documents\GitHub\Bootcamp\Week_01_Python_Basics\Day_03_Modules_and_Packages\Exercises\ex_01_absolute_vs_relative_imports\parent_main.py", line 8, in <module>
#     from parent_module import say_hello as say_hello_parent_abs
# ModuleNotFoundError: No module named 'parent_module'

"""
if we explicitly add the parent directory to sys.path, this code will run when with -m flag
"""
import sys

sys.path.append(
    "C:\\Users\\Ahan\\Documents\\GitHub\\Bootcamp\\Week_01_Python_Basics\\Day_03_Modules_and_Packages\\Exercises\\ex_01_absolute_vs_relative_imports"
)

print(f"\nsys.path: {sys.path}")

from parent_module import say_hello as say_hello_parent_abs
from package.package_module import say_hello as say_hello_pkg_abs
from package.subpackage.subpackage_module import say_hello as say_hello_subpkg_abs

print(say_hello_parent_abs(name="Ahan"))
print(say_hello_pkg_abs(name="Ahan"))
print(say_hello_subpkg_abs(name="Ahan"))

print("")

# PS C:\Users\Ahan\Documents\GitHub\Bootcamp> & C:/Users/Ahan/AppData/Local/Programs/Python/Python312/python.exe -m Week_01_Python_Basics.Day_03_Modules_and_Packages.Exercises.ex_01_absolute_vs_relative_imports.parent_main

# sys.path: ['C:\\Users\\Ahan\\Documents\\GitHub\\Bootcamp', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\DLLs', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312', 'C:\\Users\\Ahan\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages']

# __package__: Week_01_Python_Basics.Day_03_Modules_and_Packages.Exercises.ex_01_absolute_vs_relative_imports

# Hello, Ahan from parent/parent_module
# Hello, Ahan from parent/package/package_module
# Hello, Ahan from parent/package/subpackage/subpackage_module

"""
Conclusion: "For absolute imports to work, the module's import path must be relative to one of the directories listed in sys.path.
"""
