"""
Created on Thu July 14:35 2017

Author : HAO zhaojun
"""

# the function to optimise the order of matrix multiplication
# input  : an array of matrix dimension, ith and (i+1)th represent the nth matrice dimension 
# output : two matrix M and P
#          M counts the number of multiplication at element level, its (i,j) element represents the number of multiplication between ith matrice and jth matrice 
#          P records the index of left matrice in last multiplication, its (i,j) element represents the index of left matrice in last multiplication between ith matrice and jth matrice
def MatMulOrder(D):
	num = len(D)-1
	print("There are %d matrix to multiply" %num )  
	M = [ [0 for i in range(num)] for j in range(num) ]
	P = [ [0 for i in range(num)] for j in range(num) ]
	for l in range(2,num+1):
		for i in range(num-l+l):
			for j in range(i+1,i+l):
				M[i][j]= 100000000
				for k in range(i,j) :
					new = M[i][k]+M[k+1][j]+D[i]*D[k+1]*D[j+1]
					if(new < M[i][j]):
						M[i][j] = new
						P[i][j] = k+1
	return(M,P)
						
						
						
	