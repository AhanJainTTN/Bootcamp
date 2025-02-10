Exception Handling


An exception which is not handled during execution of the code is an error.

[Source: https://realpython.com/python-built-in-exceptions/#errors-and-exceptions-in-python] You can fix errors, but you can’t handle them. In other words, if you have a syntax error like the one in the example, then you won’t be able to handle that error and make the code run. You need to correct the syntax.

On the other hand, exceptions are events that interrupt the execution of a program. As their name suggests, exceptions occur in exceptional situations that should or shouldn’t happen. So, to prevent your program from crashing after an exception, you must handle the exception with the appropriate exception-handling mechanism.

Exeception handling primarily is used to make handling abnormal/unexpected behaviour more convenient while maintaining readibility.

Ex:

a = 4
b = 6

a + b # works as expected

However, if b = 'abc' then this raises a TypeError exception.

We see that even though this code is syntactically correct, it still raises a TypeError exception i.e. since this exception was not handled using try-catch during code execution, it raised an error.

