# numpy 
- A[np.newaxis, :],矩阵增加一个维度,for instance, 
```
A = np.array([1,2])
A[np.newaxis,:] # array([[1,2]])  
A[:,np.newaxis] # array([[1],[2]])                      
```

- np.rand.shuffle(a), shuffle一个数组,返回值为空  
- np.reshape,改变矩阵形状  
```
A = np.reshape(A, (新形状)) 
A = tf.reshape(A, [新形状])  
```                
- np.min\max\sum,类似于min\max\sum,不过可以用于多维数组             
- np.argsort(array, axis=-1, kind="quicksort", order=None),返回的是数组值从小到大的索引值.要注意的是,2-d矩阵中numpy中axis=0表示列方向, axis=1表示行方向                                                                  
- np.dtype,定义数据类型,类似c里的结构体,比如 
```
dt = np.dtype([('name', np.str, 16), ('grade', np.float, (2))])  
bulletin = np.array([ ('hzj', (99,99)), ('hsz',(100,100))], dtype=dt)  
```                
- astype, numpy中做数据类型转换时最好用astype
    
## np数据类型(https://docs.scipy.org/doc/numpy/user/basics.types.html):     
        
|    Data type	| Description |
| -----         | --------    |
|     bool_|	Boolean (True or False) stored as a byte|
|  int_|	Default integer type (same as C long; normally either int64 or int32)|
| intc	|Identical to C int (normally int32 or int64)|
|intp|	Integer used for indexing (same as C ssize_t; normally either int32 or int64)|
|int8|	Byte (-128 to 127)|
|int16|	Integer (-32768 to 32767)|
|int32|	Integer (-2147483648 to 2147483647)|
|int64|	Integer (-9223372036854775808 to 9223372036854775807)|
|uint8|	Unsigned integer (0 to 255)|
|uint16|	Unsigned integer (0 to 65535)|
|uint32	|Unsigned integer (0 to 4294967295)|
|uint64	|Unsigned integer (0 to 18446744073709551615)|
|float_	| Shorthand for float64.|
|float16|	Half precision float: sign bit, 5 bits exponent, 10 bits mantissa|
|float32|	Single precision float: sign bit, 8 bits exponent, 23 bits mantissa|
|float64|	Double precision float: sign bit, 11 bits exponent, 52 bits mantissa|
|complex_	|Shorthand for complex128.|
|complex64	|Complex number, represented by two 32-bit floats (real and imaginary components)|
|complex128	|Complex number, represented by two 64-bit floats (real and imaginary components)|
    
    
    
# scipy
## 稀疏矩阵
scipy.sparse.csr_matrix 
- scipy提供了稀疏矩阵的存储方式，当要存储的矩阵稀疏时，用于节省内容  
- 稀疏矩阵有不同的储存格式，比如csr(Compressed Sparse Row Format），就是按照行来存储非零元素，有两种实现方式:  
    1. csr_matrix((data, (row_ind, col_ind)), [shape=(M, N)]), data, row_ind和col_ind满足关系 : a[row_ind[k], col_ind[k]] = data[k].  
     2. csr_matrix((data, indices, indptr), [shape=(M, N)]), 标准的csr_matrix表现方式. 第i行的非零元素的列指数存在indices[indptr[i]:indptr[i+1]]中，对应元素值为data[indptr[i]:indptr[i+1]].   
- reference : https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html 和 https://blog.csdn.net/pipisorry/article/details/41762945                         

## 向量对距离
  scipy.spatial.distance.cdist(XA, XB, metric='euclidean', *args, **kwargs) 
 - Computes distance between each pair of the two collections of inputs.
 - 距离可以自定义,比如距离函数可以自定义,比如
 ```
comic_sim = cdist(comic_matrix, comic_matrix, lambda u, v: np.dot(u, v) / (LA.norm(u) * LA.norm(v)+1))
 ```
