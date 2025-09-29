import random

import galois
import numpy as np

from Program.Quantumer.MokeQuantumComputation.Helper.FiniteFieldSolve import FiniteFieldSolve
from Program.Quantumer.MokeQuantumComputation.Helper.QuantumCodeDistance import QuantumCodeDistance
from Program.Quantumer.MokeQuantumComputation.Operator.MajoranaOperator import MajoranaOperator


def generate_cyclic_matrix(n, l=None):
    """
    生成n×n的循环01矩阵

    参数:
    n: 矩阵维度
    l: 偏置参数，如果为None则随机生成

    返回:
    numpy数组: 循环01矩阵
    """
    if l is None:
        random.seed()
        l = random.randint(0, n - 1)  # 随机生成偏置

    matrix = np.zeros((n, n), dtype=int)
    matrix[0, l % n] = 1  # 在第一行的位置l放置1

    # 构建循环矩阵的其余行
    for i in range(1, n):
        matrix[i] = np.roll(matrix[i - 1], 1)

    return matrix


def generate_sum_of_cyclic_matrices(n, num_matrices=None):
    """
    生成若干个循环01矩阵的和，确保每个矩阵都是不同的

    参数:
    n: 矩阵维度
    num_matrices: 要相加的循环矩阵数量，如果为None则随机生成1-3个

    返回:
    numpy数组: 循环矩阵的和（结果模2）
    """
    if num_matrices is None:
        num_matrices = random.randint(1, 3)  # 随机选择1-3个矩阵相加

    result = np.zeros((n, n), dtype=int)
    generated_matrices = []  # 用于存储已生成的矩阵，确保唯一性

    for _ in range(num_matrices):
        # 生成一个唯一的循环矩阵
        max_attempts = 100  # 最大尝试次数，防止无限循环
        attempts = 0
        unique_matrix_found = False

        while not unique_matrix_found and attempts < max_attempts:
            attempts += 1
            new_matrix = generate_cyclic_matrix(n)

            # 检查新矩阵是否与已生成的矩阵重复
            is_unique = True
            for mat in generated_matrices:
                if np.array_equal(new_matrix, mat):
                    is_unique = False
                    break

            if is_unique:
                unique_matrix_found = True
                generated_matrices.append(new_matrix)
                result = (result + new_matrix) % 2  # 模2加法

    if len(generated_matrices) < num_matrices:
        print(f"警告: 在{n}×n的维度下无法生成{num_matrices}个不同的循环矩阵")
        print(f"实际生成了{len(generated_matrices)}个不同的循环矩阵")

    return result


def kronecker_product(A, B):
    """
    计算两个矩阵的克罗内克积（张量积）

    参数:
    A, B: 输入矩阵

    返回:
    numpy数组: 克罗内克积结果
    """
    return np.kron(A, B)


def generate_hgp_check_matrix(n1, n2, use_sum=False):
    """
    生成HGP码的校验矩阵H

    参数:
    n1, n2: H_1和H_2的维度
    use_sum: 是否使用多个循环矩阵的和来生成H_1和H_2

    返回:
    numpy数组: 完整的校验矩阵H
    """
    # 生成H_1和H_2
    if use_sum:
        H1 = generate_sum_of_cyclic_matrices(n1,2)
        H2 = generate_sum_of_cyclic_matrices(n2,2)
    else:
        H1 = generate_cyclic_matrix(n1)
        H2 = generate_cyclic_matrix(n2)

    # 计算H_1和H_2的转置
    H1T = H1.T
    H2T = H2.T

    # 生成单位矩阵
    I_n1 = np.eye(n1, dtype=int)
    I_n2 = np.eye(n2, dtype=int)

    # 计算各部分张量积
    part1 = H1  # H_1^T ⊗ I_{n_2}
    part2 = H2  # I_{n_1} ⊗ H_2
    part3 = H1T  # H_1 ⊗ I_{n_2}
    part4 = H2T  # I_{n_1} ⊗ H_2^T

    # 构建第一行块矩阵
    row1 = np.hstack([part1, part2, part3, part4])

    # 构建第二行块矩阵
    row2 = np.hstack([part4, part3, part2, part1])

    # 合并两行得到最终的校验矩阵H
    H = np.vstack([row1, row2])

    return H, H1, H2


def print_matrix(matrix, name="Matrix"):
    """打印矩阵的辅助函数"""
    print(f"\n{name} ({matrix.shape[0]}x{matrix.shape[1]}):")
    n_rows = min(10, matrix.shape[0])  # 最多打印10行
    n_cols = min(10, matrix.shape[1])  # 最多打印10列

    for i in range(n_rows):
        if matrix.shape[1] <= 10:
            print(' '.join(map(str, matrix[i])))
        else:
            # 对于宽矩阵，只打印前几列和后几列
            print(' '.join(map(str, matrix[i][:5])) + ' ... ' + ' '.join(map(str, matrix[i][-5:])))

    if matrix.shape[0] > 10:
        print("...")


def main():
    """主函数，用于测试生成HGP码校验矩阵"""
    # 设置参数
    n1 = 43  # H_1的维度
    n2 = 43  # H_2的维度
    use_sum = True  # 是否使用多个循环矩阵的和

    # 生成HGP码校验矩阵
    GF=galois.GF(2)
    H, H1, H2 = generate_hgp_check_matrix(n1, n2, use_sum)
    stabilizer_list=[]
    for i in range(len(H)):
        temp=MajoranaOperator(np.where(H[i][0::2]!=0)[0],np.where(H[i][1::2]!=0)[0],1)
        stabilizer_list.append(temp)
    if np.all(np.mod(H@H.T,2)==0):
        if np.linalg.matrix_rank(H)<H.shape[1]//2:
            ones = np.ones(H.shape[1], dtype=int)
            if FiniteFieldSolve(H, ones) is None:
                print('Weight: ',np.count_nonzero(H[0]))
                print('Logical numbers: ',H.shape[1]//2-np.linalg.matrix_rank(GF(H)))
                print('Distance: ')
                QuantumCodeDistance(stabilizer_list, [], H.shape[1] // 2)
            else:
                print(False)


if __name__ == "__main__":
    for i in range(200):
        np.random.seed(i)
        print(i)
        main()
    np.random.seed(3)
    main()


