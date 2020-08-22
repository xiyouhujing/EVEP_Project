# -*- coding: UTF-8 -*-
import readfile
from GeneticAlgorithm import GeneticAlgorithm
import calFitness


def main():
    depots, stations, customers, demand, time_win, tolerate_time_win = readfile.readfile("2depot_2station_20customer.csv", depot_num=2, station_num=2, customer_num=20)
    dis_dep_cus = readfile.get_dis_matrix(depots, customers)  #depot到customer的距离矩阵
    dis_sta_cus = readfile.get_dis_matrix(stations, customers)  #station到customer的距离矩阵
    dis_cus_cus = readfile.get_dis_matrix(customers, customers)  #customer之间的距离矩阵

    min_dis_depot = readfile.get_min_dis(dis_dep_cus)  #获取距离每个customer最近的depot及距离
    min_dis_station = readfile.get_min_dis(dis_sta_cus)  #获取距离每个customer最近的station及距离

    mans = 20
    rows = 100
    times = 300

    # line = [3, 29, 14, 39, 19, 7, 35, 5, 21, 6, 33, 4, 26, 31, 11, 18, 20, 1, 30, 36, 15, 24, 23, 32, 34, 40, 37, 9, 22, 16, 8, 38, 12, 13, 10, 28, 2, 17, 25, 27]
    # result = calFitness.fitness(dis_cus_cus, dis_sta_cus, min_dis_depot, min_dis_station, time_win, tolerate_time_win, demand, line, True)
    # print result

    genetic = GeneticAlgorithm(dis_dep_cus, dis_sta_cus, dis_cus_cus, min_dis_depot, min_dis_station, demand, time_win, tolerate_time_win, mans, rows, times)
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

if __name__ == '__main__':

    main()

    # for i in range(10):
    #     print "第 %d 次：" % (i + 1)
    #     main()