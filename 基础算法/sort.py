"""
Created on 24th Jun, 2018

Author : woshihaozhaojun@sina.com
"""
from termcolor import colored
from math import ceil


def fabonacci(n):
    """获得斐波那契数

    Args:
        n(int) :- 斐波那契数列的序号
    """
    assert type(n) == int
    if n < 2:
        return 1
    else:
        return fabonacci(n-1) + fabonacci(n-2)


def bisect(liste, x, print_flag=False):
    """二分插入

    Args:
         liste(iterables) :- 要插入的列表
         x(digit) :- 要插入的元素
    Returns:
        插入x的新列表
    """
    length = len(liste)
    l = 0
    r = len(liste)-1
    if x > liste[r]:
        liste.append(x)
        r = length
    elif x < liste[l]:
        liste.insert(0, x)
        r = 0
    else:
        while r-l > 1:
            mid = (l+r) // 2
            if liste[mid] > x:
                r = mid
            else:
                l = mid
        liste.insert(r, x)

    if print_flag:
        for i in range(length + 1):
            if i == r:
                print(
                    colored(liste[i], "red"),
                    end=" "
                )
            else:
                print(liste[i], end=" ")
        print("\n")
    return liste


def insert_sort(liste, print_flag=False):
    """插入排序"""
    length = len(liste)
    for i in range(1, length):
        liste[:i+1] = bisect(liste[:i], liste[i], print_flag)


def shell_sort(liste, print_flag=False):
    """希尔排序"""
    length = len(liste)
    
    d = length//2
    
    while d >= 1:
        if print_flag:
            print("d为{}".format(d))
        for i in range(d):
            tmp = liste[i:length:d]
            if print_flag:
                print(f"第{i+1}组间距为d的子列")
            insert_sort(tmp, print_flag)
            liste[i:length:d] = tmp
        d = d//2
        if print_flag:
            print("现在数组变成", liste)


def swap(a, i, j):
    """交换列表中两个元素的位置

    Args:
        a(iterables) :- 列表
        i, j(int) :- 要交换位置的两个元素的索引
    """
    a[i], a[j] = a[j], a[i]


def bubble_sort(liste, print_flag=False):
    """冒泡排序"""
    length = len(liste)
    for i in range(length-1):
        for j in range(length-i-1):
            if liste[j] > liste[j+1]:
                swap(liste, j, j+1)
        if print_flag:
            for k in range(length):
                if k == length-i-1:
                    print(
                        colored(liste[k], "red"),
                        end=" "
                    )
                else:
                    print(liste[k], end=" ")
            print("\n")


def partition(liste, left, right, print_flag):
    """
    以liste[left]为pivot,
    将liste[left:right+1]排成[小于等于pivot的, pivot, 大于pivot的]，
    并给出pivot的索引
    
    left, right分别是元素在列表中的序号
    
    right - left> 0
    """
    pivot = liste[left]
    position_pivot = left
    for i in range(left+1, right+1):
        if liste[i] <= pivot:
            swap(liste, i, position_pivot)
            position_pivot += 1
            swap(liste, i, position_pivot)

    if print_flag:
        print("\n")
        for j in range(len(liste)):
            if j < left or j > right:
                print(liste[j], end=" ")
            elif j == position_pivot:
                print(colored(liste[j], "red"), end=" ")
            else:
                print(colored(liste[j], "green"), end=" ")
        
    return position_pivot
        

def quick_sort_recursive(liste, left, right, print_flag=False):
    """快排的递归"""
    if right > left:  # 这里控制迭代的break
        position_pivot = partition(liste, left, right, print_flag)
        quick_sort_recursive(liste, left, position_pivot-1, print_flag)
        quick_sort_recursive(liste, position_pivot+1, right, print_flag)
    

def quick_sort(liste, print_flag=False):
    """快排"""
    quick_sort_recursive(liste, 0, len(liste)-1, print_flag)


def merge(liste, left, mid,  right, print_flag):
    """归并

    mid - left > 0
    right >= mid
    
    将liste[left: mid]和liste[mid:right+1]进行归并

    """
    list1 = liste[left:mid]
    list2 = liste[mid: right+1]
    
    len1, len2 = len(list1), len(list2)
    
    list3 = []
    while len1 or len2:
        if not list1:
            list3.extend(list2)
            break
        elif not list2:
            list3.extend(list1)
            break
        elif list1[0] <= list2[0]:
            list3.append(list1.pop(0))
        else:
            list3.append(list2.pop(0))

    liste[left:right+1] = list3

    if print_flag:
        print("\n")
        for j in range(len(liste)):
            if j < left or j > right:
                print(liste[j], end=" ")
            else:
                print(colored(liste[j], "green"), end=" ")
            
        
def merge_sort(liste, print_flag=False):
    """归并排序"""
    length = len(liste)
    d = 1
    while d <= length:  # d为要合并的列表的大小
        num2merge = ceil(length/d/2)
        if print_flag:
            print("\n要合并的列表的数量 : {}".format(num2merge))
        for i in range(num2merge):
            merge(
                liste, 
                left=i*2*d, 
                mid=min((i*2+1)*d, length-1),
                right=min((i*2+2)*d-1, length-1),
                print_flag=print_flag
            )
        d *= 2
