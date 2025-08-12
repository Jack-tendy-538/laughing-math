import builtins

originalInt, originalFloat = builtins.int, builtins.float
def sigma(value:list, function):
    """
    Applies a function to each element in the list and returns the sum of the results.
    
    :param value: A list of values to process.
    :param function: A function to apply to each element in the list.
    :return: The sum of the results after applying the function.
    """
    return sum(function(x) for x in value)

# example usage
# result = sigma([1, 2, 3], lambda x: x * 2) #returns 12
def pi(value:list, function):
    """
    Applies a function to each element in the list and returns the product of the results.
    
    :param value: A list of values to process.
    :param function: A function to apply to each element in the list.
    :return: The product of the results after applying the function.
    """
    result = 1
    for x in value:
        result *= function(x)
    return result

# example usage
# result = pi([1, 2, 3], lambda x: x + 2) #returns 18
def quick_range(start, end=None):
    if not end:
        start, end = 1, start
    return list(range(start, end + 1))

def factorial(n:int|float):
    if isinstance(n, float):
        if n!= int(n):
            raise ValueError("Factorial is not defined for non-integer values.")
        return(factorial(int(n)))
    if n < 0:
        return -1
    if n == 0 or n == 1:
        return 1
    return pi(range(2, n + 1), lambda x: x)

class FloatPatcher(float):
    def __invert__(self):
        return factorial(int(self))
    
    def __xor__(self, other):
        return quick_range(int(self), int(other))
    
class IntPatcher(int):
    def __invert__(self):
        return factorial(self)
    
    def __xor__(self, other):
        return quick_range(self, other)
    
def replace_builtins():
    """
    Replaces the built-in int and float types with patched versions.
    """
    global builtins
    builtins.int = IntPatcher
    builtins.float = FloatPatcher

replace_builtins()
# example usage
# result = int(5) ^ 10 # returns [5, 6, 7, 8, 9, 10]
# result = float(5.0) ^ 10.0 # returns [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
# result = float(5.0) ~  # returns 120 (factorial of 5)
def restore_builtins():
    """
    Restores the original built-in int and float types.
    """
    global builtins
    builtins.int = originalInt
    builtins.float = originalFloat

if __name__ == "__main__":
    # Example usage of the patched functions
    print(int(5) ^ 10)  # Output: [5, 6, 7, 8, 9, 10]
    print(float(5.0) ^ 10.0)  # Output: [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    print(~float(5.0))  # Output: 120 (factorial of 5)
    restore_builtins()  # Restore original built-ins if needed