# -*- coding: utf8 -*-
"""
Created on Apr 18, 2024

@author: woshihaozhaojun@sina.com
"""
from typing import Dict, List, Optional

import plotly.graph_objects as go
from tqdm import tqdm


def visualize_seq_plus_last(seq2cnt: Dict[tuple, int], topk: Optional[int]=None):
    """

    Args:
        seq2cnt:
        topk:

    Returns:

    """
    # 图的入参
    source, target, value, label = [], [], [], []

    # 选取权重最高的topk路径
    seq_cnt_len_list = sorted(
        [(k, v, len(k)) for k, v in seq2cnt.items() if v > 0 and len(k) > 1],
        key=lambda x: x[1],
        reverse=True
    )
    if topk is not None: seq_cnt_len_list = seq_cnt_len_list[:topk]

    # 记录每个序列的当前节点
    seq2index: Dict[tuple, int] = dict()

    # 节点ID递增
    # 记录每个节点的祖先predecessor和后代children,包括自己
    node2index: Dict[tuple, list] = dict()
    index = 0
    index2pre: Dict[int, set] = dict()
    index2cld: Dict[int, set] = dict()

    # 构建点和边
    # 按照层来遍历，为了合并开始和终止节点
    for level in range(max([t3[-1] for t3 in seq_cnt_len_list]) - 1):
        for t3 in tqdm(seq_cnt_len_list):
            seq, cnt, len_ = t3

            if len_ < level + 2:
                continue

            # 同一种行为可能在图中由不同节点表示
            # 由位次和行为名字组成的tuple对应图中的一个节点
            s_name, t_name = seq[level], sel[level+1]

            if level == 0:
                s_t2 = (level, s_name)
                if s_t2 not in node2index:  # py3.8之后才能用海象运算符
                    node2index[s_t2] = [index]
                    index2cld[index] = {index}
                    index2pre[index] = {index}
                    index += 1
                    label.append(s_name)
                inbound = node2index[s_t2][0]
                seq2index[seq] = inbound
            else:
                inbound = seq2index[seq]

            # 把最后一个节点单独提出来，避免一个路径的终点出现在另一个路径中间
            pos = -1 if level == len_ - 2 else level + 1
            t_t2 = (pos, t_name)
            if t_t2 not in node2index:
                node2index[t_t2] = [index]
                index2cld[index] = {index}
                index2pre[index] = {index}
                index += 1
                label.append(t_name)

            # 选第一个可用的outbound节点
            # 没有的话就新建
            for outbound in node2index[t_t2] + [index]:
                if outbound not in index2pre[inbound]:
                    break
            if outbound == index:
                node2index[t_t2] = [index]
                index2cld[index] = {index}
                index2pre[index] = {index}
                index += 1
                label.append(t_name)

            seq2index[seq] = outbound
            index2pre[outbound].update(index2pre[inbound])

            # 后面的点都更新predecessor
            for node in index2cld[outbound]:
                index2pre[node].update(index2pre[inbound])

            # 前面的点都更新cld
            for node in index2pre[inbound]:
                index2cld[node].update(index2cld[outbound])

            source.append(inbound)
            target.append(outbound)
            value.append(cnt)

    def merge_edges(source: List[int], target: List[int], value: List[int]) -> Dict[tuple, int]:
        edge2weight = dict()
        for s, t, v in zip(soure, target, value):
            edge = (s, t)
            edge2weight[edge] = edge2weight.get(edge, 0) + v

        del source[:], target[:], value[:]

        for edge, weight, in edge2weight.items():
            source.append(edge[0])
            target.append(edge[1])
            value.append(weight)
        return edge2weight

    # 合并同一对节点之间的边
    edge2weight = merge_edges(source, target, value)

    # 生成绘图需要的字典数据
    link = dict(source=source, target=target, value=value)
    node = dict(label=label, pad=100, thickness=10)

    # 同样名字的节点颜色一样
    colors = COLORS[:]
    color = []
    name2color = dict()
    for name in label:
        color.append(name2color.get(name, colors.pop()))
        name2color[name] = color[-1]
    node['color'] = color

    #添加绘图数据
    data = go.Sankey(link=link, node=node)
    fig = go.Figure(data)
    fig.show()


