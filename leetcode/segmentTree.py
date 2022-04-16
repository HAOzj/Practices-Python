# -*- coding:utf-8 -*-
"""
Created on Apr 11 2022

@author : woshihaozhaojun@sina.com
"""


def build_tree(nodes, l, r, p, nums):
    if l == r:
        print(f"l is {l}, reach leaf {p} ", nodes)
        nodes[p] = nums[l]
    else:
        mid = (l + r) // 2
        print(f"mid is {mid}, l={l}, r={r}, p={p}")
        build_tree(nodes, l, mid, p * 2 + 1, nums) # build left child
        build_tree(nodes, mid + 1, r, p * 2 + 2, nums)
        nodes[p] = nodes[2 * p + 1] + nodes[2 * p + 2]
        print(f"reach non-leaf node {p} ", nodes)


def build(nums):
    length = len(nums)
    nodes = [None for _ in range(2 * length + 1)]
    import math
    depth = math.ceil(math.log2(length))
    nodes += [0 for _ in range(2 ** depth - length)]
    build_tree(nodes, 0, length, 0, nums)


def main():
    nums = [i for i in range(5)]
    print(nums)
    build(nums)


if __name__ == "__main__":
    main()

