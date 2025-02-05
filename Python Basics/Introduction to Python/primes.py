def is_prime(n):

    # 1 is neither prime nor composite
    # since we are checking for primes, we will simply return false
    if n == 1:
        return False

    for i in range(2, (n // 2) + 1):
        if n % i == 0:
            return False

    return True


n = int(input("Enter a Number: "))
print(is_prime(n))
