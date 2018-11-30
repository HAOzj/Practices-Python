"""
Created on Thu July 14:35 2017

Author : HAO zhaojun
"""
def MatMulOrder(D):
	'''the function to optimise the order of matrix-chain multiplication

	Args :
		input(iterables) :- an array of matrix dimension, 
							ith and (i+1)th represent the ith matrice dimension 
	Returns : 
		M(iterables) :- matrice to record the number of multiplication at element level, 
						its [i][j] element represents the number of scalar multiplication 
						between ith matrice and jth matrice 
		P(iterables) :- matrice to records the index of left matrice in last multiplication, 
						its [i][j] element represents the index of left matrice in last multiplication 
						between ith matrice and jth matrice
	'''
	num = len(D)-1 # number of matrix in the chain
	print("There are %d matrix to multiply" %num )  
	M = [ [0 for j in range(num)] for i in range(num) ] 
	P = [ [0 for j in range(num)] for i in range(num) ]

	for i in range(num-2, -1, -1 ): # i要从大到小
		for j in range(i+1, num): # i == j时, M[i][j]=0,所以不用更新
			M[i][j]= 100000000 # i-th矩阵到j-th矩阵的乘的最优值初始化为inf
			for k in range(i,j) : 
				new = M[i][k] + M[k+1][j] + D[i]*D[k+1]*D[j+1]
				if(new < M[i][j]):
					M[i][j] = new 
					P[i][j] = k
	return(M,P)
						
						
						
	
