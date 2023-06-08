# update of the variables in a hashmap
hash_map = {
    "1": 1,
    "2": 2,
}

# print(hash_map['1'] )
a = hash_map["1"]

a += 1
# print(hash_map['1'])


# update of vairables in a Node
class Node:
    def __init__(self, val: int, next=None, random=None) -> None:
        self.val = val
        self.next = next
        self.random = random

    def __str__(self) -> str:
        return f"Value {self.val} | Next -> {self.next.val if self.next else None} | Random -> {self.random.val if self.random else None}"


if __name__ == "__main__":
    n5 = Node(1, next=None, random=None)
    n4 = Node(10, next=n5, random=None)
    n3 = Node(11, next=n4, random=None)
    n2 = Node(13, next=n3, random=None)
    n1 = Node(7, next=n2, random=None)

    n1.random = n4
    n2.random = n1
    n3.random = n5
    n4.random = n3
    n5.random = n1

    print("display the original heads")
    for nodes in [n1, n2, n3, n4, n5]:
        print(nodes)
    print()

    print("swapping the random and current pointer")
    curr = n1
    # print(dir(head))
    while curr:
        print(n1)
        curr.next, curr.random = curr.random, curr.next
        print(n1)
        print()
        curr = curr.next

    print("playing with a toy example")
    cur = n1
    print(cur, "//", n1)
    print(cur.next, "//", n1.next)
    print()

    print("Overridding the .next attribute of the cur refernece variable")
    cur.next = Node(
        100,
    )
    print(cur, "//", n1)
    print(cur.next, "//", n1.next)
