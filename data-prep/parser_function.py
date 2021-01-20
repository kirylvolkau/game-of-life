import csv
import numpy as np

class list_value:
    def __init__(self, id, delta, matrix):
        self.id = int(id)
        self.delta = delta
        self.matrix = matrix

def create_matrix(row):
    mat = np.zeros((25,25))
    arr_index = 2
    for i in range(25):
        for j in range(25):
            mat[i,j] = row[arr_index]
            arr_index+=1
    return(mat)

def read_file(filename):
    with open(filename) as fname:
        reader = csv.reader(fname, delimiter=',')
        file_list = [None] * 50000
        line_count = 0
        reader.__next__()
        for row in reader:
            file_list[line_count] = list_value(row[0],row[1],create_matrix(row))
            line_count += 1
    return(file_list)
