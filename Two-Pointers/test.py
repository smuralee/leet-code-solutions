from typing import List

def TwoSum_mock(l:List[int]):
    """calculate the sum of ana array 

    Args:
        l (List[int]): _description_

    Returns:
        _type_: _description_
    """
    return sum(l)

def iterate_tools(l:List[int],times:int)->None:

    """
    Learn how to build nested for loops using recurssion 
    print the number from 1 to end of the list for number of times specified 

    Args:
        l (List[int]): _description_
        times (int): _description_
    """

    for i in range(len(l)):
        print(l[i])
        if times == 1: 
            return TwoSum_mock(l)
        else:
            for num in iterate_tools(l[i+1:],times): 
                print(num)
        times -=1 
            

if __name__ == '__main__': 

    l = [1,2,3,4,5,6]
    times = 2
    print(iterate_tools(l,times))