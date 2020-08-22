# -*- coding: UTF-8 -*-
import readfile
from GeneticAlgorithm import GeneticAlgorithm
import calFitness

def main():
    depots, stations, customers, demand, time_win, tolerate_time_win = readfile.readfile("4depot_10station_40customer3.csv", depot_num=4, station_num=10, customer_num=40)
    dis_dep_cus = readfile.get_dis_matrix(depots, customers)  #depot到customer的距离矩阵
    dis_sta_cus = readfile.get_dis_matrix(stations, customers)  #station到customer的距离矩阵
    dis_cus_cus = readfile.get_dis_matrix(customers, customers)  #customer之间的距离矩阵

    min_dis_depot = readfile.get_min_dis(dis_dep_cus)  #获取距离每个customer最近的depot及距离
    min_dis_station = readfile.get_min_dis(dis_sta_cus)  #获取距离每个customer最近的station及距离

    customer_means = []
    cus1 = []
    cus2 = []
    cus3 = []
    cus4 = []
    for i in range(0, len(min_dis_depot)):
        if min_dis_depot[i][0] == 0:
            cus1.append(i+1)
        if min_dis_depot[i][0] == 1:
            cus2.append(i+1)
        if min_dis_depot[i][0] == 2:
            cus3.append(i+1)
        if min_dis_depot[i][0] == 3:
            cus4.append(i+1)
    customer_means.append(cus1)
    customer_means.append(cus2)
    customer_means.append(cus3)
    customer_means.append(cus4)

    for i in range(len(customer_means)):
        customers = customer_means[i]
        mans = len(customers)
        dep_num = i + 1 + 40
        rows = 100
        times = 300
        genetic = GeneticAlgorithm(dep_num, customers, dis_dep_cus[i], dis_sta_cus, dis_cus_cus, min_dis_station, demand, time_win, tolerate_time_win, mans, rows, times)
        genetic.run()

    # print "depot到customer的距离矩阵:"
    # print dis_dep_cus
    # print "station到customer的距离矩阵:"
    # print dis_sta_cus
    # print "customer之间的距离矩阵:"
    # print dis_cus_cus
    # print "距离每个customer最近的depot及距离:"
    # print min_dis_depot
    # print "距离每个customer最近的station及距离:"
    # print min_dis_station
    # print "customer的需求："
    # print demand
    # print "customer的期望时间窗："
    # print time_win
    # print "customer的可接受时间窗："
    # print tolerate_time_win
    # print customer_means

if __name__ == '__main__':

    main()

    # for i in range(10):
    #     print "第 %d 次：" % (i + 1)
    #     main()