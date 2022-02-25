import random

# modular arithmatic


def mod(pr, modulus):

    # if modulus % pr == 0: (inefficient)
    #    return 0
    # else:
    if pr > modulus:
        while pr > modulus:
            pr -= modulus
        return pr
    else:
        while modulus > pr:
            modulus -= pr
        return modulus


my_pr = 3**54
my_num = mod(my_pr, 17)

print(my_num)
print(my_pr)
