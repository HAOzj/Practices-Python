# -*- coding:utf-8 -*-
"""
Created on Apr 11 2022

@author : woshihaozhaojun@sina.com
"""


class Node(object):
    def __init__(self, startIndex, endIndex, val):
        self.startIndex, self.endIndex = startIndex, endIndex
        self.l, self.r = None, None
        self.val = val
        self.lazyVal = None


class SegmentTree(object):
    def __init__(self, data):
        self.data = data

    def _build_tree(self, start, end):
        if start == end:
            return Node(start, end, self.data[start])
        

def main():
    nums = [i for i in range(5)]
    print(nums)


if __name__ == "__main__":
    main()

