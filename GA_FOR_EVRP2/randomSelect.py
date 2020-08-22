# -*- coding: UTF-8 -*-

import random

# 根据概率随机选择的序列


def randomSelect(ranFit):
    ran = random.random()

    for i in range(len(ranFit)):
        if ran < ranFit[i]:
            return i
