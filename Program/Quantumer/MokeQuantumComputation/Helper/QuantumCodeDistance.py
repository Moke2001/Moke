import itertools
import multiprocessing
import galois
import numpy as np
from ToolBox.Quantumer.MokeQuantumComputation.Helper.FiniteFieldSolve import FiniteFieldSolve


upper=2000
lower=0

#%%  KEY：计算quantum stabilizer code的码距
"""
input.matrix：np.array of GF(2)对象，校验矩阵
input.gauge_list：list of np.array of GF(2)对象，规范子
output：int对象，码距
"""
def QuantumCodeDistance(stabilizer_list,gauge_list,number_qubit):

    matrix=None
    for i in range(len(stabilizer_list)):
        if i==0:
            matrix=stabilizer_list[i].get_matrix(number_qubit)
        else:
            matrix=np.vstack([matrix,stabilizer_list[i].get_matrix(number_qubit)])

    gauge=[]
    for i in range(len(gauge_list)):
        if i==0:
            gauge=gauge_list[i].get_matrix(number_qubit)
        else:
            gauge=np.vstack([gauge,gauge_list[i].get_matrix(number_qubit)])

    global upper
    global lower
    if len(gauge)>0:
        gauge_group=np.vstack([gauge,matrix])
    else:
        gauge_group=matrix

    # 提交任务给进程池
    upper = multiprocessing.Value('i', 2000)
    lower = multiprocessing.Value('i', 0)
    processes = [multiprocessing.Process(target=lower_bound, args=(matrix,gauge,lower,upper)),multiprocessing.Process(target=upper_bound, args=(gauge_group,matrix.null_space(),lower,upper))]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    print('result:bound=',lower.value)

    return lower


def upper_bound(gauge_group,center_list,lower,upper):
    for num in range(1,center_list.shape[0]):
        for each in itertools.combinations(center_list,num):
            temp=None
            for vec in each:
                if temp is None:
                    temp=vec
                else:
                    temp=temp+vec
            if FiniteFieldSolve(gauge_group, temp) is None:
                if upper.value > np.count_nonzero(temp):
                    upper.value = np.count_nonzero(temp)
                    print('upperbound:', upper.value)
            if lower.value == upper.value:
                return lower.value

def lower_bound(matrix,gauge,lower,upper):
    GF=galois.GF(2 ** 1)
    pos=range(matrix.shape[1])
    temp = GF(np.zeros(matrix.shape[1], dtype=int))
    if len(gauge)>0:
        gauge_group=np.vstack([gauge,matrix])
    else:
        gauge_group=matrix
    for num in range(1,matrix.shape[1]):
        lower.value=num
        print('lowerbound:', lower.value)
        for each in itertools.combinations(pos,num):
            temp[:]=0
            temp[list(each)]=1
            if np.count_nonzero(matrix@temp)==0:
                if FiniteFieldSolve(gauge_group, temp) is None:
                    upper.value = np.count_nonzero(temp)
                    print('upperbound:', upper.value)
            if lower.value==upper.value:
                return lower.value


