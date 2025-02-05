import sys

sys.path.append("/home/ahan/Documents/Bootcamp/Python Basics/Modules and Packages")

print(sys.path)

# from package.subpackage.greetings_de import say_hello as say_hello_de
# from package.greetings_en import say_hello as say_hello_en

from .greetings_de import say_hello as say_hello_de
from ..greetings_en import say_hello as say_hello_en


name = "Ahan"

print(f"Hello in English: {say_hello_en(name)}")
print(f"Hello in Deutsch: {say_hello_de(name)}")
