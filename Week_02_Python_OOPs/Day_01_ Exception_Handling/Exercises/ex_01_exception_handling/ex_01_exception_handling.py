"""
Define what are following exceptions, when to handle, and handle exceptions, below: 
- SyntaxError 
- Exception 
- RuntimeError 
- ValueError 
- TypeError 
- Warning
"""

"""
SyntaxError: Cannot be handled and has to be fixed. Occurs due to a syntax issue in the code.
"""

# my_list = [1, 2, 3, 4

#   File "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/ex_01_exception_handling.py", line 15
#     my_list = [1, 2, 3, 4
#               ^
# SyntaxError: '[' was never closed

"""
Exception: Exceptions are events that interrupt the normal flow/execution of a program. An exception which is not handled during execution of the code is an error.
"""

my_dict = {"a": 1, "b": 2, "c": 2}
# raises KeyError exception which, since not handled results in KeyError
print(my_dict["d"])
print("After accessing my_dict.")  # control never reaches here

# Traceback (most recent call last):
#   File "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/ex_01_exception_handling.py", line 27, in <module>
#     print(my_dict["d"])
# KeyError: 'd'

my_dict = {"a": 1, "b": 2, "c": 2}
# try block is used to around code which may raise an exception
try:
    print(my_dict["d"])
# except is where control goes if an exception is encountered in the try block
except:
    print("Invalid Key.")
# control reaches here after try is executed and except handles the exception (if any)
print("After accessing my_dict.")

# Invalid Key.
# After accessing my_dict.

"""
RuntimeError: Runtime errors are errors which are encountered during the runtime i.e. execution of the program, after compilation.
"""

student_marks = [60, 70, 80, 95, 96]
class_average = sum(student_marks) / len(student_marks)
print(class_average)  # 80.2

student_marks = []
class_average = sum(student_marks) / len(student_marks)
print(class_average)

# Traceback (most recent call last):
#   File "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/tempCodeRunnerFile.py", line 2, in <module>
#     class_average = sum(student_marks) / len(student_marks)
# ZeroDivisionError: division by zero

student_marks = []

if student_marks:
    class_average = sum(student_marks) / len(student_marks)
    print(class_average)
else:
    print("No student marks entered.")

student_marks = []

try:
    class_average = sum(student_marks) / len(student_marks)
    print(class_average)
except:
    print("No student marks entered.")

"""
We see that what can be done through try-except can technically be done using conditional statements - however thinking of every possible way our code might break will sacrifice readability (due to variouse if-else trees) and time. We follow the principle of "Cure is Better than Prevention" i.e. let the exception occur and then handle it.
"""

"""
TypeError: Raised when an operation or function is applied to an object of inappropriate type.
"""

a = 4
b = 6

a + b  # works as expected

a = 4
b = "abc"
a + b  # TypeError exception.


a = 4
b = "abc"
try:
    print(a + b)
except TypeError:
    print("Invalid operation between int and str.")


"""
ValueError: Python raises a ValueError exception if a function receieves a value of the correct but type but not appropriate in the context.
"""

my_val = float("1")
print(my_val)  # 1.0

my_val = float("one")
print(my_val)  # ValueError

# Traceback (most recent call last):
#   File "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/tempCodeRunnerFile.py", line 1, in <module>
#     my_val = float("one")
# ValueError: could not convert string to float: 'one'

# A ValueError exception is encountered since while we have entered the right data i.e. str float() expects a string consisting of only numeric values and/or decimal points.

try:
    my_val = float("one")
except:
    print("Invalid argument for float.")

"""
Warning: Program continues to run but shows a message. [Documentation] Warning messages are typically issued in situations where it is useful to alert the user of some condition in a program, where that condition (normally) doesn’t warrant raising an exception and terminating the program. For example, one might want to issue a warning when a program uses an obsolete module.
"""

import warnings

warnings.warn("Deprecated module.")  # example of user warnings

# /home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/tempCodeRunnerFile.py:3: UserWarning: Deprecated module.
#   warnings.warn("Deprecated module.")
