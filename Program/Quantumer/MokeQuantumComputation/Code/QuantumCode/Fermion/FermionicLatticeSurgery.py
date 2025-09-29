import copy

import networkx as nx
import numpy as np

from Program.Quantumer.MokeQuantumComputation.Code.QuantumCode.Fermion.FermionicCode import FermionicCode
from Program.Quantumer.MokeQuantumComputation.Helper.IndependentCyclesFinder import IndependentCyclesFinder
from Program.Quantumer.MokeQuantumComputation.Operator.MajoranaOperator import MajoranaOperator

# %%  USER：生成Fermionic lattice surgery之后的code
"""
input.code_0：FermionicCode对象
input.code_1：FermionicCode对象
input.index_0：int对象，逻辑算符下标
input.index_1：int对象，逻辑算符下标
ouput：FermionicCode对象，融合结果
"""


def FermionicLatticeSurgery(code_A, code_B, index_A, index_B):
    # %%  SECTION：数据标准化
    code_A = code_A.copy()
    code_B = code_B.copy()
    assert isinstance(code_A, FermionicCode)
    assert isinstance(code_B, FermionicCode)
    assert isinstance(index_A, int)
    assert isinstance(index_B, int)

    # %%  SECTION：数据预处理
    number_qubit_A = code_A.number_qubit
    number_qubit_B = code_B.number_qubit
    code_B.index_map(number_qubit_A + number_qubit_B, np.arange(number_qubit_B) + number_qubit_A)
    code_A.index_map(number_qubit_A + number_qubit_B, np.arange(number_qubit_A))
    logical_operator_0 = code_A.logical_operator_list_x[index_A]
    logical_operator_1 = code_B.logical_operator_list_x[index_B]
    support_index_vector_A = np.array(logical_operator_0.x_vector, dtype=int)
    support_index_vector_B = np.array(logical_operator_1.x_vector, dtype=int)

    ##  目标初始化
    check_origin_list = []
    check_ancilla_list = []
    check_modify_list = []
    check_stable_list = []
    check_gauge_list = []
    check_z_list = []
    check_measure_list = []

    vertex_qubit_list = []
    vertex_check_list = []

    edge_list = []
    for i in range(len(code_A.check_list)):
        if len(code_A.check_list[i].x_vector) > 0:
            if len(set(code_A.check_list[i].x_vector) & set(support_index_vector_A)) > 0:
                check_origin_list.append(code_A.check_list[i].copy())
                check_modify_list.append(code_A.check_list[i].copy())
            else:
                check_stable_list.append(code_A.check_list[i].copy())
        else:
            check_z_list.append(code_A.check_list[i].copy())

    for i in range(len(code_B.check_list)):
        if len(code_B.check_list[i].x_vector) > 0:
            if len(set(code_B.check_list[i].x_vector) & set(support_index_vector_B)) > 0:
                check_origin_list.append(code_B.check_list[i].copy())
                check_modify_list.append(code_B.check_list[i].copy())
            else:
                check_stable_list.append(code_B.check_list[i].copy())
        else:
            check_z_list.append(code_B.check_list[i].copy())

    ##  为待修改的stabilizers增加ancilla及其索引
    code = FermionicCode()
    code.define_qubit(number_qubit_A + number_qubit_B)
    ancilla_list_list = []
    for i in range(len(check_modify_list)):
        x_vector_temp = check_modify_list[i].x_vector.tolist()
        z_vector_temp = []
        number_ancilla_temp = len(
            set(check_modify_list[i].x_vector) & set(np.append(support_index_vector_A, support_index_vector_B))) // 2
        temp = []
        for j in range(number_ancilla_temp):
            if check_modify_list[i].x_vector[0] < number_qubit_A:
                vertex_check_list.append((str(len(vertex_check_list)) + 'A'))
            else:
                vertex_check_list.append((str(len(vertex_check_list)) + 'B'))
            code.push_qubit(1)
            temp.append((code.qubit_list[-1], 'x'))
            temp.append((code.qubit_list[-1], 'z'))
            x_vector_temp.append(code.qubit_list[-1])
            z_vector_temp.append(code.qubit_list[-1])
            edge_list.append((str(code.qubit_list[-1]) + 'x', vertex_check_list[-1]))
            edge_list.append((str(code.qubit_list[-1]) + 'z', vertex_check_list[-1]))
        check_modify_list[i] = MajoranaOperator(x_vector_temp, z_vector_temp, 1)
        ancilla_list_list.append(temp)
    for i in range(number_qubit_A + number_qubit_B, code.number_qubit):
        vertex_qubit_list.append(str(i) + 'x')
        vertex_qubit_list.append(str(i) + 'z')

    # %%  SECTION：加入测量稳定子
    single_point = None
    single_qubit_list = []
    ##  右边logical更长的情况
    if len(support_index_vector_A) >= len(support_index_vector_B):
        ##  先将两边对齐的部分连起来
        for i in range(len(support_index_vector_B)):
            vertex_check_list.append((str(len(vertex_check_list)) + 'M'))
            x_vector_temp = [support_index_vector_A[i], support_index_vector_B[i]]
            z_vector_temp = []
            for j in range(len(check_modify_list)):
                if support_index_vector_A[i] in check_modify_list[j].x_vector or support_index_vector_B[i] in \
                        check_modify_list[j].x_vector:
                    temp = ancilla_list_list[j][-1]
                    if temp[1] == 'x':
                        x_vector_temp.append(temp[0])
                        edge_list.append((str(temp[0]) + 'x', vertex_check_list[-1]))
                    elif temp[1] == 'z':
                        z_vector_temp.append(temp[0])
                        edge_list.append((str(temp[0]) + 'z', vertex_check_list[-1]))
                    ancilla_list_list[j].pop(-1)

            if np.mod(len(x_vector_temp) + len(z_vector_temp), 2) != 0:
                if single_point is None:
                    code.push_qubit(1)
                    single_point = code.qubit_list[-1]
                    vertex_qubit_list.append(str(single_point) + 'x')
                    vertex_qubit_list.append(str(single_point) + 'z')
                    edge_list.append((str(single_point) + 'x', vertex_check_list[-1]))
                    single_qubit_list.append(code.qubit_list[-1])
                    x_vector_temp.append(code.qubit_list[-1])
                else:
                    z_vector_temp.append(single_point)
                    edge_list.append((str(single_point) + 'z', vertex_check_list[-1]))
                    single_point = None

            ##  引入新的measurement stabilizer
            check_measure_list.append(MajoranaOperator(x_vector_temp, z_vector_temp, 1))

        ##  将右边剩余的部分连起来
        length_B = len(support_index_vector_B)
        length_A = len(support_index_vector_A)
        for i in range((length_A - length_B) // 2):
            index_0 = length_B + 2 * i
            index_1 = index_0 + 1
            vertex_check_list.append((str(len(vertex_check_list)) + 'M'))
            x_vector_temp = [support_index_vector_A[index_0], support_index_vector_A[index_1]]
            z_vector_temp = []
            for j in range(len(check_modify_list)):
                if support_index_vector_A[index_0] in check_modify_list[j].x_vector:
                    temp = ancilla_list_list[j][-1]
                    if temp[1] == 'x':
                        x_vector_temp.append(temp[0])
                        edge_list.append((str(temp[0]) + 'x', vertex_check_list[-1]))
                    elif temp[1] == 'z':
                        z_vector_temp.append(temp[0])
                        edge_list.append((str(temp[0]) + 'z', vertex_check_list[-1]))
                    ancilla_list_list[j].pop(-1)
                if support_index_vector_A[index_1] in check_modify_list[j].x_vector:
                    temp = ancilla_list_list[j][-1]
                    if temp[1] == 'x':
                        x_vector_temp.append(temp[0])
                        edge_list.append((str(temp[0]) + 'x', vertex_check_list[-1]))
                    elif temp[1] == 'z':
                        z_vector_temp.append(temp[0])
                        edge_list.append((str(temp[0]) + 'z', vertex_check_list[-1]))
                    ancilla_list_list[j].pop(-1)

            if np.mod(len(x_vector_temp) + len(z_vector_temp), 2) != 0:
                if single_point is None:
                    code.push_qubit(1)
                    single_point = code.qubit_list[-1]
                    vertex_qubit_list.append(str(single_point) + 'x')
                    vertex_qubit_list.append(str(single_point) + 'z')
                    edge_list.append((str(single_point) + 'x', vertex_check_list[-1]))
                    single_qubit_list.append(code.qubit_list[-1])
                    x_vector_temp.append(code.qubit_list[-1])
                else:
                    z_vector_temp.append(single_point)
                    edge_list.append((str(single_point) + 'z', vertex_check_list[-1]))
                    single_point = None

            ##  引入新的measurement stabilizer
            check_measure_list.append(MajoranaOperator(x_vector_temp, z_vector_temp, 1))
    else:
        ##  先将两边对齐的部分连起来
        for i in range(len(support_index_vector_A)):
            vertex_check_list.append((str(len(vertex_check_list)) + 'M'))
            x_vector_temp = [support_index_vector_A[i], support_index_vector_B[i]]
            z_vector_temp = []
            for j in range(len(check_modify_list)):
                if support_index_vector_A[i] in check_modify_list[j].x_vector or support_index_vector_B[i] in \
                        check_modify_list[j].x_vector:
                    temp = ancilla_list_list[j][-1]
                    if temp[1] == 'x':
                        x_vector_temp.append(temp[0])
                        edge_list.append((str(temp[0]) + 'x', vertex_check_list[-1]))
                    elif temp[1] == 'z':
                        z_vector_temp.append(temp[0])
                        edge_list.append((str(temp[0]) + 'z', vertex_check_list[-1]))
                    ancilla_list_list[j].pop(-1)

            if np.mod(len(x_vector_temp) + len(z_vector_temp), 2) != 0:
                if single_point is None:
                    code.push_qubit(1)
                    single_point = code.qubit_list[-1]
                    vertex_qubit_list.append(str(single_point) + 'x')
                    vertex_qubit_list.append(str(single_point) + 'z')
                    edge_list.append((str(single_point) + 'x', vertex_check_list[-1]))
                    single_qubit_list.append(code.qubit_list[-1])
                    x_vector_temp.append(code.qubit_list[-1])
                else:
                    z_vector_temp.append(single_point)
                    edge_list.append((str(single_point) + 'z', vertex_check_list[-1]))
                    single_point = None

            ##  引入新的measurement stabilizer
            check_measure_list.append(MajoranaOperator(x_vector_temp, z_vector_temp, 1))

        ##  将右边剩余的部分连起来
        length_B = len(support_index_vector_B)
        length_A = len(support_index_vector_A)
        for i in range((length_B - length_A) // 2):
            index_0 = length_A + 2 * i
            index_1 = index_0 + 1
            vertex_check_list.append((str(len(vertex_check_list)) + 'M'))
            x_vector_temp = [support_index_vector_B[index_0], support_index_vector_B[index_1]]
            z_vector_temp = []
            for j in range(len(check_modify_list)):
                if support_index_vector_B[index_0] in check_modify_list[j].x_vector or support_index_vector_B[
                    index_1] in check_modify_list[j].x_vector:
                    temp = ancilla_list_list[j][-1]
                    if temp[1] == 'x':
                        x_vector_temp.append(temp[0])
                        edge_list.append((str(temp[0]) + 'x', vertex_check_list[-1]))
                    elif temp[1] == 'z':
                        z_vector_temp.append(temp[0])
                        edge_list.append((str(temp[0]) + 'z', vertex_check_list[-1]))
                    ancilla_list_list[j].pop(-1)

            if np.mod(len(x_vector_temp) + len(z_vector_temp), 2) != 0:
                if single_point is None:
                    code.push_qubit(1)
                    single_point = code.qubit_list[-1]
                    vertex_qubit_list.append(str(single_point) + 'x')
                    vertex_qubit_list.append(str(single_point) + 'z')
                    edge_list.append((str(single_point) + 'x', vertex_check_list[-1]))
                    single_qubit_list.append(code.qubit_list[-1])
                    x_vector_temp.append(code.qubit_list[-1])
                else:
                    z_vector_temp.append(single_point)
                    edge_list.append((str(single_point) + 'z', vertex_check_list[-1]))
                    single_point = None

            ##  引入新的measurement stabilizer
            check_measure_list.append(MajoranaOperator(x_vector_temp, z_vector_temp, 1))

    # %%  SECTION：图论计算规范稳定子
    for i in range(code.number_qubit - number_qubit_A - number_qubit_B):
        temp = MajoranaOperator([i + number_qubit_B + number_qubit_A], [i + number_qubit_B + number_qubit_A], 1)
        check_ancilla_list.append(temp)

    ##  获取关键参数

    for i in range(len(single_qubit_list)):
        vertex_check_list.append(str(i) + 'D')
        edge_list.append((str(single_qubit_list[i]) + 'x', str(i) + 'D'))
        edge_list.append((str(single_qubit_list[i]) + 'z', str(i) + 'D'))

    graph = nx.Graph()
    graph.add_nodes_from(vertex_check_list)
    graph.add_nodes_from(vertex_qubit_list)
    graph.add_edges_from(edge_list)
    check_gauge_list = IndependentCyclesFinder(graph)

    target = logical_operator_0.mul(logical_operator_1, code.number_qubit)

    # %%  SECTION：返回结果
    code_state=FermionicCode()
    code_state.define_qubit(code.number_qubit)
    code_correct=FermionicCode()
    code_correct.define_qubit(code.number_qubit)
    code_other=FermionicCode()
    code_other.define_qubit(code.number_qubit)
    code_measure=FermionicCode()
    code_measure.define_qubit(code.number_qubit)

    code.check_list = check_stable_list + check_modify_list+ check_gauge_list + check_z_list+check_measure_list
    code_correct.check_list=check_stable_list+ check_z_list+check_gauge_list
    code_state=copy.deepcopy(check_stable_list)+copy.deepcopy(check_z_list)
    code_other=copy.deepcopy(check_measure_list)+copy.deepcopy(check_gauge_list)+copy.deepcopy(check_modify_list)
    code_measure=copy.deepcopy(check_measure_list)+copy.deepcopy(check_measure_list)

    code.number_checker = len(code.check_list)
    code.target=target
    assert code.commute_judge()  # 检查对易性
    return code, code_state, code_other, code_correct, code_measure