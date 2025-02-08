l1 = [1, 2, 3]
l2 = [4, 5, 6]

# possible
t = (l1, l2)
print(t)

# possible
l1[0] = 4
print(t)

# possible
t[0][0] = 9
print(t)

# possible
t[0].append(11)
print(t)

# possible
t[0].pop()
print(t)

# not possible
# t[0] = [1, 4, 7]

# a list inside a tuple can be modified, however the tuple structure should remain the same i.e. tuple level modifications like adding a new list or modifying an entire list since it is a tuple element is not allowed

# possible
t[0].pop()
print(t)
