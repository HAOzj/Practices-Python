# ConfigParser  
从.ini文件中读参数  

### .ini文件格式

[section]  
param=value

### 代码  
```
import Configparser  
config_get = ConfigParser.ConfigParser()  
config_get.read(conf_path)  
val = config_get.get(section, param) # 可以getint,返回的就是int类型  
```

# yaml
从.yaml文件中读数据

### .yaml文件格式

结构通过空格缩进来展示.列表里的项用"-"来代表,字典里的键值对用":"分隔.

```
name: junxi  
age: 18  
spouse:  
    name: Rui  
    age: 18  
children:  
    - name: Chen You  
      age: 3  
    - name: Ruo Xi  
      age: 2  
```

### 代码 

```
import yaml
yaml_conf_dic = yaml.load(open('yaml_example.yaml', 'r'), Loader=yaml.FullLoader))
spouse_name = yaml_conf_dic['spouse']['name']
```

# optparse  
从命令行中读取参数  

### 代码  
```
from optparse import OptionParser  
optparser = OptionParser()  
optparser.add_option('-c', # short option  
  '--conf_path',  # long option  
  action="store", # 默认为store, 也有 store_true, store_false, append, store_const, count, callback等. store_true时, 有这个参数则conf_path=True
  dest='conf_path',  # destination  
  help='参数路径', # 帮助信息  
  type="string", # The argument type expected by this option (e.g., "string" or "int")  
  default="../config/conf.ini"  
)   

(options, args) = optparser.parse_args() # options储存命名参数,比如options.conf_path, args以列表存储剩余的参数
```
### 参考  
https://docs.python.org/2/library/optparse.html

# argparse  
和optparse一样,从命令行读取参数  

### 代码  
```
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("name", type=str)                # positional argument,如果没有赋值则报错
parser.add_argument("-n", "--nmb", action="count")   # key argument, action参考orgparse

group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true") 
group.add_argument("-q", "--quiet", action="store_true")


args = parser.parse_args()
nmb = args.nmb 
```
