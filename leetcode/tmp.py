class Solution:
    def canPartition(self, nums):
        print(nums)
        somme, n = sum(nums), len(nums)
        if somme % 2 == 1:
            return False

        target = somme // 2
        if max(nums) > target:
            return False
        import copy
        arr = copy.deepcopy(nums)
        diff = target

        def backtrack(pos):
            nonlocal diff
            if diff == 0:
                raise StopIteration
            if pos >= n:
                return

            for ele in [nums[pos], 0]:
                if diff >= ele:
                    diff -= ele
                    arr[pos] = ele
                    print(pos, diff, ele)
                    backtrack(pos + 1)
                    arr[pos] = 0
                    diff += ele

        try:
            backtrack(0)
            return False, arr
        except StopIteration:
            return True, arr


def main(nums):
    solution = Solution()
    ans = solution.canPartition(nums)
    print("ans is ", ans)


if __name__ == "__main__":
    import random
    nums = [random.randint(1, 100) for _ in range(10)]
    main(nums)
    main([i for i in range(16)])
