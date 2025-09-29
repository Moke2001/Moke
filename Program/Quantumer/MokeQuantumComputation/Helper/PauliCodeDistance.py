import itertools
import multiprocessing
import galois
import numpy as np
from ToolBox.Quantumer.MokeQuantumComputation.Helper.FiniteFieldSolve import FiniteFieldSolve

upper=None
lower=None

#%%  KEY：计算quantum stabilizer code的码距
"""
input.matrix：np.array of GF(2)对象，校验矩阵
input.gauge_list：list of np.array of GF(2)对象，规范子
output：int对象，码距
"""
def PauliCodeDistance(H_X,H_Z):
    GF=galois.GF(2)
    H_X=GF(np.array(H_X,dtype=int))
    H_Z=GF(np.array(H_Z,dtype=int))

    global upper
    global lower

    # 提交任务给进程池
    print('x-distance:')
    upper = multiprocessing.Value('i', 2000)
    lower = multiprocessing.Value('i', 0)
    processes = [multiprocessing.Process(target=lower_bound, args=(H_X,H_Z,lower,upper)),multiprocessing.Process(target=upper_bound, args=(H_X,H_Z,lower,upper))]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    print('result:x-bound=',lower.value)

    # 提交任务给进程池
    print('z-distance:')
    upper = multiprocessing.Value('i', 2000)
    lower = multiprocessing.Value('i', 0)
    processes = [multiprocessing.Process(target=lower_bound, args=(H_Z,H_X,lower,upper)),multiprocessing.Process(target=upper_bound, args=(H_Z,H_X,lower,upper))]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    print('result:z-bound=',lower.value)


def upper_bound(H_X,H_Z,lower,upper):
    center_list=H_Z.null_space()
    for num in range(1,center_list.shape[0]):
        for each in itertools.combinations(center_list,num):
            temp=None
            for vec in each:
                if temp is None:
                    temp=vec
                else:
                    temp=temp+vec
            if FiniteFieldSolve(H_X, temp) is None:
                if upper.value > np.count_nonzero(temp):
                    upper.value = np.count_nonzero(temp)
                    print('upperbound:', upper.value)
            if lower.value == upper.value:
                return lower.value


def lower_bound(H_X,H_Z,lower,upper):
    GF=galois.GF(2 ** 1)
    pos=range(H_X.shape[1])
    temp = GF(np.zeros(H_X.shape[1], dtype=int))
    for num in range(1,H_X.shape[1]):
        lower.value=num
        print('lowerbound:', lower.value)
        for each in itertools.combinations(pos,num):
            temp[:]=0
            temp[list(each)]=1
            if np.count_nonzero(H_Z@temp)==0:
                if FiniteFieldSolve(H_X, temp) is None:
                    upper.value = np.count_nonzero(temp)
                    print('upperbound:', upper.value)
            if lower.value==upper.value:
                return lower.value

if __name__ == '__main__':
    H_X=np.array([[1,1,1,1,0,0,0],[1,0,0,1,0,1,1],[1,0,1,0,1,0,1]])
    H_Z=np.array([[1,1,1,1,0,0,0],[1,0,0,1,0,1,1],[1,0,1,0,1,0,1]])
    PauliCodeDistance(H_X,H_Z)