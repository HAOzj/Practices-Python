# -*- coding:utf-8 -*-
"""
Created on May 03 2022

@author : woshihaozhaojun@sina.com
"""


class Heap(object):
    def __init__(self, data):
        self.data = data
        self.len = len(data)
        print(data)

    def build_heap(self):
        for i in range(self.len // 2 - 1, -1, -1):
            self._build_heap(i, self.len)

    def _build_heap(self, i, limit):
        max_index = i
        maximum = self.data[i]
        l, r = 2 * i + 1, 2 * i + 2
        if l < limit and self.data[l] > maximum:
            max_index = l
            maximum = self.data[l]
        if r < limit and self.data[r] > maximum:
            max_index = r
        if max_index != i:
            self.swap(self.data, max_index, i)
            self._build_heap(max_index, limit)

    def heap_sort(self):
        for i in range(self.len - 1):
            self.swap(self.data, 0, self.len - i - 1)
            self._build_heap(0, self.len - i - 1)

    @staticmethod
    def swap(data, i, j):
        data[i], data[j] = data[j], data[i]


def main():
    import random
    data = [random.randint(0, 20) for _ in range(10)]
    heap = Heap(data)
    heap.build_heap()
    heap.heap_sort()
    assert sorted(data) == heap.data, print(sorted(data), "\n", heap.data)


if __name__ == "__main__":
    main()