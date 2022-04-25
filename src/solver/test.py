from gurobipy import *
from common.data import read_data, Data

data = read_data(Data(), file_path="c101.txt", cust_num=25)

data.vehicle_num = 8

model = Model("test")

BigM = 1e8

x = {}
s = {}
for i in range(data.node_num):
    for k in range(data.vehicle_num):
        name = 's_' + str(i) + '_' + str(k)
        s[i,k] = model.addVar(0
                              , 1500
                              , vtype= GRB.CONTINUOUS
                              , name= name)
        for j in range(data.node_num):
            if(i != j):
                name = 'x_' + str(i) + '_' + str(j) + '_' + str(k)
                x[i,j,k] = model.addVar(0
                                        , 1
                                        , vtype= GRB.BINARY
                                        , name= name)

obj = LinExpr(0)
for i in range(data.node_num):
    for k in range(data.vehicle_num):
        for j in range(data.node_num):
            if(i != j):
                obj.addTerms(data.dist_matrix[i][j], x[i,j,k])
model.setObjective(obj, GRB.MINIMIZE)

for k in range(data.vehicle_num):
    lhs = LinExpr(0)
    for j in range(data.node_num):
        if(j != 0):
            lhs.addTerms(1, x[0,j,k])
    model.addConstr(lhs == 1, name= 'vehicle_depart_' + str(k))

for k in range(data.vehicle_num):
    for h in range(1, data.node_num - 1):
        expr1 = LinExpr(0)
        expr2 = LinExpr(0)
        for i in range(data.node_num):
            if (h != i):
                expr1.addTerms(1, x[i,h,k])

        for j in range(data.node_num):
            if (h != j):
                expr2.addTerms(1, x[h,j,k])

        model.addConstr(expr1 == expr2, name= 'flow_conservation_' + str(i))
        expr1.clear()
        expr2.clear()


for k in range(data.vehicle_num):
    lhs = LinExpr(0)
    for j in range(data.node_num - 1):
        if(j != 0):
            lhs.addTerms(1, x[j, data.node_num-1, k])
    model.addConstr(lhs == 1, name= 'vehicle_enter_' + str(k))


for i in range(1, data.node_num - 1):
    lhs = LinExpr(0)
    for k in range(data.vehicle_num):
        for j in range(1, data.node_num):
            if(i != j):
                lhs.addTerms(1, x[i,j,k])
    model.addConstr(lhs == 1, name= 'customer_visit_' + str(i))

for k in range(data.vehicle_num):
    for i in range(data.node_num):
        for j in range(data.node_num):
            if(i != j):
                model.addConstr(s[i,k] + data.dist_matrix[i][j] + data.service_time[i] - s[j,k]- BigM + BigM * x[i,j,k] <= 0 , name= 'time_windows_')


for i in range(1,data.node_num-1):
    for k in range(data.vehicle_num):
        model.addConstr(data.ready_time[i] <= s[i,k], name= 'ready_time')
        model.addConstr(s[i,k] <= data.due_time[i], name= 'due_time')


for k in range(data.vehicle_num):
    lhs = LinExpr(0)
    for i in range(1, data.node_num - 1):
        for j in range(data.node_num):
            if(i != j):
                lhs.addTerms(data.demand[i], x[i,j,k])
    model.addConstr(lhs <= data.vehicle_capacity, name= 'capacity_vehicle' + str(k))


model.optimize()
print("\n\n-----optimal value-----")
print(model.ObjVal)

for key in x.keys():
    if(x[key].x > 0 ):
        print(x[key].VarName + ' = ', x[key].x)
