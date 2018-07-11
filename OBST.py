"""
Created on the 1th July 2018

@author : woshihaozhaojun@sina.com
"""
def OBST(P,Q):
    ''' 最优二叉搜索树

    Args:
        P(iterables) :- 关键字的概率
        Q(iterables) :- 关键字的间隙的概率

    Returns:
        Exp(dict) :- Exp[i_j]表示i-th关键字到j-th关键字所在的子树的路径长度期望
        Pivot(dict) :- Pivot[i_j]表示i-th关键字到j-th关键字所在的子树的根节点
    '''
    n = len(P)

    try :
        assert len(Q) == n+1
    except AssertionError:
        print("P的长度为{},Q应该长{},但实际长{}".format(
            n, n+1, len(Q)
        )     
        )
    Exp = dict()
    
    Pivot = dict()
    
    for i in range(n,-1,-1):
        Exp["{}_{}".format(i,i-1)] = 0
        Pivot["{}_{}".format(i,i)] = i
        for j in range(i, n):
            
            if i==j:
                Exp["{}_{}".format(i,j)] = P[i] + sum(Q[i:i+2])*2
            else :
                optimum = np.inf
                pivot = i+1
                for k in range(i+1, j+1):
                    new = Exp["{}_{}".format(i,k-1)] + Exp["{}_{}".format(k+1, j)] +  sum(P[i:j+1]) + sum(Q[i:j+2])
                    if optimum > new :
                        optimum = new
                        pivot = k
                Exp["{}_{}".format(i,j)] = optimum
                Pivot["{}_{}".format(i,j)] = pivot

    root = Pivot["{}_{}".format(0, n-1)]
    print("k{}是根".format( root    ))
    
    relation_recur(Pivot,0, root-1, 'l')
    relation_recur(Pivot, root+1, n-1, 'r')
    
                 
    return Exp, Pivot
                
def relation_recur(Pivot, i, j, pos):
    ''' 通过Pivot字典来文字输出树结构
    
    Args:
        Pivot(dict) :- Pivot[i_j]表示i-th关键字到j-th关键字所在的子树的根节点
        i(int) :- 子树包含的最小关键字的索引
        j(int) :- 子树包含的最大关键字的索引
        pos(str) :- i-th到j-th关键所在的子树相对上级子树的位置,
                    choices =["l", "r"]
    '''
    if j-i >= 0:
        pivot = Pivot["{}_{}".format(i,j)]
        if pos =='r':
            print("k{}的右孩子是k{}".format(i-1, pivot))
        else :
            print("k{}的左孩子是k{}".format(j+1, pivot))
        
        relation_recur(Pivot, i, pivot-1, 'l')
        relation_recur(Pivot, pivot+1, j, 'r')

def main():
    P = [0.15, 0.10, 0.05, 0.10, 0.20] # 5
    Q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10] # 6

    OBST(P, Q)

if __name__ ="__main__":
    main()


    
    