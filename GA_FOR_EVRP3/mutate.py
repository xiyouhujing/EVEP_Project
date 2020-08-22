# -*- coding: UTF-8 -*-

import random

# 基因变异
# 变异的意思是当满足变异率的条件下，随机的两个因子发生多次交换，交换次数为变异迭代次数规定的次数


def change(line):
    BYL = 0.009
    JYHW = 5
    if random.random() < BYL:
        i = 0
        while i < JYHW:
            f = random.uniform(0, len(line))
            n = random.uniform(0, len(line))

            doChange(line, f, n)
            i += 1


# 将线路中的两个因子执行交换
def doChange(line, f, n):
    tmp = line[int(f)]
    line[int(f)] = line[int(n)]
    line[int(n)] = tmp

