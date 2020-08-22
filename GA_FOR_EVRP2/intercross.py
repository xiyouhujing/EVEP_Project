# -*- coding: UTF-8 -*-
import random
import math

def intercross(route1, route2):
    L = len(route1)

    #确定交叉宽度
    if L <= 10:
        W = 2
    elif L > 10 and (float(L)/10 - L/10) >= random.random():
        W = math.ceil(float(L)/10) + 8
    else:
        W = float(L)/10 + 8

    p = int(random.uniform(0, L-W+1))  #选择随机交叉范围，从p到p+W

    #交叉
    for i in range(1, int(W+1)):
        node1 = route2[p+i-1]
        index1 = route1.index(node1)
        node2 = route1[p+i-1]
        index2 = route2.index(node2)
        route1[p+i-1], route2[p+i-1] = doChange(route1[p+i-1], route2[p+i-1])
        route1[index1], route2[index2] = doChange(route1[index1], route2[index2])

    return route1, route2

def doChange(a, b):
    tem = a
    a = b
    b = tem
    return a, b

# if __name__ == '__main__':
#     route1 = [10, 9, 8, 5, 6, 7, 1, 2, 3, 4]
#     route2 = [8, 5, 9, 4, 3, 2, 1, 10, 6, 7]
#     R1, R2 = intercross(route1, route2)
#     print R1, R2