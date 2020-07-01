# ValueError: 'userid' is both an index level and a column label, which is ambiguous.

新版本的pandas在index和某一列重名时会造成如上错误,可以用重置index名字来解决

```python
df.index.name = None
```

# columns overlap but no suffix specified: Index(['data2', 'data2'], dtype='object')

两个DF合并时index名字相同造成的,可以通过重命名index来解决


