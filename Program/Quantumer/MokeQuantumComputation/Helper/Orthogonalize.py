import galois
import numpy as np


#%%  USER：GF(2)上的扩展格拉姆-施密特正交化算法
"""
intput.vectors：list of np.array of GF(2)对象，向量基矢
output：list of np.array of GF(2)对象，正交基向量列表
"""

def orthogonalize(vectors):


    #%%  SECTION：正交化方法

    def gf2_gram_schmidt(vectors, bilinear_form):
        o_i = None
        GF2 = galois.GF2
        k = len(vectors)
        # 复制向量以避免修改原始数据
        B_i = [v.copy() for v in vectors]
        O = []  # 存储正交基
        for i in range(k):
            if np.mod(np.count_nonzero(B_i[i]),2)==1:
                for j in range(k):
                    if j != i and np.mod(np.count_nonzero(B_i[j]),2)==0:
                        B_i[j]=B_i[j]+B_i[i]
                break
            if i==k-1:
                print('There is no odd-weight vector')
                return False

        while True:
            length=10000
            b1=None
            flag=None
            for i in range(len(B_i)):
                if length>np.count_nonzero(B_i[i]):
                    b1=B_i[i]
                    flag=i
                    length=np.count_nonzero(B_i[i])

            o_i=b1

            O.append(o_i)

            next_B = []
            for j in range(len(B_i)):
                if j!= flag:
                    b = B_i[j]
                    coef = bilinear_form(b, o_i)
                    b_new = b + coef * o_i
                    next_B.append(b_new)

            B_i = next_B
            if len(B_i)==0:
                return O
            length=len(B_i)
            for i in range(length):
                if np.mod(np.count_nonzero(B_i[i]),2) == 1:
                    for j in range(length):
                        if j != i and np.mod(np.count_nonzero(B_i[j]), 2) == 0:
                            B_i[j] = B_i[j] + B_i[i]
                    break
                if i == len(B_i):
                    return O


    #%%  SECTION：计算双线性形式

    def inner_product(u, v):
        return np.dot(u, v)


    #%%  SECTION：处理正交向量组

    ##  双线性形式矩阵
    bilinear_form1 = lambda u, v: inner_product(u, v)
    ortho_basis1 = gf2_gram_schmidt(vectors, bilinear_form1)
    judge_matrix=np.zeros((len(ortho_basis1), len(ortho_basis1)))
    for i in range(len(ortho_basis1)):
        for j in range(len(ortho_basis1)):
            judge_matrix[i,j] = np.dot(ortho_basis1[i], ortho_basis1[j])

    ##  判断是否存在正交基
    flag_0=np.trace(judge_matrix)
    flag_1=np.count_nonzero(judge_matrix)
    assert flag_0>0
    print("输入向量:", [v.tolist() for v in vectors])
    print("正交基:", [v.tolist() for v in ortho_basis1])

    ##  输出结果
    return ortho_basis1


if __name__ == "__main__":
    GF = galois.GF2
    vectors=[GF(np.array([0,1,1],dtype=int)),GF(np.array([1,1,1],dtype=int)),GF(np.array([1,1,0],dtype=int))]
    orthogonalize(vectors)