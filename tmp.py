from functools import lru_cache
import time


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


def main():
    # s = Solution()
    # getTime(s.climbStairs)
    # # getTime(s.climbStairsWithoutCache)
    # getTime(s.climb)
    s = Solution1()
    res = s.solveNQueens(2)
    res = s.solveNQueens(2)
    print("res is ", res)


if __name__ == "__main__":
    main()


