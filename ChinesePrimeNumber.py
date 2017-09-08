'''
Created on 06 Aug 13:21

@author : HAO Zhaojun
'''

# According to Chinese Prime  Number theory, all numbers that are divisible by the power of 2 over them minus one are prime numbers
# Nevertheless, some numbers which satisfy this condition are not prime numbers

from math import sqrt, pow
from numpy import exp

# function to identify prime numbers
# input   : number 
# output  : if the given number is prime, 'Y'; otherwise, 'N'
def isPrime(n):
	bi = 'Y'
	for i in range(2,round(sqrt(n))):
		if(n%i == 0):
			bi = 'N'
	return(bi)
    

# function to identify fake prime numbers according to Chinese Prime Numbers Hypothesis
# input  : the largest amount of fake prime numbers 
#		   the number boundary of fake prime numbers
# output : display all fake prime numbers in the given range
def CPN(n,m):
	i = 3
	k = 0
	while i<m and k<n :
		# math.pow has boundary problem
		f = 2**(i-1)-1
		f = int(f)
		if(f%i == 0 and isPrime(i) == 'N'   ):
			k += 1
			print("{0}th Fake Prime Number is {1}".format(k,i))
		i += 2
		
# main function 
CPN(10, 10000)