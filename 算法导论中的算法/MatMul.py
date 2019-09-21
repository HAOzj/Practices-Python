"""
Created on Thu July 14:35 2017

@author: woshihaozhaojun@sina.com
"""


def MatMulOrder(D):
	"""optimise the order of matrix-chain multiplication

	Args:
		D(iterables) :- an array of matrix dimension,
							ith and (i+1)th represent the ith matrix dimension
	Returns:
		M(iterables) :- matrix to record the number of multiplication at element level,
						its [i][j] element represents the number of scalar multiplication 
						between ith matrix and jth matrix
		P(iterables) :- matrix to records the index of left matrix in last multiplication,
						its [i][j] element represents the index of left matrix in last multiplication
						between ith matrix and jth matrix
	"""
	num = len(D)-1 # number of matrix in the chain
	print(f"There are {num} matrix to multiply")
	M = [[0 for _ in range(num)] for _ in range(num)]
	P = [[0 for _ in range(num)] for _ in range(num)]

	# i要从大到小
	# i == j时, M[i][j]=0,所以不用更新
	# i-th矩阵到j-th矩阵的乘的最优值初始化为inf
	for i in range(num-2, -1, -1):
		for j in range(i+1, num):
			M[i][j] = 100000000
			for k in range(i, j):
				new = M[i][k] + M[k+1][j] + D[i]*D[k+1]*D[j+1]
				if new < M[i][j]:
					M[i][j] = new 
					P[i][j] = k
	return M, P
