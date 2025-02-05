import sys

sys.path.append(
    "/Users/ahan/Documents/GitHub/Bootcamp/Python Basics/Modules_and_Packages"
)

print(sys.path)
__package__ = "package.subpackage"
print(__package__)

from package.subpackage.greetings_de import say_hello as say_hello_de_abs
from package.greetings_en import say_hello as say_hello_en_abs
from .greetings_de import say_hello as say_hello_de_rel
from ..greetings_en import say_hello as say_hello_en_rel

name = "Ahan"

print(f"Hello in English: {say_hello_de_abs(name)}")
print(f"Hello in Deutsch: {say_hello_en_abs(name)}")
print(f"Hello in English: {say_hello_de_rel(name)}")
print(f"Hello in Deutsch: {say_hello_en_rel(name)}")


# works: cd "/Users/ahan/Documents/GitHub/Bootcamp/Python Basics/Modules and Packages"
# python -m package.subpackage.not-main
#  - why - This tells Python to treat 'package' as a package, so relative imports will work.
# either add to system path but that remains for duration of python interpreter
# so better to add to PYTHONPATH environment variable for permanent effect
# why do all of this? - because relative imports only work inside a package and cannot be used when running a script Python doesn’t recognize not-main.py as part of a package when executed as a script.
# works - rename not-main.py to __main__.py and python -m package.subpackage - why - __main__.py makes the directory executable as a package, so relative imports are allowed.
# works use __init__.py in every directory to make python recognise package strucutre and treat as package and not folder
# run as script: __package__ == None
# run as package: __package__ == package.subpackage i.e. __package__ Indicates the Package to Which a Module Belongs
# works - explicitly define __package__
# relative imports are relative i.e. they need to know where they are i.e. what package they belong to
# Yes! The value of __package__ depends on how you run the script, not where the script file is physically located.
# When running a script from different directories, the number of levels of nesting required for __package__ and relative imports changes. ex if run from parent of modules and packages - __package__ = "Modules and Packages.package.subpackage"

# works
# import sys

# sys.path.append("/Users/ahan/Documents/GitHub/Bootcamp/Python Basics")

# print(sys.path)

# __package__ = "Modules_and_Packages.package.subpackage"
# print(__package__)

# from Modules_and_Packages.package.subpackage.greetings_de import (
#     say_hello as say_hello_de_abs,
# )
# from Modules_and_Packages.package.greetings_en import say_hello as say_hello_en_abs
# from .greetings_de import say_hello as say_hello_de_rel
# from ..greetings_en import say_hello as say_hello_en_rel

# name = "Ahan"

# print(f"Hello in English: {say_hello_de_abs(name)}")
# print(f"Hello in Deutsch: {say_hello_en_abs(name)}")
# print(f"Hello in English: {say_hello_de_rel(name)}")
# print(f"Hello in Deutsch: {say_hello_en_rel(name)}")
