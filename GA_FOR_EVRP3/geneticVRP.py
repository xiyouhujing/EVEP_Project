# -*- coding: UTF-8 -*-
import random
import intercross
import fitness
import mutate

class GeneticAlgorithm:
    def __init__(self, dis_dep_cus, dis_sta_cus, dis_cus_cus, min_dis_depot, min_dis_station, demand, time_win, tolerate_time_win, popSize, NGen, cxPb, mutPb):
        self.dis_dep_cus = dis_dep_cus
        self.dis_sta_cus = dis_sta_cus
        self.dis_cus_cus = dis_cus_cus
        self.min_dis_depot = min_dis_depot
        self.min_dis_station = min_dis_station
        self.demand = demand
        self.time_win = time_win
        self.tolerate_time_win = tolerate_time_win
        self.popSize = popSize  #种群大小
        self.NGen = NGen  #迭代次数
        self.cxPb = cxPb  #交叉概率
        self.mutPb = mutPb  #变异概率

    def geneticVRP(self):
        cus_num = len(self.dis_cus_cus)
        zonglines = []  #用于存储历代所有种群
        lines = [[0 for i in range(cus_num)] for j in range(self.popSize)]
        R = lines[0]  # 一个随机个体
        R2 = R
        R_len = [0 for i in range(self.popSize)]  # 用来存储每条路径长度

        t = 1
        while t <= self.NGen:
            print "第 %d 次迭代：" % (t)

            #生成随机初始路径
            for i in range(self.popSize):
                line = random.sample(range(1, cus_num+1), cus_num)
                lines[i] = line

            #交叉
            farm = lines
            farm2 = farm
            for i in range(0, self.popSize, 2):
                if random.random() < self.cxPb and i < self.popSize:
                    route1 = farm[i]
                    route2 = farm[i+1]
                    route1, route2 = intercross.intercross(route1, route2)
                    farm[i] = route1
                    farm[i+1] = route2

            #变异
            for i in range(0, self.popSize):
                if random.random() <= self.mutPb:
                    farm[i] = mutate.mutate(farm[i])

            #群体的选择和更新
            FARM = [[0 for i in range(cus_num)] for j in range(self.popSize)]
            fitness_value, Cost, R = fitness.fitness(self.dis_cus_cus, self.dis_sta_cus, self.min_dis_depot, self.min_dis_station, self.time_win, self.tolerate_time_win, self.demand, farm)
            rank = [index for index, value in sorted(list(enumerate(fitness_value)), key=lambda x: x[1])]
            for i in range(0, self.popSize):
                FARM[i] = farm[rank[i]]
            fitness_value_s = sorted(fitness_value)
            zonglines.append(fitness_value_s[0])
            R = FARM[0]  #更新最短路径

            t += 1

            print "最佳路径为："
            for i in range(0, len(FARM[0])):
                print "%d," % (FARM[0][i]),

        return zonglines, R

        #画迭代图







