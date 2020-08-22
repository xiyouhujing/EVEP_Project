# -*- coding: UTF-8 -*-
import numpy as np
import math

def readfile(filename, depot_num, station_num, customer_num):
    data = np.genfromtxt(filename, delimiter=',', skip_header=True)
    depots = []
    stations = []
    customers = []
    for i in range(0, depot_num):
        depots.append(data[i])
    for i in range(depot_num, depot_num+station_num):
        stations.append(data[i])
    for i in range(depot_num+station_num, depot_num+station_num+customer_num):
        customers.append(data[i])

    demand = [0 for i in range(len(customers))]
    time_win = []
    tolerate_time_win = []
    for i in range(0, len(customers)):
        d = customers[i][3]
        et = customers[i][4]
        lt = customers[i][5]
        llt = customers[i][6]
        demand[i] = d
        time_win.append([et, lt])
        tolerate_time_win.append(llt)

    return depots, stations, customers, demand, time_win, tolerate_time_win

def get_dis_matrix(list1, list2):
    dis_mat = [[0 for i in range(len(list2))] for j in range(len(list1))]
    for i in range(0, len(list1)):
        for j in range(0, len(list2)):
            dis = math.sqrt(pow(list1[i][1] - list2[j][1], 2) + pow(list1[i][2] - list2[j][2], 2))
            dis_mat[i][j] = dis
    return dis_mat

def get_min_dis(dis_mat):
    min_dis_mat = []
    for j in range(0, len(dis_mat[0])):
        min_dis = dis_mat[0][j]
        min_index = 0
        for i in range(0, len(dis_mat)):
            if min_dis > dis_mat[i][j]:
                min_dis = dis_mat[i][j]
                min_index = i
        min_dis_mat.append([min_index, min_dis])
    return min_dis_mat
