from gurobipy import *
from common.data import Data


def gb_solver(data: Data, vehicle_num):
    data.vehicle_num = vehicle_num
    model = Model("VRPTW")
    x = {}
    w = {}
    BigM = 1e6
    for i in range(data.node_num):
        for k in range(data.vehicle_num):
            name = "w_{}_{}".format(i, k)
            w[i, k] = model.addVar(0, 2000, vtype=GRB.CONTINUOUS, name=name)
            for j in range(data.node_num):
                if i != j:
                    name = "x_{}_{}_{}".format(i, j, k)
                    x[i, j, k] = model.addVar(0, 1, vtype=GRB.BINARY, name=name)

    model.update()

    # C1: 最小化行驶距离
    obj = quicksum(x[i, j, k] * data.dist_matrix[i][j]
                   for i in range(data.node_num)
                   for k in range(data.vehicle_num)
                   for j in range(data.node_num)
                   if i != j)
    model.setObjective(obj, GRB.MINIMIZE)

    # C2: 每个顾客至多被服务一次
    for i in range(1, data.node_num-1):
        model.addConstr(quicksum(x[i, j, k] for j in range(data.node_num) for k in range(data.vehicle_num) if i != j)
                        == 1)

    # C3: 车从车场出发
    for k in range(data.vehicle_num):
        model.addConstr(quicksum(x[0, j, k] for j in range(data.node_num) if j != 0) == 1)

    # C4: 流平衡
    for k in range(data.vehicle_num):
        for h in range(1, data.node_num - 1):
            expr1 = LinExpr(0)
            expr2 = LinExpr(0)
            for i in range(data.node_num):
                if h != i:
                    expr1.addTerms(1, x[i, h, k])
            for j in range(data.node_num):
                if h != j:
                    expr2.addTerms(1, x[h, j, k])
            model.addConstr(expr1 == expr2)
            expr1.clear()
            expr2.clear()

    # C5: 服务结束，车返回车场
    for k in range(data.vehicle_num):
        model.addConstr(quicksum(x[i, data.node_num - 1, k]
                                 for i in range(data.node_num) if i != data.node_num - 1) == 1)

    # C6：时间窗约束：不能晚于下个顾客开始服务时间
    for i in range(data.node_num):
        for k in range(data.vehicle_num):
            for j in range(data.node_num):
                if i != j:
                    model.addConstr(w[i, k] + data.service_time[i] + data.dist_matrix[i][j] - w[j, k]
                                    <= (1 - x[i, j, k]) * BigM)

    # C7-C8：时间窗约束：当前顾客的服务时间窗约束
    for i in range(1, data.node_num - 1):
        for k in range(data.vehicle_num):
            model.addConstr(w[i, k] >= data.ready_time[i])
            model.addConstr(w[i, k] <= data.due_time[i])

    # C9：车容量约束
    for k in range(data.vehicle_num):
        model.addConstr(quicksum(x[i, j, k] * data.demand[i] for i in range(data.node_num) for j in range(data.node_num)
                                 if i != j) <= data.vehicle_capacity)

    model.optimize()

    for key in x.keys():
        # print(key)
        if x[key].x > 0:
            print(key)
            # print(x[key].VarName + ' = ', x[key].x)
    #
    # print(model.ObjVal)
