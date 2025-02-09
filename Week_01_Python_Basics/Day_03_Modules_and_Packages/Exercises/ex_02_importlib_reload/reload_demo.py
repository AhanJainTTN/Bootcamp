"""
Explain the use of `from importlib import reload`
"""

# run directly in interpreter
import module_to_reload

print(module_to_reload.say_hello("Ahan"))

# modify module_to_reload.say_hello() to return "Bye, {name}"
# import again
import module_to_reload

# run again - no difference
print(module_to_reload.say_hello("Ahan"))

# use reload from importlib
from importlib import reload

reload(module_to_reload)

# run again - changes reflected
print(module_to_reload.say_hello("Ahan"))

# >>> import module_to_reload
# >>> print(module_to_reload.say_hello("Ahan"))
# Hello, Ahan
# >>> import module_to_reload
# >>> print(module_to_reload.say_hello("Ahan"))
# Hello, Ahan
# >>> from importlib import reload
# >>> reload(module_to_reload)
# <module 'module_to_reload' from '/Users/ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_03_Modules_and_Packages/Exercises/ex_02_importlib_reload/module_to_reload.py'>
# >>> print(module_to_reload.say_hello("Ahan"))
# Bye, Ahan
