# pip安装
pip install psycopg2-binary

# 连接客户端

- 和mysql, hive类似,只是 password的变量名不同
- 同样可以用 pandas来获取df
```python3
import psycopg2
import pandas as pd


class PG:
    def __init__(self, yaml_conf_dic, section):
        """打开mysql数据库连接

        yaml_conf_dic写法举例:
        {
            "mysql":
                "Host": "xxxx",
                "Port": "3306",
                "User": "recommend",
                "Password": "xxx",
                "Db_name": "samh_recommender",
                "Table_name:{
                    "Dest": "correlative_new"
                }
        }

        Args:
            yaml_conf_dic(dict) :- 配置的字典
            section(str)        :- mysql连接配置块所在的字段
        """
        self.db = psycopg2.connect(host=yaml_conf_dic[section]['Host'],
                                  user=yaml_conf_dic[section]['User'],
                                  password=yaml_conf_dic[section]['Password'],
                                  database=yaml_conf_dic[section]['Db_name'],
                                  port=int(yaml_conf_dic[section]['Port']))
        self.Table_name = yaml_conf_dic[section]["Table_name"]

    def execute(self, sql):
        """执行并提交"""
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
                self.db.commit()
        except Exception as e:
            print(sql)
            raise e

    def execute_no_commit(self, sql):
        """执行但不提交

        当有大量执行时,批量执行后再commit,用于节省时间
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql)

    def read_pd(self, sql):
        """执行出来dataframe"""
        return pd.read_sql(sql, self.db)

    def query(self, sql):
        """ 普通query"""
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            self.db.commit()
            return cursor.fetchall()

    def query_exception(self, sql):
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
                self.db.commit()
                return cursor.fetchall()
        except Exception as e:
            print(sql)
            raise e

    def close(self):
        """关闭连接"""
        self.db.close()
```

# pg方便的数据结构

###  array
操作符和函数可以参看 [CSDN上文章](https://blog.csdn.net/pg_hgdb/article/details/79483767)

e.g.
- 排序后聚合: array_agg(cid order by etime)