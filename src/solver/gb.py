from gurobipy import *

from data import Data

# data = read_data(data=Data(), file_path="src/sources/solomon-100/c101.txt", cust_num=10)


def gb_solver(data: Data):
    model = Model("VRPTW")
    x = {}
    w = {}
    BigM = 1e6
    for i in range(data.node_num):
        for k in range(data.vehicle_num):
            name = "w_" + str(i) + "_" + str(k)
            w[i, k] = model.addVar(0, 1, GRB.BINARY, name=name)
            for j in range(data.node_num):
                name = "x_" + str(i) + "_" + str(j) + "_" + str(k)
                x[i, j, k] = model.addVar(0, 1, GRB.BINARY, name=name)
    model.update()

    # C1
    obj = LinExpr(0)
    for i in range(data.node_num):
        for k in range(data.vehicle_num):
            for j in range(data.node_num):
                obj += data.dist_matrix[i][j] * x[i, j, k]
    GRB.MINIMIZE(obj)

    # C2
    for i in range(data.node_num):
        for k in range(data.vehicle_num):
            for j in range(data.node_num):
                model.addConstr(x[i, j, k] == 1)

    # C3-C5
    for j in range(data.node_num):
        for k in range(data.vehicle_num):
            if j != 0:
                model.addConstr(x[0, j, k] == 1)

    for k in range(data.vehicle_num):
        for h in range(1, data.node_num - 1):
            expr1 = LinExpr(0)
            expr2 = LinExpr(0)
            for i in range(data.node_num):
                if h != i:
                    expr1.addTerms(1.0, x[i, h, k])
            for j in range(data.node_num):
                if h != j:
                    expr2.addTerms(1.0, x[h, j, k])

    # C6
    for i in range(data.node_num):
        for k in range(data.vehicle_num):
            for j in range(data.node_num):
                model.addConstr(w[i, k] + data.service_time[i] + data.dist_matrix[i][j] - w[j, k]
                                <= (1 - x[i, j, k]) * BigM)

    # C7
    for i in range(data.node_num):
        for k in range(data.vehicle_num):
            model.addConstr(w[i, k] >= data.ready_time[i])









