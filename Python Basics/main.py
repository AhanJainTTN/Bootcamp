# str = "Hello Python!"
# str_rev = str[::-1]

# print("Original String: ", str)
# print("Reversed String (After Slicing): ", str_rev)
# print("Indexed Character: ", str_rev[0])


# str = "information"
# str_slice = str[2::2]

# print("Original String: ", str)
# print("Sliced String: ", str_slice)


# d1 = {'simple_key':'hello'}
# d2 = {'k1':{'k2':'hello'}}
# d3 = {'k1':[{'nest_key':['this is deep',['hello']]}]}
# d4 = {'k1':[1, 2, {'k2':['this is tricky',{'tough':[1, 2, ['hello']]}]}]}

# print("From d1: ", d1['simple_key'])
# print("From d2: ", d2['k1']['k2'])
# print("From d3: ", d3['k1'][0]['nest_key'][1][0])
# print("From d4: ", d4['k1'][2]['k2'][1]['tough'][2][0])


# list3 = [1,2,[3,4,'hello']]
# print('List Before Modification: ', list3)

# list3[2][2] = 'goodbye'
# print('List After Modification: ', list3)


# list5 = [1, 2, 2, 33, 4, 4, 11, 22, 3, 3, 2]
# set5 = set(list5)

# print(type(set5), set5)


str = 'information'
i_count = 0

for k in str:
    if k == 'i':
        i_count += 1

print('String: ', str)
print('Using Loop: ', i_count)
print('Using str.count()', str.count('i'))
