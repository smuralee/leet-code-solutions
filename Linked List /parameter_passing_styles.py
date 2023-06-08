# pass by value
from typing import List


def modiylist(b: List):
    print(a)
    print(b)
    print()

    b.append(1)

    print(a)
    print(b)
    print()

    b = [2]
    print(a)
    print(b)
    print()


a = [0]
modiylist(a)


# pass
