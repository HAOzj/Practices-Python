import random
from functools import lru_cache
import time
import cProfile
import pstats
dmp_file = "profiling_tmp.dmp"


class Solution:
    def climb(self, n):
        wayNumArr = [1, 2]
        if n <= 2:
            return wayNumArr[n - 1]
        for i in range(2, n):
            wayNumArr.append(sum(wayNumArr))
            wayNumArr.pop(0)
        return wayNumArr[-1]

    @lru_cache(maxsize=3)
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        return self.climbStairs(n - 1) + self.climbStairs(n - 2)

    def climbStairsWithoutCache(self, n: int) -> int:
        if n <= 2:
            return n
        return self.climbStairsWithoutCache(n - 1) + self.climbStairsWithoutCache(n - 2)


def getTime(func):
    startTime = time.time()
    for i in range(1, 10):
        func(i)
    endTime = time.time()
    print(func.__name__, (endTime - startTime) / 60)


class Solution1:
    def solveNQueens(self, n: int):
        import copy
        def dfs(pos):
            print("pos is ", pos)
            if pos == n:
                print("res is ", res, "current is ", current)
                res.append(copy.copy(current))
            else:
                for j in range(n):
                    forbidden = copy.copy(current)
                    if current:
                        for row, col in enumerate(current):
                            forbidden.append(col - (row - j))
                            forbidden.append(col + (row - j))

                    # print("current is ", current, "j is ", j)
                    if j not in forbidden:
                        current.append(j)
                        # print("append, current becomes ", current)
                        dfs(pos + 1)
                        current.pop()
                    # print("current becomes ", current)
            print("pos = ", pos, " res becomes ", res)

        res, current = [], []
        dfs(0)
        ans = []
        print("solutiones are ", res)
        for solution in res:
            tmp = [["."] * n for _ in range(n)]
            for i, j in enumerate(solution):
                tmp[i][j] = "Q"
            tmp = ["".join(ele) for ele in tmp]
            ans.append(tmp)
        return ans


class CheckDunderBool:
    def __init__(self, nums=None):
        if nums is not None:
            assert isinstance(nums, list), print("nums should be a list")
        self.nums = nums if nums is not None else []
        self.index = 0

    def __repr__(self):
        return "{!r}".format(self.nums)

    def __len__(self):
        return len(self.nums)

    def __getitem__(self, pos):
        return self.nums[pos] if pos < self.__len__() else None

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self):
            self.index += 1
            return self.nums[self.index - 1]
        else:
            # raise StopIteration
            return None
        # return next(iter(self.nums))  # 这样每次都会重新生成generator

    def __iadd__(self, other):
        self.nums.append(other)
        return self

    def __add__(self, other):
        if isinstance(other, list):
            return CheckDunderBool(self.nums + other)
        elif isinstance(other, int):
            return CheckDunderBool(self.nums + [other])
        else:
            print("other should be int or list")


def do_cprofile(filename):
    """
    Decorator for function profiling.
    """
    def wrapper(func):
        def profiled_func(*args, **kwargs):
            profile = cProfile.Profile()
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            # Sort stat by internal time.
            sortby = "tottime"
            ps = pstats.Stats(profile).sort_stats(sortby)
            # ps.print_stats()
            ps.dump_stats(filename)
            return result
        return profiled_func
    return wrapper


def print_dmp_file(file):
    ps = pstats.Stats(file)
    ps.print_stats()


@do_cprofile(dmp_file)
def main():
    # s = Solution()
    # getTime(s.climbStairs)
    # # getTime(s.climbStairsWithoutCache)
    # getTime(s.climb)
    # s = Solution1()
    # res = s.solveNQueens(2)
    # res = s.solveNQueens(2)
    # print("res is ", res)
    from random import choice
    check = CheckDunderBool([0])
    print(bool(check))
    check += 3
    check += 4
    print(repr(check))
    print(choice(check))
    print(list(reversed(check)))

    ele = next(check)
    print("\nstart generator")
    while ele is not None:
        print(ele)
        ele = next(check)

    print(bool(check))
    # print(check[1::2])


def roundrobin(*iterables):
    from collections import deque
    iterators = deque(map(iter, iterables))
    while iterators:
        try:
            while True:
                yield next(iterators[0])
                iterators.rotate(-1)
        except StopIteration:
            iterators.popleft()


def main2():
    [a, b, c] = [familia.split(' ') for familia in ['hzj wbb', 'haoyunyun zhangcheng doudou hehe', 'hyj yinxing']]
    for name in roundrobin(a, b, c):
        print(name)

if __name__ == "__main__":
    # main()
    # print_dmp_file(dmp_file)
    main2()




