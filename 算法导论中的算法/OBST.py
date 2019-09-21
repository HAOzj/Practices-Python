"""
Created on the 15th July 2018

@author : woshihaozhaojun@sina.com
"""
import numpy as np


def OBST(P, Q):
    """最优二叉搜索树

    假定我们正在设计一个程序，实现英文文本到法语的翻译。对英语文本中出现的每个单词,
    我们需要查找对应的法语单词。为了实现这些查找操作，
    我们可以创建一棵二叉搜索树,将n个英语单词作为关键字，对应的法语单词作为关联数据。
    由于对文本中的每个单词都要进行搜索，我们希望花费在搜索上的总时间尽量少。
    因为在二叉搜索树中搜索一个关键字需要访问的结点数等于包含关键字的结点的深度加1.
    我们希望文本中频繁出现的单词被置于靠近根的位置.
    而且,文本中的一些单词可能没有对应的法语单词，这些单词根本不应该出现在二叉搜索树中.
    在给定单词出现频率的前提下，如何组织一棵二叉搜索树，使得所有搜索操作访问的结点总数最少?
    这就是最优二叉搜索树问题.

    形式定义如下：
    给定一个n个不同关键字的已排序的序列K=<k1, k2, ..., kn>.
    对每个关键字ki,都有一个概率pi表示其搜索频率。
    有些要搜索的值可能不在K中，因此我们还有n+1个伪关键字,do,d1,...,dn表示不在K中的值.
    d0表示所有小于k1的值,dn表示所有大于kn的值,对i=1,2,...,n-1，伪关键字di表示所有在ki和k i+1 之间的值。
    对每个伪关键字di，都有一个概率qi表示对应的搜索频率.
    每个关键字ki是一个内部节点,而每个伪关键字di是一个叶结点。
    每次搜索要么成功（找到某个关键字ki）要么失败（找到某个伪关键字di）

    Args:
        P(iterables) :- 关键字的概率
        Q(iterables) :- 关键字的间隙的概率

    Returns:
        Exp(dict) :- Exp[i_j]表示i-th关键字到j-th关键字所在的子树的路径长度期望
        Pivot(dict) :- Pivot[i_j]表示i-th关键字到j-th关键字所在的子树的根节点
    """
    n = len(P)

    try:
        assert len(Q) == n+1
    except AssertionError:
        print("P的长度为{},Q应该长{},但实际长{}".format(
            n, n+1, len(Q)
        )     
        )
    exp_map = dict()
    
    pivot_map = dict()
    
    for i in range(n, -1, -1):
        exp_map[f"{i}_{i-1}"] = 0
        pivot_map[f"{i}_{i}"] = i
        for j in range(i, n):
            if i == j:
                exp_map[f"{i}_{j}"] = P[i]
            else:
                optimum = np.inf
                pivot = i+1
                for k in range(i+1, j+1):
                    new = exp_map[f"{i}_{k-1}"] +\
                          exp_map[f"{k+1}_{j}"] +\
                          sum(P[i:j + 1])
                    if optimum > new:
                        optimum = new
                        pivot = k
                exp_map[f"{i}_{j}"] = optimum
                pivot_map[f"{i}_{j}"] = pivot

    root = pivot_map[f"{0}_{n-1}"]
    print(f"k{root}是根")
    
    relation_recur(pivot_map,0, root-1, 'l')
    relation_recur(pivot_map, root+1, n-1, 'r')
                 
    return exp_map, pivot_map


def relation_recur(pivot, i, j, pos):
    """通过Pivot字典来文字输出树结构
    
    Args:
        pivot(dict) :- Pivot[i_j]表示i-th关键字到j-th关键字所在的子树的根节点
        i(int) :- 子树包含的最小关键字的索引
        j(int) :- 子树包含的最大关键字的索引
        pos(str) :- i-th到j-th关键所在的子树相对上级子树的位置,
                    choices =["l", "r"]
    """
    if j-i >= 0:
        pivot = pivot[f"{i}_{j}"]
        if pos == "r":
            print(f"k{i-1}的右孩子是k{pivot}")
        else:
            print(f"k{j+1}的左孩子是k{pivot}")
        
        relation_recur(pivot, i, pivot - 1, 'l')
        relation_recur(pivot, pivot + 1, j, 'r')


def main():
    p = [0.15, 0.10, 0.05, 0.10, 0.20] # 5
    q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10] # 6

    OBST(p, q)


if __name__ == "__main__":
    main()
