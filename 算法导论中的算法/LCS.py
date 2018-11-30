"""
Created on the 11th July 2018

@author : woshihaozhaojun@sina.com
"""
def LCS_bottom_up(A,B):
    '''
    
    Args:
        A, B(iterables) :- 要寻找最长公共子序列的序列
        
    Returns:
        lcs(np.array) :- lcs[i,j]记录A[:i]和B[:j]的最长公共子序列的长度
        record(np.array) :- record[i,j]记录A[:i]和B[:j]的最长公共子序列的递归方式,
                            1表示从lcs[i-1, j]继承
                            2表示从lcs[i, j-1]继承
                            3表示从lcs[i-1, j-1]继承
    '''
    m = len(A)
    n = len(B)
    
    record = np.zeros((m,n))
    lcs = np.zeros((m,n))
    
    lcs[0,0] = 1 if A[0] == B[0] else 0
    record[0, 0] = 3 if A[0] == B[0] else 1
    
    record[0,1] = 2 # 取lcs[i, j-1]
    record[1, 0] = 1 # 取 lcs[i-1, j]
    
    if B[0] in A[:2] :
        if lcs[0, 0] ==1:
            lcs[1,0] = 1
        else:
            lcs[1,0] = 1 
            record[1,0] = 3 # add
    else :
        lcs[1,0] = 0
        
    if A[0] in B[:2] :
        if lcs[0, 0] ==1:
            lcs[0,1] = 1
        else:
            lcs[0,1] = 1
            record[0,1] = 3
    else :
        lcs[0,1] = 0
        
    for i in range(1,m):
        for j in range(1,n):
            if A[i] == B[j]:
                lcs[i,j] = lcs[i-1, j-1] + 1
                record[i, j ] = 3 
            elif lcs[i,j-1] >= lcs[i-1,j] :
                lcs[i,j] =  lcs[i,j-1]
                record[i,j] = 2
            else :
                lcs[i,j] = lcs[i-1,j]
                record[i,j] = 1
                
    subsequence = []
    
    num = 0
    i,j = m-1, n-1
    while num < lcs[m-1,n-1] and i>= 0 and j>= 0:
        if record[i,j] == 3:
            subsequence.append(A[i])
            num += 1
            i -= 1
            j -= 1
        elif record[i,j] == 2 :
            j -= 1
        else :
            i -= 1
    subsequence.reverse()
    print("the longest common subsequence : ",subsequence)
            
    return lcs, record


def LCS_memorized(A, B):
    m = len(A)
    n = len(B)
    
    lcs = dict()
    record = dict()
        
    LCS_memorized_recur(A, B, m-1, n-1, lcs, record)
    
    subsequence = []
    
    num = 0
    i,j = m-1, n-1
    while num < lcs["{}_{}".format(m-1,n-1)] and i>= 0 and j>= 0:
        if record["{}_{}".format(i,j)] == 3:
            subsequence.append(A[i])
            num += 1
            i -= 1
            j -= 1
        elif record["{}_{}".format(i,j)] == 2 :
            j -= 1
        else :
            i -= 1
    subsequence.reverse()
    print("the longest common subsequence : ",subsequence)
    
    return lcs, record
    
        

def LCS_memorized_recur(A,B, i, j, lcs, record):
    '''
    Args:
        A, B(iterables) :- 要寻找最长公共子序列的序列
        
    Returns:
        A[:i+1]和B[:j+1]的最长公共子序列的长度
    '''

    if i == 0 :
        record["{}_{}".format(i,j)] = 2
        if A[i] in B[:j+1]:
            lcs["{}_{}".format(i,j) ] = 1 

            if A[i] == B[j]:
                record["{}_{}".format(i,j)] = 3

            return 1
        else :
            lcs["{}_{}".format(i,j) ] = 0 
            return 0
        
    elif j == 0 :
        record["{}_{}".format(i,j)] = 1
        if B[j] in A[:i+1]:
            lcs["{}_{}".format(i,j) ] = 1 
            if A[i] == B[j]:
                record["{}_{}".format(i,j)] = 3
            return 1
        else :
            lcs["{}_{}".format(i,j) ] = 0 
            return 0        
    
    elif "{}_{}".format(i,j) in lcs:
        return lcs["{}_{}".format(i,j)]
    
    else :
        if A[i] == B[j]:
            lcs["{}_{}".format(i,j) ] = LCS_memorized_recur(A, B, i-1, j-1, lcs, record) + 1
            record["{}_{}".format(i, j) ] = 3 
            return  lcs["{}_{}".format(i,j) ]
            
        else :
            lcs1 = LCS_memorized_recur(A, B, i, j-1, lcs , record)
            lcs2 = LCS_memorized_recur(A, B, i-1, j, lcs, record)
        
            if lcs1 >= lcs2 :
                lcs["{}_{}".format(i,j)] =  lcs1
                record["{}_{}".format(i,j)] = 2

            else :
                lcs["{}_{}".format(i,j)] = lcs2
                record["{}_{}".format(i,j)] = 1

            return lcs["{}_{}".format(i,j)]