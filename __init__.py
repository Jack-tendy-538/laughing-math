import builtins
from typing import Callable
from random import random

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
def arrangement(m:int, n:int):
    """
    Calculates the number of arrangements of m items taken n at a time.
    
    :param m: Total number of items.
    :param n: Number of items to arrange.
    :return: The number of arrangements.
    """
    if m < n:
        return 0
    return factorial(m) // factorial(m - n)

def combination(m:int, n:int):
    """
    Calculates the number of combinations of m items taken n at a time.
    
    :param m: Total number of items.
    :param n: Number of items to choose.
    :return: The number of combinations.
    """
    if m < n:
        return 0
    return factorial(m) // (factorial(n) * factorial(m - n))

def permutation(m:int, n:int):
    """
    Calculates the number of permutations of m items taken n at a time.
    
    :param m: Total number of items.
    :param n: Number of items to permute.
    :return: The number of permutations.
    """
    if m < n:
        return 0
    return factorial(m) // factorial(m - n)

C, A , P = combination, arrangement, permutation

def stirling(m: int, n: int):
    if m < n:
        return 0
    if n == 0:
        return 1 if m == 0 else 0
    return n * stirling(m - 1, n) + stirling(m - 1, n - 1)


class discreteRV(dict):
    """
    A class representing a discrete random variable with methods to calculate
    its probability distribution and mean, variance.
    Inherits from the built-in dict class.
    the keys are the values, and the values are the frequencies.
    """
    def dip(self):
        """
        Returns the probability distribution as a list of tuples (value, probability).
        
        :return: List of tuples representing the probability distribution.
        """
        total = sum(self.values())
        return [(k, v / total) for k, v in self.items()]
    
    def get_choice(self):
        p = random()
        for k, v in self.dip():
            p -= v
            if p <= 0:
                return k
    
    def mean(self):
        """
        Calculates the mean (expected value) of the discrete random variable.

        :return: The mean value.
        """
        total = sum(self.values())
        return sigma(list(self.items()), lambda kv: kv[0] * kv[1] / total)
    
    def variance(self):
        """
        Calculates the variance of the discrete random variable.
        
        :return: The variance value.
        """
        mean_value = self.mean()
        return sigma(list(self.items()), lambda kv: kv[1] * (kv[0] - mean_value) ** 2)
    
    def stddev(self):
        """
        Calculates the standard deviation of the discrete random variable.
        
        :return: The standard deviation value.
        """
        return self.variance() ** 0.5
    
    def __repr__(self):
        return f"discreteRV({super().__repr__()})"
    
    def possibility_between(self, low, high,low_inclusive=True, high_inclusive=True):
        """
        Calculates the probability of the random variable falling between two values.
        
        :param low: The lower bound.
        :param high: The upper bound.
        :param low_inclusive: Whether to include the lower bound in the range.
        :param high_inclusive: Whether to include the upper bound in the range.
        :return: The probability of the random variable falling between the bounds.
        """
        total = sum(self.values())
        if low_inclusive and high_inclusive:
            return sum(v for k, v in self.items() if low <= k <= high) / total
        elif low_inclusive and not high_inclusive:
            return sum(v for k, v in self.items() if low <= k < high) / total
        elif not low_inclusive and high_inclusive:
            return sum(v for k, v in self.items() if low < k <= high) / total
        else:
            return sum(v for k, v in self.items() if low < k < high) / total

def two_point_dist(p:float):
    """
    Creates a two-point discrete random variable with probabilities p and 1-p.
    
    :param p: Probability of the first outcome (0).
    :return: A discreteRV instance representing the two-point distribution.
    """
    if not (0 <= p <= 1):
        raise ValueError("Probability must be between 0 and 1.")
    return discreteRV({0: p, 1: 1 - p})

def binomial_dist(n:int, p:float):
    """
    Creates a binomial discrete random variable with parameters n and p.
    
    :param n: Number of trials.
    :param p: Probability of success on each trial.
    :return: A discreteRV instance representing the binomial distribution.
    """
    if not (0 <= p <= 1):
        raise ValueError("Probability must be between 0 and 1.")
    rv = discreteRV()
    for k in range(n + 1):
        rv[k] = C(n, k) * (p ** k) * ((1 - p) ** (n - k))
    return rv

def hypergeometric_dist(N:int, K:int, n:int):
    """
    Creates a hypergeometric discrete random variable with parameters N, K, and n.
    
    :param N: Total number of items.
    :param K: Total number of successful items.
    :param n: Number of items drawn.
    :return: A discreteRV instance representing the hypergeometric distribution.
    """
    if not (0 <= K <= N) or not (0 <= n <= N):
        raise ValueError("Invalid parameters for hypergeometric distribution.")
    rv = discreteRV()
    for k in range(max(0, n - (N - K)), min(n, K) + 1):
        rv[k] = (C(K, k) * C(N - K, n - k)) / C(N, n)
    return rv

B, h= binomial_dist, hypergeometric_dist

###### TACKLE YOUR ISSUE HERE######
def question_1(n: int, m: int, k: int):
    """
    解答问题：从 n 个产品中有 m 个次品，现要选出 k 个次品，且每次抽取后放回（有放回抽样）。
    问：选出 k 个次品有多少种情况？

    参数说明：
        n: 总产品数量
        m: 次品数量（m <= n）
        k: 需要选出的次品数量

    问题分析：
    - 这是有放回抽样，所以每次抽完都放回，总体数量不变。
    - 我们关注选中的次品数为 k 的组合方式。
    - 需要考虑 k 的取值范围，以及特殊边界情况。

    处理思路：
        1. 若 m <= k < m-n：在该区间，不可能选出超过所有次品的数量，所以情况数为0。
        2. 若 k >= m-n：最多能选出 m-n 个次品，超出部分无法实现，需特殊处理。
        3. 其他情况，按照组合数和排列数公式计算。

    返回值：
        返回选出 k 个次品的所有可能情况数。
    """

    # 检查参数合法性
    if m < 0 or n < 0 or k < 0 or m > n:
        raise ValueError("参数不合法：请确保 0 <= m <= n，且 n, m, k 均为非负整数。")

    # 情况1：k 的范围小于可选的次品数，直接返回0（无解）
    if m <= k < m-n:
        # 此处无解，因为选出的次品数超出实际可选的次品
        return 0

    # 情况2：k 大于等于 m-n（可选次品的最大数），需特殊处理
    elif k >= m-n:
        # 只考虑最多能选出的次品数量 m-n
        k = m-n

        # 计算方式：
        # 用 sigma 累加每个可能的 r（次品被选到的次数），
        # 其中 m^(k+1) 代表所有可能的排列方式，C(r-m, r-n) 是组合数，~int(r-1) 是阶乘（排列数）
        # 还有一种特殊情况，直接加上 ~(m-n)（如果前面抽出来的全都是正品，那么没抽到的全都是次品）
        return m * sigma(m ^ (k + 1), lambda r: C(r - m, r - n) * ~int(r - 1)) + ~(m - n)

    # 情况3：其他情况，按照组合和排列公式计算
    else:
        # 标准的组合加排列计算
        return m * sigma(m ^ (k + 1), lambda r: C(r - m, r - n) * ~int(r - 1))

###### END OF ISSUE######

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




