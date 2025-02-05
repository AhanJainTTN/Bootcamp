import package.greetings_en as greetings_en

name = "Ahan"
print(f"Hello in English: {greetings_en.say_hello(name)}")

from importlib import reload

reload(greetings_en)
