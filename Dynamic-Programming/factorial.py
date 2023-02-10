def factorial(n:int)->int:

    if n >= 1: 
        return n*factorial(n-1)
    elif n == 0: 
        return 1
    else: 
        raise "input cannot be smaller than 0"

if __name__ == "__main__": 

    input_ = 100
    print(f"The factorial for {input_} is {factorial(input_)}") 

    
