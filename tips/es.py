''' 精确匹配
'''
"query" : {
    "constant_score" : {  # constant_score 查询以非评分模式来执行 term 查询并以一作为统一评分
        "filter" : {
            "term" : {  # term 查询会查找我们指定的精确值。它接受一个字段名以及我们希望查找的数值
                "price" : 20
            }
        }
    }
}


"query" : {
    "constant_score" : {
        "filter" : {
            "terms" : { # 包含关系，价格为20 或30. 此外,如果一个product的price包含20，也会被匹配
                "price" : [20, 30]
            }
        }
    }
}

''' 范围匹配
'''
"query" : {
    "constant_score" : {
        "filter" : {
            "range" : { # 范围,而不是精确匹配
                "price" : {
                    "gte" : 20,  # gte, gt, lte, lt
                    "lt"  : 40
                }
            }
        }
    }
}



''' 底层查询 

term 或 fuzzy 这样的底层查询不需要分析阶段，它们对单个词项进行操作
'''

''' 高层查询

像 match 或 query_string 这样的查询是高层查询，它们了解字段映射的信息：

如果查询 日期（date） 或 整数（integer） 字段，它们会将查询字符串分别作为日期或整数对待。
如果查询一个（ not_analyzed ）未分析的精确值字符串字段， 它们会将整个查询字符串作为单个词项对待。
但如果要查询一个（ analyzed ）已分析的全文字段， 它们会先将查询字符串传递到一个合适的分析器，然后生成一个供查询的词项列表。
一旦组成了词项列表，这个查询会对每个词项逐一执行底层的查询，再将结果合并，然后为每个文档生成一个最终的相关度评分。
'''


''' bool查询

bool （布尔）过滤器。 这是个 复合过滤器（compound filter） ，它可以接受多个其他过滤器作为参数，并将这些过滤器结合成各式各样的布尔（逻辑）组合。

bool 查询是多语句查询的主干
它的适用场景很多，特别是当需要将不同查询字符串映射到不同字段的时候。
'''

''' must must_not should

布尔过滤器编辑
一个 bool 过滤器由三部分组成：

{
   "bool" : {
      "must" :     [],
      "should" :   [],
      "must_not" : [],
   }
}

must
所有的语句都 必须（must） 匹配，与 AND 等价。
must_not
所有的语句都 不能（must not） 匹配，与 NOT 等价。
should
至少有一个语句要匹配，与 OR 等价。

所有 must 语句必须匹配，所有 must_not 语句都必须不匹配
默认情况下，没有 should 语句是必须匹配的，只有一个例外：那就是当没有 must 语句的时候，至少有一个 should 语句必须匹配。
就像我们能控制 match 查询的精度 一样，我们可以通过 minimum_should_match 参数(绝对数字或百分比)控制需要匹配的 should 语句的数量
'''
"query": {
    "bool": { # bool查询, more-matches-is-better
        "should": [   # more
            { "match": { "title":  "War and Peace" }},
            { "match": { "author": "Leo Tolstoy"   }},
            { "bool":  {  # 调节权重用, 为了让translator权重低, 现在title和author以及translator各 1/3
                "should": [
                    { "match": { "translator": "Constance Garnett" }},
                    { "match": { "translator": "Louise Maude"      }}
                ]
            }}
        ]
    }
}

''' boost 

直接用boost来调节权重, boost默认为1
'''
"query": {
    "bool": {
      "should": [
        { "match": { 
            "title":  {
              "query": "War and Peace",
              "boost": 2
        }}},
        { "match": { 
            "author":  {
              "query": "Leo Tolstoy",
              "boost": 2
        }}},
        { "bool":  { 
            "should": [
              { "match": { "translator": "Constance Garnett" }},
              { "match": { "translator": "Louise Maude"      }}
            ]
        }}
      ]
    }
}

''' multi-field 多字段搜索

单字符串查询的三种场景 : 最佳字段best fields，多数字段most fields，交叉字段cross fields

前两者是字段中心式 field-centric,le dernier是词中心式term-centric
'''


''' best field 
不使用 bool 查询，可以使用 dis_max 即分离 最大化查询（Disjunction Max Query）

分离（Disjunction）的意思是 或（or） ，这与可以把结合（conjunction）理解成 与（and） 相对应。

分离最大化查询（Disjunction Max Query）指的是： 将任何与任一查询匹配的文档作为结果返回，但只将最佳匹配的评分作为查询的评分结果返回

dis_max 只使用单个最佳匹配的字段的得分
'''

"query": {
    "dis_max": { 
        "queries": [
            { "match": { "title": "Brown fox" }},
            { "match": { "body":  "Brown fox" }}
        ]
    }
}

'''
tie_breaker 参数提供了一种 dis_max 和 bool 之间的折中选择，它的评分方式如下：

获得最佳匹配语句的评分 _score 。
将其他匹配语句的评分结果与 tie_breaker 相乘。
对以上评分求和并规范化。
'''
"query": {
    "dis_max": {
        "queries": [
            { "match": { "title": "Quick pets" }},
            { "match": { "body":  "Quick pets" }}
        ],
        "tie_breaker": 0.3
    }
}


# multi_match 查询为能在多个字段上反复执行相同查询提供了一种便捷方式
"dis_max": {
    "queries":  [
        {
            "match": {
                "title": {
                    "query": "Quick brown fox",
                    "minimum_should_match": "30%"
                }
            }
        },
        {
            "match": {
                "body": {
                    "query": "Quick brown fox",
                    "minimum_should_match": "30%"
                }
            }
        },
    ],
    "tie_breaker": 0.3
}
# 改写成multi_match
"multi_match": {
    "query":                "Quick brown fox",
    "type":                 "best_fields",  # 默认值,可以不写
    "fields":               [ "title", "body" ],
    "tie_breaker":          0.3,
    "minimum_should_match": "30%" 
}

"multi_match": {
    "query":  "Quick brown fox",
    "fields": [ "*_title", "chapter_title^2" ]  # 提升单个字段的权重, chapter_title的boost为2
}


''' most fields

为了提高召回率,我们通常考虑 提取词干\变音\近义词 等,将同一文本不同处理后放入其它的字段
这些附加的字段可以看成提高每个文档的相关度评分的信号 signals ，能匹配字段的越多越好
'''

"query": {
    "multi_match": {
        "query":  "jumping rabbits",
        "type":   "most_fields", 
        "fields": [ "title", "title.std" ]
    }
}

''' cross fields

跨字段查询词

相比设置新的field来综合要跨的fields，_all和cross_fields避免了信息冗余
相比_all,可以设置boost
'''



''' match 查询

match查询的多词查询只是简单地将生成的term查询包含在了一个bool查询中

匹配分数和文档长度也有关
'''

1.
{
    "match": { "title": "brown fox"}  
}
等价于
{
  "bool": {
    "should": [
      { "term": { "title": "brown" }},
      { "term": { "title": "fox"   }}
    ]
  }
}


2.
{
    "match": {
        "title": {
            "query":    "brown fox",
            "operator": "and" # 默认or操作符
        }
    }
}
等价于
{
  "bool": {
    "must": [
      { "term": { "title": "brown" }},
      { "term": { "title": "fox"   }}
    ]
  }
}

3. 
{
    "match": {
        "title": {
            "query":                "quick brown fox",
            "minimum_should_match": "75%"
        }
    }
}
等价于
{
  "bool": {
    "should": [
      { "term": { "title": "brown" }},
      { "term": { "title": "fox"   }},
      { "term": { "title": "quick" }}
    ],
    "minimum_should_match": 2 
  }
}