from io import StringIO


def append_quotechar(item, quotechar):
    return f"{quotechar + item + quotechar}"


def extract_data(obj):
    delimiter = ","
    quotechar = '"'
    return ",".join(
        item if delimiter not in item else append_quotechar(item, quotechar)
        for item in obj.values()
    )


my_dict = {
    "Login email": "mary@example.com",
    "Identifier": "9346",
    "One-time password": "14ju73",
    "Recovery code": "mj9346",
    "First name": "Mary",
    "Last name": "Jenkins",
    "Department": "Engineering, HR",
    "Location": "Manchester",
}

extracted_str = extract_data(my_dict)
print(type(extracted_str))

extracted_file = StringIO(extracted_str)
with extracted_file:
    print(type(extracted_file))
    print(extracted_file.read())
