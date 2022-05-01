from common.data import read_data, Data
from solver.gurobi_solver import gb_solver
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = read_data(Data(), file_path="src/sources/solomon-100/c101.txt", cust_num=25)
    plt.scatter(data.cor_x[0], data.cor_y[0], marker="s", c="r")
    plt.scatter(data.cor_x[1:-1], data.cor_y[1:-1], c="b")
    # plt.show()
    # print(data.cor_x)
    # print(data.cor_y)
    active_arcs = gb_solver(data, vehicle_num=5)
    for i, j in active_arcs:
        plt.plot([data.cor_x[i], data.cor_x[j]], [data.cor_x[i], data.cor_y[j]], c='g', zorder=0)
    plt.plot(data.cor_x[0], data.cor_y[0], c='r', marker='s')
    plt.scatter(data.cor_x[1:-1], data.cor_y[1:-1], c='b')
    plt.show()
