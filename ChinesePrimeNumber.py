"""
Created on 06 Aug 2017

@author : HAO Zhaojun
"""

# According to Chinese Prime  Number theory, all numbers that are divisible by the power of 2 over them minus one are prime numbers
# Nevertheless, some numbers which satisfy this condition are not prime numbers

from math import sqrt, pow
from numpy import exp


def is_prime(n):
    """ function to identify prime numbers
    args:
        n(int) :- integer to check
    returns:
        bi(str) :- 'Y" if {n} is prime, 'Y'; otherwise, 'N'
    """
    bi = 'Y'
    for i in range(2, round(sqrt(n))):
        if n % i == 0:
            bi = 'N'
    return bi


def chinese_prime_number(n, m):
    """
    function to identify fake prime numbers according to Chinese Prime Numbers Hypothesis
    display all fake prime numbers in the given range

    args:
        n(int) :- the largest amount of fake prime numbers
        m(int) :- the number boundary
    """
    i = 3
    k = 0
    while i < m and k < n:
        # math.pow has boundary problem
        f = 2 ** (i - 1) - 1
        f = int(f)
        if f % i == 0 and is_prime(i) == 'N':
            k += 1
            print("{0}th Fake Prime Number is {1}".format(k, i))
        i += 2


# main function 
chinese_prime_number(10, 10000)
