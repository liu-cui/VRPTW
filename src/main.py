from common.data import read_data, Data
from solver.gb import gb_solver

if __name__ == '__main__':

    data = read_data(Data(), file_path="src/sources/solomon-100/c101.txt", cust_num=25)
    gb_solver(data, vehicle_num=8)

