import copy
import galois
import numpy as np


class BinaryArray:
    GF=galois.GF(2**1)

    # %%  USER：生成函数
    """
    self.array：array of GF(2)对象，01数组
    self.location：array of tuple or list对象，1所在数组的位置
    self.shape：tuple of int对象，数组的规格
    """
    def __init__(self,array):
        self.array = self.GF(np.array(array,dtype=int))
        self.location=np.where(self.array==1)[0]
        self.shape=self.array.shape


    # %%  USER：重载加法运算符
    """
    input.other：BitSpace对象
    output：BitSpace对象
    """
    def __add__(self,other):
        assert isinstance(other, BinaryArray)
        assert self.shape == other.shape
        return BinaryArray(self.array + other.array)


    # %%  USER：重载减法运算符
    """
    input.other：BitSpace对象
    output：BitSpace对象
    """
    def __sub__(self,other):
        assert isinstance(other, BinaryArray)
        assert self.shape == other.shape
        return BinaryArray(self.array - other.array)


    # %%  USER：重载乘法运算符
    """
    input.other：BitSpace对象
    output：BitSpace对象
    """
    def __mul__(self,other):
        assert isinstance(other, BinaryArray)
        assert self.shape == other.shape
        return BinaryArray(self.array * other.array)


    # %%  USER：重载右乘法运算符
    """
    input.other：BitSpace对象
    output：BitSpace对象
    """
    def __rmul__(self,other):
        assert isinstance(other, BinaryArray)
        assert self.shape == other.shape
        assert len(self.shape)==len(other.shape)==1
        return BinaryArray(self.array * other.array)


    # %%  USER：重载矩阵乘法运算符
    """
    input.other：BitSpace对象
    output：BitSpace对象
    """
    def __matmul__(self,other):
        assert isinstance(other, BinaryArray)
        return np.dot(self.array,other.array)


    # %%  USER：重载输出运算符
    """
    output：string对象
    """
    def __str__(self):
        return 'Shape: '+str(self.shape)+'; Location: '+str(self.location)+' Array: '+str(self.array)


    # %%  USER：求解有限域线性方程
    """
    input.vectors：BitSpace对象，01矩阵，被组合的向量组
    input.target：BitSpace对象，01向量，目标向量
    output：BitSpace or None对象，01向量，组合系数
    """
    @ staticmethod
    def solve(vectors, target):
        assert isinstance(target, BinaryArray)
        assert len(target.shape) == 1
        assert vectors.shape[1] == target.shape[0]

        vectors = vectors.array
        target = np.array(target, dtype=int)
        m, n = vectors.shape[0], target.shape[0]

        A = np.vstack(vectors).T
        aug = np.hstack([A, target.reshape(-1, 1)])  # n x (m+1)
        rank = 0

        for col in range(m):
            # 找主元
            rows_with_one = np.where(aug[rank:, col] == 1)[0]
            if rows_with_one.size == 0:
                continue
            pivot = rank + rows_with_one[0]
            # 行交换
            if pivot != rank:
                aug[[rank, pivot]] = aug[[pivot, rank]]
            # 消元
            mask = (aug[:, col] == 1) & (np.arange(aug.shape[0]) != rank)
            aug[mask] ^= aug[rank]
            rank += 1

        solution = np.zeros(m, dtype=int)
        for r in range(rank):
            row = aug[r, :m]
            idx = np.where(row == 1)[0]
            if idx.size == 0:
                continue
            pc = idx[0]
            val = aug[r, -1]
            if pc + 1 < m:
                val ^= np.dot(row[pc + 1:], solution[pc + 1:]) % 2
            solution[pc] = val

        if not np.all((np.dot(A, solution) % 2) == target):
            return None
        return BinaryArray(solution.tolist())


    # %%  USER：求两个向量空间交空间的基矢组
    """
    input.basis1：BitSpace对象，01矩阵，基矢组
    input.basis2：BitSpace对象，01矩阵，基矢组
    output：BitSpace or None对象，01矩阵，基矢组
    """
    @staticmethod
    def cap(basis1, basis2):
        assert isinstance(basis1, BinaryArray)
        assert isinstance(basis2, BinaryArray)
        GF2 = galois.GF(2)

        # 转化为GF2数组
        basis1 = basis1.array
        basis2 = basis2.array

        m = basis1.shape[0]
        k = basis2.shape[0]

        # 解方程 basis1^T * x + basis2^T * y = 0 (表示交集向量)
        # 构造矩阵 [basis1^T | basis2^T]
        aug_matrix = GF2(np.concatenate((basis1.T, basis2.T), axis=1))

        # 计算零空间（解空间）
        nullspace = aug_matrix.null_space()

        # 从零空间中取对应于每一组自变量两部分中对应于 basis1 的分量在这里获得解的a区段
        ab_space = nullspace[:, :m]

        # 将系数乘以 basis1 得到具体解（交集）
        if len(ab_space) == 0:
            return GF2.Zeros((0, basis1.shape[1]))

        intersection_vectors = ab_space @ basis1

        # 计算行相关即进行矩阵的高斯消元
        rref_intersection = intersection_vectors.row_reduce()

        # 除去全0行的行（即为没有有用基底捕获的时候）
        nz_mask = np.any(rref_intersection != 0, axis=1)
        rref_basis = rref_intersection[nz_mask]

        return BinaryArray(rref_basis)


    # %%  USER：求两个向量空间差空间的基矢组
    """
    input.basis1：BitSpace对象，01矩阵，基矢组，被减空间
    input.basis2：BitSpace对象，01矩阵，基矢组，减空间
    output：BitSpace or None对象，01矩阵，基矢组
    """
    @staticmethod
    def minus(basis1, basis2):
        assert isinstance(basis1, BinaryArray)
        assert isinstance(basis2, BinaryArray)
        GF2 = galois.GF(2)

        # 转化为GF2数组
        intersect = BinaryArray.cap(basis1, basis2).array
        basis1 = basis1.array

        if len(intersect) == 0:
            return basis1

        result = []
        for i in range(len(basis1)):
            rank = np.linalg.matrix_rank(intersect)
            intersect = np.vstack((intersect, basis1[i]))
            if np.linalg.matrix_rank(intersect) > rank:
                result.append(basis1[i])

        return GF2(np.array(result, dtype=int))


    # %%  USER：数组堆叠
    """
    input.case_list：list of BitSpace对象
    output：BitSpace，堆叠结果
    """
    @ staticmethod
    def vstack(case_list):
        assert isinstance(case_list, list)
        case_list=copy.deepcopy(case_list)
        first=case_list[0]
        temp=first.array
        for i in range(1,len(case_list)):
            temp=np.vstack([temp,case_list[i].array])
        return BinaryArray(temp)


    # %%  USER：向量内积运算
    """
    input.other：BitSpace对象
    output：GF(2)对象，内积结果
    """
    @ staticmethod
    def inner(self,other):
        assert isinstance(other, BinaryArray)
        assert self.shape == other.shape
        assert len(self.shape)==len(other.shape)==1
        return np.sum(self.array*other.array)


    # %%  USER：求向量空间的正交化基矢组
    """
    input.origin：BitSpace对象，待正交化的基矢组
    output：BitSpace，正交化结果
    """
    @ staticmethod
    def orthogonalize(self):
        vectors=self.array

        def gf2_gram_schmidt(vectors, bilinear_form):
            o_i = None
            GF2 = galois.GF2
            k = len(vectors)
            # 复制向量以避免修改原始数据
            B_i = [v.copy() for v in vectors]
            O = []  # 存储正交基

            for i in range(k):
                # 1. 优先选择非迷向向量
                non_isotropic_found = False
                for idx in range(len(B_i)):
                    if bilinear_form(B_i[idx], B_i[idx]) != GF2(0):
                        if idx != 0:
                            B_i[0], B_i[idx] = B_i[idx], B_i[0]
                        non_isotropic_found = True
                        break

                b1 = B_i[0]
                if non_isotropic_found:
                    o_i = b1
                else:
                    # 2. 尝试构造非迷向向量
                    found = False
                    for j in range(1, len(B_i)):
                        b_j = B_i[j]
                        if bilinear_form(b1, b_j) != GF2(0):
                            v = b1 + b_j
                            if bilinear_form(v, v) != GF2(0):
                                o_i = v
                                found = True
                                break
                    if not found:
                        o_i = b1

                O.append(o_i)

                # 3. 更新剩余向量
                next_B = []
                for j in range(1, len(B_i)):
                    b = B_i[j]
                    coef = bilinear_form(b, o_i)
                    b_new = b + coef * o_i
                    next_B.append(b_new)

                B_i = next_B

            return O

        ##  双线性形式矩阵
        bilinear_form1 = lambda u, v: np.dot(u, v)
        ortho_basis1 = gf2_gram_schmidt(vectors, bilinear_form1)
        judge_matrix = np.zeros((len(ortho_basis1), len(ortho_basis1)))
        for i in range(len(ortho_basis1)):
            for j in range(len(ortho_basis1)):
                judge_matrix[i, j] = np.dot(ortho_basis1[i], ortho_basis1[j])

        ##  判断是否存在正交基
        flag_0 = np.trace(judge_matrix)
        flag_1 = np.count_nonzero(judge_matrix)
        assert flag_0==flag_1

        ##  输出结果
        return BinaryArray(ortho_basis1)


    # %%  USER：基于数组生成BitSpace对象
    """
    input.array：np.array对象
    output：BitSpace对象
    """
    @ classmethod
    def ValueDefine(cls,array):
        return cls(array)


    # %%  USER：基于1的位置生成BitSpace对象
    """
    input.array：np.array对象
    output：BitSpace对象
    """
    @ classmethod
    def LocationDefine(cls,location_list,length):
        temp=cls.GF(np.zeros(length,dtype=int))
        location=np.array(location_list,dtype=int)
        temp[location]=1
        return cls(temp)


    # %%  USER：求零空间
    """
    output：BitSpace对象，零空间向量基矢
    """
    def null_space(self):
        result=self.array.null_space()
        return BinaryArray(result)


    # %%  USER：求行空间的秩
    """
    output：int对象，行空间秩的大小
    """
    def get_rank(self):
        return np.linalg.matrix_rank(self.array)
