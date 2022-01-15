"""
Created on Sunday 13th Aug 2017

@author : Hao Zhaojun

"""


def ergo(m, k, g):
    """function to caculate the probability to pass at least g states when 
    We uniformly randomly jump onto a state amongs m kind of stateseach time.
    After k times jumps, how possible are we to pass at least g states ?

    Args:
        m(int) :- 全部可能状态的数目
        k(int) :- 有放回的抽取的次数
        g(int) :- 要经历的状态的最小数目
        m <= k, k>2
    Returns
        n(int) :- the possibility multplied by m**k 
    """
    liste = [i for i in range(m)]
    SS = [[a, b] for a in liste for b in liste]

    for i in range(k - 2):
        SS = [a + [b] for a in SS for b in liste]

    # n 纪录符合要求的状态的数目	
    n = 0
    for i in SS:
        if len(set(i)) >= g:
            n += 1
    return n
