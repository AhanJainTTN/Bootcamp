def to_binary(n):

    ans = ""
    
    while (n):
        ans = str(n % 2) + ans
        n = n // 2
    
    return int(ans)

def to_octal(n):
    
    ans = ""
    
    while (n):
        ans = str(n % 8) + ans
        n = n // 8
    
    return int(ans)

hexa_map = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']

def to_hexadecimal(n):
    
    ans = ""
    
    while (n):
        ans = str(hexa_map[n % 16]) + ans
        n = n // 16
    
    return ans

n = int(input("Enter a Number: "))

print("Binary: ", to_binary(n))
print("Octal: ", to_octal(n))
print("Hexadecimal: ", to_hexadecimal(n))