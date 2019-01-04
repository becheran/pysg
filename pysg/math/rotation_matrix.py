import numpy as np


class RotationMatrix(object):
    def __init__(self, m00, m01, m02, m10, m11, m12, m20, m21, m22):
        self.m00 = m00
        self.m01 = m01
        self.m02 = m02
        self.m10 = m10
        self.m11 = m11
        self.m12 = m12
        self.m20 = m20
        self.m21 = m21
        self.m22 = m22

    @classmethod
    def from_list(cls, matrix_list):
        if len(matrix_list) != 9:
            raise Exception('Array must be length 9 to create matrix form list')
        return cls(matrix_list[0], matrix_list[1], matrix_list[2], matrix_list[3], matrix_list[4], matrix_list[5],
                   matrix_list[6], matrix_list[7], matrix_list[8])

    @classmethod
    def from_sparse_matrix(cls, sparse_matrix):
        if len(sparse_matrix) != 6:
            raise Exception('Array must be length 6 to create matrix form sparse matrix')
        v1 = sparse_matrix[0:3]
        v2 = sparse_matrix[3:6]
        v3 = np.cross(v1, v2).tolist()
        return cls(v1[0], v1[1], v1[2], v2[0], v2[1], v2[2], v3[0], v3[1], v3[2])

    def to_list(self):
        return [self.m00, self.m01, self.m02, self.m10, self.m11, self.m12, self.m20, self.m21, self.m22]

    # From http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/index.htm
    def to_quaternion(self):
        tr = self.m00 + self.m11 + self.m22
        if tr > 0:
            S = np.sqrt(tr + 1.0) * 2  # S = 4 * w
            w = 0.25 * S
            x = (self.m21 - self.m12) / S
            y = (self.m02 - self.m20) / S
            z = (self.m10 - self.m01) / S
        elif (self.m00 > self.m11) and (self.m00 > self.m22):
            S = np.sqrt(1.0 + self.m00 - self.m11 - self.m22) * 2  # S = 4 * x
            w = (self.m21 - self.m12) / S
            x = 0.25 * S
            y = (self.m01 + self.m10) / S
            z = (self.m02 + self.m20) / S
        elif self.m11 > self.m22:
            S = np.sqrt(1.0 + self.m11 - self.m00 - self.m22) * 2  # S = 4 * y
            w = (self.m02 - self.m20) / S
            x = (self.m01 + self.m10) / S
            y = 0.25 * S
            z = (self.m12 + self.m21) / S
        else:
            S = np.sqrt(1.0 + self.m22 - self.m00 - self.m11) * 2  # S = 4 * z
            w = (self.m10 - self.m01) / S
            x = (self.m02 + self.m20) / S
            y = (self.m12 + self.m21) / S
            z = 0.25 * S
        return x, y, z, w

    def print(self):
        s = '[{:2.2},{:2.2},{:2.2}\n{:2.2},{:2.2},{:2.2}\n{:2.2},{:2.2},{:2.2}\n]'.format(self.m00, self.m01, self.m02,
                                                                                          self.m10, self.m11, self.m12,
                                                                                          self.m20, self.m21, self.m22)
        print(s)

    def normalize(self):
        try:
            m = self.to_list()
            m = np.reshape(m, (3, 3))
            u, s, vh = np.linalg.svd(m, full_matrices=False)
            m_orthogonal = np.matmul(u, vh)

            # Make sure that determinant equals one
            det = np.linalg.det(m_orthogonal)
            if det < 0:
                m_orthogonal = np.negative(m_orthogonal)
            m_orthogonal = m_orthogonal.flatten()
            self.m00 = m_orthogonal[0]
            self.m01 = m_orthogonal[1]
            self.m02 = m_orthogonal[2]
            self.m10 = m_orthogonal[3]
            self.m11 = m_orthogonal[4]
            self.m12 = m_orthogonal[5]
            self.m20 = m_orthogonal[6]
            self.m21 = m_orthogonal[7]
            self.m22 = m_orthogonal[8]
        except np.linalg.LinAlgError:
            print("Normalization was not possible. SVD is not possible for matrix.")
            self.print()

    @staticmethod
    def orthonormalize_sparse_matrix(sparse_matrix):
        try:
            sparse_matrix = np.reshape(sparse_matrix, (2, 3))
            u, s, vh = np.linalg.svd(sparse_matrix, full_matrices=False)
            m_orthogonal = np.matmul(u, vh)
            return m_orthogonal.flatten().tolist()
        except np.linalg.LinAlgError:
            print("Normalization was not possible. SVD is not possible for sparse matrix.")
            print(sparse_matrix)
