import galois
import numpy as np

from Program.Quantumer.MokeQuantumComputation.Operator.MajoranaOperator import MajoranaOperator

#%%  KEY：计算Euler图的圈分解
"""
input.vectors：G：nx.graph对象，待分解的Euler图
ouput：list of list对象，分解的顶点集合划分
"""
def IndependentCyclesFinder(G):
    qubit_list=[]
    check_list=[]
    for index,value in enumerate(G.nodes()):
        if value[-1]=='A' or value[-1]=='B' or value[-1]=='D' or value[-1]=='M':
            check_list.append(value)
        else:
            qubit_list.append(value)
    matrix=np.zeros((len(check_list),len(qubit_list)),dtype=int)
    for index0,check in enumerate(check_list):
        for index1,qubit in enumerate(qubit_list):
            if (qubit,check) in G.edges():
                matrix[index0,index1]=1
    GF=galois.GF(2**1)
    matrix=GF(matrix)
    result=matrix.null_space()
    check_gauge_list=[]
    for i in range(len(result)):
        index_list=np.where(result[i]!=0)[0]
        temp_x=[]
        temp_z=[]
        for j in range(len(index_list)):
            temp=qubit_list[index_list[j]]
            if temp[-1]=='x':
                temp_x.append(int(temp[:-1]))
            elif temp[-1]=='z':
                temp_z.append(int(temp[:-1]))
            else:
                raise ValueError
        check_gauge_list.append(MajoranaOperator(temp_x,temp_z,1))
    return check_gauge_list

