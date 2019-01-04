from unittest import TestCase

import numpy as np

from src.scene.rotation.rotation_matrix import RotationMatrix


class TestRotationMatrix(TestCase):
    def test_from_sparse_matrix(self):
        rm = RotationMatrix.from_sparse_matrix([0.2496954, 0.4155630, -0.8746197, 0.6188338, 0.6262304, 0.4742154])
        self.assertTrue(np.allclose(rm.to_list(),
                                    [0.2496954, 0.4155630, -0.8746197, 0.6188338, 0.6262304, 0.4742154, 0.7447797,
                                     -0.6596537,
                                     -0.1007976]))

    def test_to_list(self):
        input_rotation_list = [0.2496954, 0.4155630, -0.8746197, 0.6188338, 0.6262304, 0.4742154, 0.7447797,
                               -0.6596537, -0.1007976]
        rm = RotationMatrix.from_list(input_rotation_list)
        self.assertTrue(np.allclose(rm.to_list(), input_rotation_list))

    def test_to_quaternion(self):
        rotation_matrix_in_list = [[-0.8953739, 0.4367030, 0.0871557,
                                    0.3210425, 0.4973881, 0.8059384,
                                    0.3086055, 0.7495969, -0.5855486],
                                   [0.0000000, -0.0000000, -1.0000000,
                                    -0.9848077, 0.1736482, -0.0000000,
                                    0.1736482, 0.9848077, 0.0000000],
                                   [-0.0210030, -0.0278720, 0.9993908,
                                    -0.5151754, 0.8569850, 0.0130736,
                                    -0.8568274, -0.5145870, -0.0323583]]
        quaternion_out_list = [[0.2195373, 0.8628891, 0.4506765, -0.0641594],
                               [0.4545195, -0.5416752, -0.4545195, 0.5416752],
                               [-0.1964498, 0.6910764, -0.1814247, 0.6714953]]
        for m, q in zip(rotation_matrix_in_list, quaternion_out_list):
            matrix = RotationMatrix.from_list(m)
            quaternion = matrix.to_quaternion()
            self.assertTrue(np.allclose(q, quaternion))

    def test_normalize(self):
        np.random.seed(42)
        wrong_rotation_matrix_list = [np.random.rand(3, 3), np.random.rand(3, 3), np.random.rand(3, 3)]
        for m in wrong_rotation_matrix_list:
            matrix = RotationMatrix.from_list(m.flatten())
            matrix.normalize()
            det = np.linalg.det(np.array(matrix.to_list()).reshape(3, 3))
            self.assertTrue(np.allclose(det, 1))

    def test_normalize_sparse_matrix(self):
        np.random.seed(42)
        wrong_rotation_matrix_list = [np.random.rand(2, 3), np.random.rand(2, 3), np.random.rand(2, 3)]
        for m in wrong_rotation_matrix_list:
            normalized_matrix = np.array(RotationMatrix.orthonormalize_sparse_matrix(m.flatten().tolist()))
            dot = np.dot(normalized_matrix.reshape(2, 3)[0], normalized_matrix.reshape(2, 3)[1])
            self.assertTrue(np.allclose(dot, 0))
