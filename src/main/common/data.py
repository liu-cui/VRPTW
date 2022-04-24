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

    print(data.name)
    print(data.vehicle_num, data.vehicle_capacity)
    print(data.cust_no)
    print(data.cor_x, data.cor_y)
    print(data.demand)
    print(data.ready_time)
    print(data.due_time)
    print(data.service_time)
    print()


read_data(data=Data(), file_path="src/sources/solomon-100/c101.txt", cust_num=10)
