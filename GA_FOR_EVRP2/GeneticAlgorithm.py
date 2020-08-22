# -*- coding: UTF-8 -*-

import random
import calFitness
import clMountain
import randomSelect
import intercross
import mutate


# 遗传算法
class GeneticAlgorithm:

    # 定义一些遗传算法需要的参数
    JCL = 0.9  # 遗传时的交叉率

    def __init__(self, dep_num, customers, dis_dep_cus, dis_sta_cus, dis_cus_cus, min_dis_station, demand, time_win, tolerate_time_win, mans, rows, times):
        self.dep_num = dep_num
        self.customers = customers
        self.dis_dep_cus = dis_dep_cus  # depot到customer的距离矩阵
        self.dis_sta_cus = dis_sta_cus  # station到customer的距离矩阵
        self.dis_cus_cus = dis_cus_cus  # customer之间的距离矩阵
        self.min_dis_station = min_dis_station  # customer到哪个station最近
        self.demand = demand  # customer的需求
        self.time_win = time_win  # 期望时间窗
        self.tolerate_time_win = tolerate_time_win  # 可接受时间窗
        self.mans = mans  # customer的数量
        self.rows = rows  # 排列个数
        self.times = times  # 迭代次数

    # -------------遗传函数开始执行---------------------
    def run(self):

        print "开始迭代"

        # 路线数组
        lines = [[0 for i in range(self.mans)] for i in range(self.rows)]

        # 适应度
        fit = [0 for i in range(self.rows)]

        # print "初始输入获取rows个随机排列，并且计算适应度"
        # 初始输入获取rows个随机排列，并且计算适应度
        for i in range(0, self.rows):
            random.shuffle(self.customers)
            lines[i] = self.customers

            # 计算每个线路的适应度
            # print "计算每个线路的适应度 i = %d" % (i)
            fit[i] = calFitness.fitness(self.dep_num, self.dis_cus_cus, self.dis_sta_cus, self.dis_dep_cus, self.min_dis_station, self.time_win, self.tolerate_time_win, self.demand, lines[i], False)

        # 迭代次数
        t = 0

        while t < self.times:

            # 适应度
            newLines = [[0 for i in range(self.mans)] for i in range(self.rows)]
            nextFit = [0 for i in range(self.rows)]
            randomFit = [0 for i in range(self.rows)]
            totalFit = 0
            tmpFit = 0

            # print "计算总的适应度"
            # 计算总的适应度
            for i in range(self.rows):
                totalFit += fit[i]

            # print "通过适应度占总适应度的比例生成随机适应度"
            # 通过适应度占总适应度的比例生成随机适应度
            for i in range(self.rows):
                randomFit[i] = tmpFit + fit[i] / totalFit
                tmpFit += randomFit[i]

            # print "上一代中的最优直接遗传到下一代"
            # 上一代中的最优直接遗传到下一代
            m = fit[0]
            ml = 0

            for i in range(self.rows):
                if m < fit[i]:
                    m = fit[i]
                    ml = i

            for i in range(self.mans):
                newLines[0][i] = lines[ml][i]

            nextFit[0] = fit[ml]

            # print "对最优解使用爬山算法促使其自我进化"
            # 对最优解使用爬山算法促使其自我进化
            clMountain.clMountain(self.dep_num, self.dis_cus_cus, self.dis_sta_cus, self.dis_dep_cus, self.min_dis_station, self.time_win, self.tolerate_time_win, self.demand, newLines[0])

            # print "开始遗传"
            # 开始遗传
            nl = 1
            while nl < self.rows:
                # 选择操作
                r = int(randomSelect.randomSelect(randomFit))

                # 交叉操作
                # 判断是否需要交叉，不能越界
                if random.random() < self.JCL and nl + 1 < self.rows:
                    # 获取交叉排列
                    rn = int(randomSelect.randomSelect(randomFit))
                    fline, nline = intercross.intercross(lines[r], lines[rn])

                    # 基因变异
                    mutate.change(fline)
                    mutate.change(nline)

                    # print "交叉并且变异后的结果加入下一代"
                    # 交叉并且变异后的结果加入下一代
                    for i in range(self.mans):
                        newLines[nl][i] = fline[i]
                        newLines[nl + 1][i] = nline[i]

                    nextFit[nl] = calFitness.fitness(self.dep_num, self.dis_cus_cus, self.dis_sta_cus, self.dis_dep_cus, self.min_dis_station, self.time_win, self.tolerate_time_win, self.demand, fline, False)
                    nextFit[nl + 1] = calFitness.fitness(self.dep_num, self.dis_cus_cus, self.dis_sta_cus, self.dis_dep_cus, self.min_dis_station, self.time_win, self.tolerate_time_win, self.demand, nline, False)

                    nl += 2
                else:
                    # print "不需要交叉的，直接变异，然后遗传到下一代"
                    # 不需要交叉的，直接变异，然后遗传到下一代
                    line = [0 for i in range(self.mans)]
                    i = 0
                    while i < self.mans:
                        line[i] = lines[r][i]
                        i += 1
                    # 基因变异
                    mutate.change(line)

                    # 加入下一代
                    i = 0
                    while i < self.mans:
                        newLines[nl][i] = line[i]
                        i += 1

                    nextFit[nl] = calFitness.fitness(self.dep_num, self.dis_cus_cus, self.dis_sta_cus, self.dis_dep_cus, self.min_dis_station, self.time_win, self.tolerate_time_win, self.demand, line, False)
                    nl += 1

            # print "新的一代覆盖上一代 当前是第 %d 代" %(t)
            # 新的一代覆盖上一代
            for i in range(self.rows):
                for h in range(self.mans):
                    lines[i][h] = newLines[i][h]

                fit[i] = nextFit[i]

            t += 1

        # 上代中最优的为适应函数最小的
        m = fit[0]
        ml = 0

        for i in range(self.rows):
            if m < fit[i]:
                m = fit[i]
                ml = i

        print "迭代完成"
        # 输出结果:
        calFitness.fitness(self.dep_num, self.dis_cus_cus, self.dis_sta_cus, self.dis_dep_cus, self.min_dis_station, self.time_win, self.tolerate_time_win, self.demand, lines[ml], True)

        print "最优权值为: %f" % (m)
        print "最优结果为:"

        for i in range(self.mans):
            print "%d," % (lines[ml][i]),

        print "    "
        print "    "
        print "    "

    # -----------------遗传函数执行完成--------------------


