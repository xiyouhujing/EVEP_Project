# -*- coding: UTF-8 -*-

import numpy as np
import math

def readfile(filename):
    data = np.genfromtxt(filename, delimiter=',', skip_header=True)
    location = data[:, :3]
    q_matrix = data[:, 3]
    et_matrix = data[:, 4]
    lt_matrix = data[:, 5]
    eet_matrix = data[:, 6]
    llt_matrix = data[:, 7]
    d_matrix = [[0 for i in range(len(data))] for i in range(len(data))]

    for i in range((len(data))):
        for j in range(len(data)):
            dist = math.sqrt(pow(location[i][1]-location[j][1], 2)+pow(location[i][2]-location[j][2], 2))
            d_matrix[i][j] = dist

    return d_matrix, q_matrix, et_matrix, lt_matrix, eet_matrix, llt_matrix


if __name__ == '__main__':
    d, q, et, lt, eet, llt = readfile("sss.csv")
    print d
    print q
    print et
    print lt
    print eet
    print llt