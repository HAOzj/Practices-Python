'''
Created on Sunday 13th Aug 2017

@author : Hao Zhaojun

'''

# m 全部可能状态的数目
# k 有放回的抽取的次数
# g 要经历的状态的最小数目
# m <= k, k>2
def ergo(m,k,g):
	liste = [ i for i in range(m)]
	SS = [[a,b] for a in liste for b in liste]


	for i in range(k-2):
		SS = [ a+[b] for a in SS for b in liste]

	# k 纪录符合要求的状态的数目	
	k = 0
	for i in SS :
		if(len(set(i))>= g):
			k+=1
	return(k)
	
