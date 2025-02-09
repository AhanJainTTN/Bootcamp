import sys

"""By default, when a script is run directly, only its parent directory is added to sys.path. This means absolute imports will only work for modules in the same directory or its subdirectories. To import modules from higher-level directories, we must explicitly add their paths to sys.path and adjust import statements accordingly."""

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

"""
Conclusion: Without explicitly modifying sys.path, only modules in the same directory or subdirectories can be accessed.
"""
