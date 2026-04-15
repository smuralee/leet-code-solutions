# Basics
print("Hello world!")

name = "Alice"
print(f"Hello {name}")

MAX_SIZE = 100
print(MAX_SIZE)

# For loop
print("===== For loop =====")
fruits = ["apple", "orange", "banana", "grapes", "tomato"]
for fruit in fruits:
    print(f"Do you want {fruit}?")
for i in range(1, 10):  # last number i.e. 10 is ignored
    print(f"The continuous count is: {i}")
for i in range(1, 10, 2):  # We provide the step increment
    print(f"The step count is: {i}")

# Access via index, with positive and negative index values
print("===== Access list using positive indexes =====")
print(fruits[0])
print(fruits[1])
print(fruits[2])
print("===== Access list using negative indexes =====")
print(fruits[-1])
print(fruits[-2])
print(fruits[-3])

# converts the string into a list
print("===== String to array using list constructor =====")
arr = list("abc")
print(arr)

# Slicing a list, including the first but excluding the last.
print("===== Slice list =====")
print(fruits)
print(fruits[0:3])

# Add items to the list
print("===== Append, extend and copy list =====")
fruits.append("blueberry")
print(fruits)
nuts = ["almonds", "cashew"]
fruits.extend(nuts)
print(fruits)

# While loop
print("===== While loop =====")
count = 1
while count <= 3:
    print(f"The count {count} is <= 3")
    count += 1

# Shallow copy
# A new object/collection is created.
# Any primitive values (like numbers or strings) are copied directly into the new object.
# Any references (like nested lists or objects) are copied as references.
# This means the copy and the original share the same sub-objects.

print("===== Shallow v/s Deep copy =====")
import copy

original = [[1, 2, 3], [4, 5, 6]]
shallow_copy = copy.copy(original)
deep_copy = copy.deepcopy(original)

# Modify the top-level list
shallow_copy.append([7, 8, 9])
deep_copy.append([10, 11, 12])
print(original)
print(shallow_copy)
print(deep_copy)

# Modify the nested object
deep_copy[0][0] = "TICK TICK"
shallow_copy[0][0] = "BOOM"
print(original)
print(shallow_copy)
print(deep_copy)

# List comprehension
print("===== List comprehension =====")
comprehend = [x * 2 for x in range(5)]
print(comprehend)

# Tuples
print("===== Tuples =====")
simple_tuple = (1, 2, 3)
print(simple_tuple)
# Trailing comma is needed, else it's not a tuple
singleton_tuple = (4,)
print(singleton_tuple)
# Convert a list to a tuple
converted_tuple = tuple([5, 6, 7])
print(converted_tuple)
# Unpacking the tuple
first, second, third = converted_tuple
print(f"Unpacked {first} then {second} and {third}")
# Concatenate a tuple
final_tuple = simple_tuple + singleton_tuple + converted_tuple
print(f"Concatenation {final_tuple}")
print(f"Repeated {simple_tuple * 3}")
# Deleting a tuple
del converted_tuple

# Sets, cannot contain lists and dictionaries - unhashable list
# Duplicates removed
demo_set_1 = {"red", "blue", "green", "green"}
demo_set_2 = {"yellow", "red", "orange"}
print(f"Set {demo_set_1}")
print(f"Set with AND operator {demo_set_1 & demo_set_2}")
print(f"Set with OR operator {demo_set_1 | demo_set_2}")
print(f"Set with XOR operator {demo_set_1 ^ demo_set_2}")
# Freeze the given sequence and makes it unchangeable.
frozen_demo_set = frozenset({"red", "green", "blue"})
print(frozen_demo_set)

# Dictionary
demo_dict_1 = {"name": "Adam", "age": "50", "job": "Engineer", "city": "SF"}
print(demo_dict_1)
keys = ["name", "age", "job"]
values = ["Bob", 25, "Engineer"]
demo_dict_2 = dict(zip(keys, values))
print(demo_dict_2)
# Update 1st dictionary with values of 2nd dictionary
demo_dict_1.update(demo_dict_2)
print(f"Update 1st dictionary with values of 2nd dictionary {demo_dict_1}")
# Get all keys and values
print(f"List all keys {demo_dict_1.keys()}")
print(f"List all values {demo_dict_1.values()}")
# Remove elements
demo_dict_1.pop("city")
print(f"Pop specific key {demo_dict_1}")
demo_dict_1.popitem()
print(f"Pop last item {demo_dict_1}")
dict_comprehend = {x: x * 2 for x in range(5)}
print(f"Dictionary comprehension {dict_comprehend}")

# String operations
demo_str = "ABCDEFGHI"
print(f"Remove last character {demo_str[:-1]}")
print("===== String slicing =====")
print(demo_str[2:5])  # Prints CDE
print(demo_str[5:-1])  # Prints FGH
print(demo_str[1:6:2])  # Prints BDF
print(f"Replace string {demo_str.replace('EFGH', 'PQRS')}")
