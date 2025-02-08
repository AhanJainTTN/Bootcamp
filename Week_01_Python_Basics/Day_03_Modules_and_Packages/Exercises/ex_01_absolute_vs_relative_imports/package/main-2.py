from package.greetings_en import say_hello as say_hello_en_abs
from package.subpackage.greetings_de import say_hello as say_hello_de_abs

name = "Ahan"

print(f"Hello in English: {say_hello_en_abs(name)}")
print(f"Hello in Deutsch: {say_hello_de_abs(name)}")
