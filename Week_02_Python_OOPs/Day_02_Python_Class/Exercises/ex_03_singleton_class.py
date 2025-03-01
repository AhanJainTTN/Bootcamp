"""
Implement a singleton class `Database` that ensures only one instance of the class can be created.
"""


class Database:
    """
    Singleton class to simulate a database connection.
    """

    curr_obj = None

    # all classes inherit form object so passing cls to super() i.e. object class returns a new object of class cls
    def __new__(cls):
        if cls.curr_obj is None:
            cls.curr_obj = super().__new__(cls)
        return cls.curr_obj

    def __init__(self):
        self.db_connect = "<connection_string>"


def main():
    db_1 = Database()
    db_2 = Database()

    # Printing memory addressed using id()
    print(f"Memory Address (db_1): {id(db_1)}")
    print(f"Memory Address (db_2): {id(db_2)}")
    print(f"Same Memory Address: {id(db_1) == id(db_2)}")


if __name__ == "__main__":
    main()
