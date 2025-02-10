# Exception Handling

## Overview

An exception that is not handled during the execution of the code results in an error. You can fix errors, but you cannot handle them. If you have a syntax error, you must correct the syntax for the code to run.

On the other hand, exceptions are events that interrupt the execution of a program. To prevent your program from crashing after an exception, you must handle the exception using the appropriate exception-handling mechanism. 

Exception handling is primarily used to manage abnormal or unexpected behavior while maintaining readability. 

Source: https://realpython.com/python-built-in-exceptions/#errors-and-exceptions-in-python

---

## Example

```python
a = 4
b = 6
print(a + b)  # Works as expected

b = 'abc'
print(a + b)  # Raises a TypeError exception
```

Even though this code is syntactically correct, it still raises a `TypeError` exception. Since this exception was not handled using `try-except`, it results in an error.

---

## Exception Types and Handling

### 1. SyntaxError

**Definition**: Cannot be handled and has to be fixed. Occurs due to a syntax issue in the code.

#### Example:

```python
# my_list = [1, 2, 3, 4
```

#### Output:

```plaintext
  File "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/ex_01_exception_handling.py", line 15
    my_list = [1, 2, 3, 4
              ^
SyntaxError: '[' was never closed
```

---

### 2. Exception

**Definition**: Exceptions are events that interrupt the normal flow/execution of a program. An exception which is not handled during execution of the code is an error.

#### Example:

```python
my_dict = {"a": 1, "b": 2, "c": 2}
print(my_dict["d"])  # Raises KeyError
print("After accessing my_dict.")  # This line will not execute
```

#### Output:

```plaintext
Traceback (most recent call last):
  File "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/ex_01_exception_handling.py", line 27, in <module>
    print(my_dict["d"])
KeyError: 'd'
```

**Handling the Exception:**

```python
my_dict = {"a": 1, "b": 2, "c": 2}
try:
    print(my_dict["d"])
except KeyError:
    print("Invalid Key.")
print("After accessing my_dict.")
```

#### Output:
```plaintext
Invalid Key.
After accessing my_dict.
```

---

### 3. RuntimeError

**Definition**: Runtime errors are errors which are encountered during the runtime i.e. execution of the program, after compilation.

#### Example (Working Code):

```python
student_marks = [60, 70, 80, 95, 96]
class_average = sum(student_marks) / len(student_marks)
print(class_average)

```

#### Output:
```plaintext
80.2
```

#### Example (ZeroDivisionError):

```python
student_marks = []
class_average = sum(student_marks) / len(student_marks)
print(class_average)  # ZeroDivisionError
```

#### Output:
```plaintext
Traceback (most recent call last):
  File "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/tempCodeRunnerFile.py", line 2, in <module>
    class_average = sum(student_marks) / len(student_marks)
ZeroDivisionError: division by zero
```

**Handling the Exception:**

#### Method 1:

```python
student_marks = []
try:
    class_average = sum(student_marks) / len(student_marks)
    print(class_average)
except ZeroDivisionError:
    print("No student marks entered.")
```

#### Method 2:

```python
student_marks = []
try:
    class_average = sum(student_marks) / len(student_marks)
    print(class_average)
except ZeroDivisionError:
    print("No student marks entered.")
```

We see that what can be done through try-except can technically be done using conditional statements - however thinking of every possible way our code might break will sacrifice readability (due to variouse if-else trees) and time.

---

### 4. ValueError

**Definition**: Raised when a function receives a value of the correct type but inappropriate in context.

#### Example:

```python
my_val = float("1")
print(my_val)  # 1.0

my_val = float("one")  # Raises ValueError
print(my_val)
```

#### Output:

```plaintext
Traceback (most recent call last):
  File "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/tempCodeRunnerFile.py", line 1, in <module>
    my_val = float("one")
ValueError: could not convert string to float: 'one'
```

**Handling the Exception:**

```python
try:
    my_val = float("one")
except ValueError:
    print("Invalid argument for float.")
```

---

### 5. TypeError

**Definition**: Raised when an operation or function is applied to an object of inappropriate type.

#### Example:

```python
a = 4
b = 'abc'
print(a + b)  # Raises TypeError
```

#### Output:

```plaintext
Traceback (most recent call last):
  File "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/tempCodeRunnerFile.py", line 7, in <module>
    a + b  # TypeError exception.
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

**Handling the Exception:**

```python
a = 4
b = "abc"

try:
    print(a + b)
except TypeError:
    print("Invalid operation between int and str.")
```

#### Output:

```plaintext
Invalid operation between int and str.
```

---

### 6. Warning

**Definition**: Program continues to run but shows a message. Warning messages are typically issued in situations where it is useful to alert the user of some condition in a program, where that condition (normally) doesn’t warrant raising an exception and terminating the program. For example, one might want to issue a warning when a program uses an obsolete module. 

Source: https://docs.python.org/3/tutorial/errors.html

#### Example:
```python
import warnings
warnings.warn("Deprecated module.")
```

#### Output:

```plaintext
/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_01_ Exception_Handling/Exercises/tempCodeRunnerFile.py:3: UserWarning: Deprecated module.
  warnings.warn("Deprecated module.")
```

---

## Conclusion

Exception handling using `try-except` prevents programs from crashing. While many issues can be addressed using conditional statements, handling every possible failure case would make the code complex and less readable. 

Instead, we follow the principle of **"Cure is Better than Prevention"** — letting exceptions occur and then handling them appropriately.