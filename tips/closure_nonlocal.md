# 嵌套函数
在python中,可以函数中定义函数.
在函数中的函数叫做nested function,外层的函数叫做enclosed function.

```python
def outerFunc(text):
    def innerFunc():
        print(text)
    innerFunc()


outerFunc("Hola") # Hola
```
当我们不想把数据或者函数暴露的时候,可以使用嵌套函数.

# nonlocal变量
nested function可以使用enclosed function中定义的变量.
正如function可以使用全局变量.
这些变量既不是全局变量又不是本地变量，叫做nonlocal变量.
比如上一段代码中的*text*变量.

```python
def outer(element):
    a = [1, 2]
    def inner():
        a.append(element)
    inner()
    print(a)

outer(2) # [1, 2, 2]
outer(3) # [1, 2, 3]
```

类似于global关键字可以表明变量可以在全局命名空间中寻找,
nonlocal关键字用来表明这个变量不用声明,尤其是对于不可变类型的变量,
可以在enclosed function的命名空间中寻找并重新赋值

```python
a = []
def ajouter(newElement):
    global a 
    a.append(newElement)
    print(a)
ajouter(1) # [1]
ajouter(2) # [1, 2]


def counter():
    i = 0
    def increment():
        nonlocal i # 如果不声明则下一行会报错,因为+= 操作表示 i = i + 1,而increment中并未声明i
        i += 1
        return i 
    return increment

a = counter()
a() # 1 
a() # 2 
```

# closure
closure是闭包,当nested function使用了nonlocal变量,
并且enclosed function返回的是nested function时,nested function叫做closure function.

即使enclosed function或nonlocal被删除(不在当前命名空间中),closure function照样可以读nonlocal变量.
这个机制叫做闭包.

```python
def exponent(n):
    def exponentOf(num):
        return num ** n 
    return exponentOf

square = exponent(2)
cube = exponent(3)
del exponent
square(2) # 4
cube(2) # 8
```

闭包最常见的用法是装饰器.
