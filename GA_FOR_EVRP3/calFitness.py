# -*- coding: UTF-8 -*-


def fitness(dis_cus_cus, dis_sta_cus, min_dis_depot, min_dis_sta, time_win, tolerate_time_win, demand, line, isShow):
    dianliang = 60.69  # 电池容量
    haodian = 1  # 耗电率
    zaizhong = 100  # 载重
    chongdian_time = 50  # 充电时间
    sudu = 1  # 电动车的速度
    server_time = 50  # 服务时间
    a = 2  # 早到的单位惩罚成本
    b = 3  # 晚到的单位惩罚成本
    M = float('inf')  # 不满足可接受时间窗时的惩罚成本
    c1 = 300  # 固定成本
    c2 = 4  # 单位距离行驶成本

    routes = []
    route = []
    mans = len(demand)
    depots = 4

    fore = line[0]  # 当前访问的点
    depot_s = min_dis_depot[fore-1][0]  # 从最近的depot出发

    carTon = demand[fore-1]  # 当前车辆的载重
    carDis = min_dis_depot[fore-1][1]  # 当前车辆行驶的总距离
    arriverTime = carDis / sudu  # 车辆到达当前点的时间
    carTime = carDis / sudu + server_time
    cf_cost = a * max(time_win[fore-1][0] - arriverTime, 0) + b * max(arriverTime - time_win[fore-1][1], 0)
    newTon = demand[fore-1]
    newDis = min_dis_depot[fore-1][1]
    totalDis = 0
    Cost = 0

    route.append(0)
    route.append(depot_s + 1 + mans)

    r = 1       # 表示当前需要车辆数

    # 遍历每个客户点
    j = 1
    while j < len(line):
        # 行驶的距离
        newDis += dis_cus_cus[fore-1][line[j]-1]

        # 当前车辆的载重
        newTon = carTon + demand[line[j]-1]

        # 当前车辆到达的时间点和离开的时间点
        arriverTime = carTime + dis_cus_cus[fore-1][line[j]-1] / sudu

        # 添加路线
        route.append(fore)

        # 如果到达j点的总行驶距离大于最大行驶距离，但是载重没有超过最大载重，就去到最近的充电站
        if newDis > dianliang/haodian and newTon <= zaizhong and arriverTime <= tolerate_time_win[line[j]-1]:
            sta_node = min_dis_sta[fore-1][0]  # 寻找最近的充电站充电
            dis_cus2sta = min_dis_sta[fore-1][1]  # 去最近的充电站的距离
            dis_sta2cus = dis_sta_cus[sta_node][line[j]-1]  # 车辆继续从充电站配送到line[j]
            newDis = dis_sta2cus  # 车辆从充电站到line[j]的行驶距离
            arriverTime = carTime + (dis_cus2sta + dis_sta2cus) / sudu + chongdian_time  # 车辆从当前点到充电站,再从充电站到line[j]的到达时间

            # 如果充电后到达line[j]的时间超过了其接受时间窗，从当前点返回最近的depot
            if arriverTime > tolerate_time_win[line[j]-1]:
                totalDis += carDis + min_dis_depot[fore - 1][1]
                Cost += cf_cost
                depot_l = min_dis_depot[fore - 1][0]  # 找到离当前点最近的depot
                route.append(depot_l+1+mans)
                route.append(0)
                route.append([cf_cost+(carDis + min_dis_depot[fore - 1][1])*c2+c1, cf_cost, (carDis + min_dis_depot[fore - 1][1])*c2])
                routes.append(route)

                r += 1  # 换一辆车配送line[j]
                fore = line[j]  # 当前配送客户点为line[j]
                depot_s = min_dis_depot[fore - 1][0]
                carTon = demand[fore-1]
                carDis = min_dis_depot[fore-1][1]
                arriverTime = carDis / sudu
                carTime = arriverTime + server_time
                cf_cost = a * max(time_win[fore - 1][0] - arriverTime, 0) + b * max(arriverTime - time_win[fore - 1][1], 0)
                route = []
                route.append(0)
                route.append(depot_s+1+mans)
            else:
                carDis = carDis + dis_cus2sta + newDis
                carTon = newTon
                cf_cost += a * max(time_win[line[j]-1][0] - arriverTime, 0) + b * max(arriverTime - time_win[line[j]-1][1], 0)
                fore = line[j]
                route.append(sta_node+1+mans+depots)

        # 如果到达j点后的载重超过最大载重，就去最近的depot，换下一辆车
        elif newTon > zaizhong or arriverTime > tolerate_time_win[line[j]-1]:
            totalDis += carDis + min_dis_depot[fore-1][1]
            Cost += cf_cost
            depot_l = min_dis_depot[fore-1][0]  # 找到未配送完成的离当前点最近的depot
            route.append(depot_l + 1 + mans)
            route.append(0)
            route.append([cf_cost+(carDis + min_dis_depot[fore - 1][1])*c2+c1, cf_cost, (carDis + min_dis_depot[fore - 1][1])*c2])
            routes.append(route)

            r += 1  # 换一辆车服务
            fore = line[j]
            depot_s = min_dis_depot[fore-1][0]
            carDis = min_dis_depot[fore-1][1]
            carTon = demand[fore-1]
            arriverTime = carDis / sudu
            carTime = carDis / sudu + server_time
            cf_cost = a * max(time_win[fore-1][0] - arriverTime, 0) + b * max(arriverTime - time_win[fore-1][1], 0)
            route = []
            route.append(0)
            route.append(depot_s + 1 + mans)
        else:
            carDis += dis_cus_cus[fore-1][line[j]-1]
            carTon = newTon
            carTime = arriverTime + server_time
            cf_cost += a * max(time_win[line[j]-1][0] - arriverTime, 0) + b * max(arriverTime - time_win[line[j]-1][1], 0)
            fore = line[j]
        j += 1

    # 加上最后一辆车的返回depot
    depot_l = min_dis_depot[fore-1][0]
    route.append(fore)
    route.append(depot_l+1+mans)
    route.append(0)
    route.append([cf_cost+(carDis+min_dis_depot[fore-1][1])*c2+c1, cf_cost, (carDis+min_dis_depot[fore-1][1])*c2])
    routes.append(route)

    # 加上最后一辆车的距离和返程的距离
    totalDis += carDis + min_dis_depot[fore-1][1]
    Cost += cf_cost

    # 目标函数，表示一个路径规划行驶的总距离的倒数越小越好
    totalCost = (c1 * r + c2 * totalDis + Cost)

    if isShow:
        print "总行驶里程为: %.1fkm" % (totalDis)
        print "总成本为: %.1f" % (totalCost)
        print "惩罚成本为：%.1f" % (Cost)
        print "运输成本为：%.1f" % (totalCost-Cost-c1)
        print "使用车辆数目：%d" % (r)
        print "完整路径："

        for i in range(len(routes)):
            print routes[i]
    else:
        # print "中间过程尝试规划的总行驶里程为: %.1fkm" %(totalDis)
        pass

    result = 1 / totalCost
    return result
