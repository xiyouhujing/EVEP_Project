# -*- coding: UTF-8 -*-

import random
import calFitness
import mutate


def clMountain(dis_cus_cus, dis_sta_cus, min_dis_depot, min_dis_sta, time_win, tolerate_time_win, demand, line):
    PSCS = 5  # 爬山算法迭代次数
    oldFit = calFitness.fitness(dis_cus_cus, dis_sta_cus, min_dis_depot, min_dis_sta, time_win, tolerate_time_win, demand, line, False)

    i = 0
    while i < PSCS:
        f = random.uniform(0, len(line))
        n = random.uniform(0, len(line))

        mutate.doChange(line, f, n)

        newFit = calFitness.fitness(dis_cus_cus, dis_sta_cus, min_dis_depot, min_dis_sta, time_win, tolerate_time_win, demand, line, False)

        if newFit < oldFit:
            mutate.doChange(line, f, n)
        i += 1
