"""
Implement a singleton class `Database` that ensures only one instance of the class can be created.
"""

import sys


class Database:
    curr_obj = None

    def __new__(cls):
        if cls.curr_obj is None:
            cls.curr_obj = super().__new__(cls)
        return cls.curr_obj

    def __init__(self):
        self.db_connect = "<connection_string>"

    @classmethod
    def __delref__(cls):
        cls.curr_obj = None


db_1 = Database()
db_2 = Database()

# Printing memory addressed using id()
print(f"Memory Address (db_1): {id(db_1)}")
print(f"Memory Address (db_2): {id(db_2)}")
print(f"Same Memory Address: {id(db_1) == id(db_2)}")

# print(sys.getrefcount(Database.curr_obj))

del db_1
del db_2

# print(sys.getrefcount(Database.curr_obj))

Database.__delref__()
import gc

gc.collect()

db_1 = Database()
db_2 = Database()

# Printing memory addressed using id()
print(f"Memory Address (db_1): {id(db_1)}")
print(f"Memory Address (db_2): {id(db_2)}")
print(f"Same Memory Address: {id(db_1) == id(db_2)}")

# print(sys.getrefcount(Database.curr_obj))
# print(sys.getrefcount(db_1))
# print(sys.getrefcount(db_2))

# Printing memory addressed using id()
# print(f"Memory Address (db_1): {id(db_1)}")
# print(f"Memory Address (db_2): {id(db_2)}")
# print(f"Same Memory Address: {id(db_1) == id(db_2)}")
