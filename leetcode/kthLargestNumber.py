# -*- coding:utf-8 -*-
"""
Created on Apr 11 2022

@author : woshihaozhaojun@sina.com
"""
import heapq
import random
k = 3


def swap(nums, i, j):
    nums[i], nums[j] = nums[j], nums[i]


def partition(nums, l, r):
    pivot = nums[l]
    print(nums, l, r, pivot)

    while r > l:
        if nums[l + 1] <= pivot:
            swap(nums, l + 1, l)
            l += 1
        else:
            swap(nums, l + 1, r)
            r -= 1
    print(nums)
    return l


def quick_sort_recursive(nums, l, r, topk_flag):
    if r > l:
        if topk_flag and not l <= k <= r:
            return
        pivot = partition(nums, l, r)
        quick_sort_recursive(nums, l, pivot, topk_flag)
        quick_sort_recursive(nums, pivot + 1, r, topk_flag)


def quick_sort(nums, topk_flag=False):
    length = len(nums)
    quick_sort_recursive(nums, 0, length - 1, topk_flag)


def find_topk_by_heapq(nums):
    assert len(nums) >= k, print("makabaka")
    print(nums)
    h = [-num for num in nums[:k]]
    heapq.heapify(h)
    for num in nums[k:]:
        heapq.heappush(h, -num)
        print(h)
        print(-heapq.heappop(h))
    return -heapq.heappop(h)


def main():
    nums = [random.randint(0, 20) for _ in range(10)]
    # quick_sort(nums, True)
    topk = find_topk_by_heapq(nums)
    print(topk)


if __name__ == "__main__":
    main()

