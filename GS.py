# -*- coding: utf8 -*-
"""
Created on Jul 04, 2023

@author: woshihaozhaojun@sina.com
"""
import math
from functools import reduce
from collections import deque
from heapq import (
    heapify, heappop, heappush
)


def pref_to_rank(pref):
    return {
        a: {b: idx for idx, b in enumerate(a_pref)}
        for a, a_pref in pref.items()
    }


def gale_shapley(A, B, A_pref, B_pref):
    """Create a stable matching using the
    Gale-Shapley algorithm.

    Args:
        A(set): customer list
        B(set): banker list
        A_pref(dict[str, list[str]]): customer preference list
        B_pref(dict[str, list[str]]): banker preference list

    Return:
        list of (a, b) pairs.
    """
    B_rank = pref_to_rank(B_pref)
    ask_list = {a: deque(bs) for a, bs in A_pref.items()}
    pair = {}
    remaining_A = set(A)

    while len(remaining_A) > 0:
        a = remaining_A.pop()
        b = ask_list[a].popleft()
        if b not in pair:
            pair[b] = a
        else:
            a0 = pair[b]
            b_prefer_a0 = B_rank[b][a0] < B_rank[b][a]
            if b_prefer_a0:
                remaining_A.add(a)
            else:
                remaining_A.add(a0)
                pair[b] = a

    return [(a, b) for b, a in pair.items()]


def multiply_banker(bankers: list, banker_capacity: dict):
    return reduce(lambda x, y: x + y, [[b] * banker_capacity[b] for b in bankers])


def gale_shapley_1vn(custs, bankers, cust_pref, banker_pref, banker_capacity=None):
    """Create a stable matching using the Gale-Shapley algorithm and allowing for the capacity of each b

    一键肯定的话，可以init_pair和remaining_cust;
    一键否定怎么办?

    Args:
        custs(set): customer list
        bankers(set): banker list
        cust_pref(dict[str, list[str]]): customer preference list
        banker_pref(dict[str, list[str]]): banker preference list
        banker_capacity(dict[str, int]): banker capacity, how many customers each banker is able to serve

    Return:
        list of (cust, b) pairs.
    """
    if banker_capacity is None:
        split_evenly = math.ceil(len(custs) / len(bankers))
        banker_capacity = {b: split_evenly for b in bankers}

    B_rank = pref_to_rank(banker_pref)
    ask_list = {cust: deque(multiply_banker(bs, banker_capacity)) for cust, bs in cust_pref.items()}
    pair = {}
    remaining_cust = set(custs)

    while remaining_cust:
        cust = remaining_cust.pop()
        b = ask_list[cust].popleft()
        if b not in pair:
            pair[b] = [cust]
        elif len(pair[b]) < banker_capacity[b]:
            pair[b].append(cust)
        else:
            for cust0 in pair[b]:
                b_prefer_cust = B_rank[b][cust0] > B_rank[b][cust]
                if b_prefer_cust:
                    pair[b].remove(cust0)
                    pair[b].append(cust)
                    remaining_cust.add(cust0)
                    break
            else:
                remaining_cust.add(cust)

    return [(cust, b) for b, cust in pair.items()]


def gale_shapley_1vn_heap(custs, bankers, cust_pref, banker_pref, banker_capacity=None):
    """Create a stable matching using the Gale-Shapley algorithm and allowing for the capacity of each b

    Args:
        custs(set): customer list
        bankers(set): banker list
        cust_pref(dict[str, list[str]]): customer preference list
        banker_pref(dict[str, list[str]]): banker preference list
        banker_capacity(dict[str, int]): banker capacity, how

    Return:
        list of (cust, b) pairs.
    """
    if banker_capacity is None:
        split_evenly = math.ceil(len(custs) / len(bankers))
        banker_capacity = {b: split_evenly for b in bankers}

    B_rank = pref_to_rank(banker_pref)
    ask_list = {cust: deque(multiply_banker(bs, banker_capacity)) for cust, bs in cust_pref.items()}
    pair = {}
    remaining_cust = set(custs)

    while remaining_cust:
        cust = remaining_cust.pop()
        b = ask_list[cust].popleft()
        rank = -B_rank[b][cust]
        if b not in pair:
            pair[b] = [(rank, cust)]
            heapify(pair[b])
        elif len(pair[b]) < banker_capacity[b]:
            heappush(pair[b], (rank, cust))
        elif rank > pair[b][0][0]:  # 比堆顶的客户排位高
            dumped = heappop(pair[b])[-1]
            heappush(pair[b], (rank, cust))
            remaining_cust.add(dumped)
        else:
            remaining_cust.add(cust)

    return [(cust, b) for b, cust in pair.items()]