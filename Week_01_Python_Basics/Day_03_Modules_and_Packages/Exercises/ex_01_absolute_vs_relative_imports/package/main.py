import os
import sys

print(f"\nCurrent Working Directory: {os.getcwd()}")

print(sys.path)

sys.path.append(
    "/Users/ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_03_Modules_and_Packages/Exercises/ex_01_absolute_vs_relative_imports"
)

sys.path.append(
    "/Users/ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_03_Modules_and_Packages/Exercises"
)

__package__ = "ex_01_absolute_vs_relative_imports.package"

print(f"\nsys.path: {sys.path}")

print(f"\nPackage: {__package__}")

from greetings_en import say_hello as say_hello_en_abs
from package.greetings_fr import say_hello as say_hello_fr_abs
from package.subpackage.greetings_de import say_hello as say_hello_de_abs

name = "Ahan"
print(f"\nHello in English: {say_hello_en_abs(name)}")
print(f"Hello in French: {say_hello_fr_abs(name)}")
print(f"Hello in German: {say_hello_de_abs(name)}")

from ..greetings_en import say_hello as say_hello_en_rel
from .greetings_fr import say_hello as say_hello_fr_rel
from .subpackage.greetings_de import say_hello as say_hello_de_rel

name = "Ahan"
print(f"\nHello in English: {say_hello_en_rel(name)}")
print(f"Hello in French: {say_hello_fr_rel(name)}")
print(f"Hello in German: {say_hello_de_rel(name)}")

print("")
