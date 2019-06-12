# 检查工具
- sklearn.utils.check_array   # 对数组,列表,稀疏矩阵等进行有效性确认检查.一般,输入会转化为大于2维的numpy array  

# 距离
- sklearn.metrics.pairwise.euclidean_distances # 类似于scipy.spatial.distance.cdist(X,Y, 'sqeuclidean")
- sklearn.preprocessing.normalize       # 归一化
- sklearn.preprocessing.MaxAbsScaler    # 标准化
- sklearn.preprocessing.StandardScaler  # 不支持稀疏矩阵
- sklearn.gaussian_process import GaussianProcessClassifier # 不能使用稀疏矩阵来训练
