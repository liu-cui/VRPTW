import math
import re


class Data:
    name = ""
    vehicle_capacity = 0
    vehicle_num = 0
    cust_num = 0
    node_num = 0
    cust_no = []
    cor_x = []
    cor_y = []
    demand = []
    ready_time = []
    due_time = []
    service_time = []
    dist_matrix = []


def read_data(data, file_path, cust_num):
    data.cust_num = cust_num
    data.node_num = cust_num + 2
    f = open(file_path, "r")
    lines = f.readlines()
    count = 0
    for line in lines:
        count += 1
        if count == 1:
            data.name = line.strip()
        if count == 5:
            line = line.strip()
            temp = re.split(r" +", line)
            temp = list(map(int, temp))
            data.vehicle_num = temp[0]
            data.vehicle_capacity = temp[1]
        if 10 <= count <= 10 + cust_num:
            line = line.strip()
            temp = re.split(r" +", line)
            temp = list(map(int, temp))
            data.cust_no.append(temp[0])
            data.cor_x.append(temp[1])
            data.cor_y.append(temp[2])
            data.demand.append(temp[3])
            data.ready_time.append(temp[4])
            data.due_time.append(temp[5])
            data.service_time.append(temp[6])

    data.cust_no.append(data.cust_no[0])
    data.cor_x.append(data.cor_x[0])
    data.cor_y.append(data.cor_y[0])
    data.demand.append(data.demand[0])
    data.ready_time.append(data.ready_time[0])
    data.due_time.append(data.due_time[0])
    data.service_time.append(data.service_time[0])

    data.dist_matrix = [[0.] * data.node_num for _ in range(data.node_num)]
    for i in range(data.node_num):
        for j in range(data.node_num):
            temp = (data.cor_x[i] - data.cor_x[j]) ** 2 + (data.cor_y[i] - data.cor_y[j]) ** 2
            data.dist_matrix[i][j] = round(math.sqrt(temp), 1)

    # print(common.name)
    # print(common.vehicle_num, common.vehicle_capacity)
    # print(common.cust_no)
    # print(common.cor_x, common.cor_y)
    # print(common.demand)
    # print(common.ready_time)
    # print(common.due_time)
    # print(common.service_time)
    # print(common.dist_matrix)
    return data



