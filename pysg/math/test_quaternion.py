from unittest import TestCase

import numpy as np

from src.scene.rotation.quaternion import Quaternion


class TestQuaternion(TestCase):
    def test_to_list(self):
        in_list = [0, 1, 0, 1]
        q = Quaternion.from_list(in_list)
        out_list = q.to_list()
        self.assertFalse(in_list != out_list)

    def test_to_axis_angle(self):
        quaternion_in_list = [[-0.1964498, 0.6910764, -0.1814247, 0.6714953],
                              [0.627765, 0.3268382, 0.5890927, 0.3899457],
                              [0.1041695, -0.1699891, -0.5120093, 0.8355232]]
        axis_angle_out = [[-0.4425087, 1.5566688, -0.4086643],
                          [1.5955588, 0.8307083, 1.4972673],
                          [0.2205699, -0.3599373, -1.0841355]]
        for q, aa in zip(quaternion_in_list, axis_angle_out):
            quaternion = Quaternion.from_list(q)
            conv_axis_angle = quaternion.to_axis_angle()
            self.assertTrue(np.allclose(aa, conv_axis_angle))

    def test_to_matrix(self):
        quaternion_in_list = [[-0.1964498, 0.6910764, -0.1814247, 0.6714953],
                              [0.627765, 0.3268382, 0.5890927, 0.3899457],
                              [0.1041695, -0.1699891, -0.5120093, 0.8355232]]
        matrix_out = [[-0.0210030, -0.0278720, 0.9993908,
                       -0.5151754, 0.8569850, 0.0130736,
                       -0.8568274, -0.5145870, -0.0323583],
                      [0.0922932, -0.0490731, 0.9945219,
                       0.8697836, -0.4822382, -0.1045125,
                       0.4847252, 0.8746646, -0.0018243],
                      [0.4179005, 0.8201758, -0.3907311,
                       -0.8910065, 0.4539905, -0.0000000,
                       0.1773882, 0.3481440, 0.9205049]]
        for q, m in zip(quaternion_in_list, matrix_out):
            quaternion = Quaternion.from_list(q)
            conv_matrix = quaternion.to_rotation_matrix()
            self.assertTrue(np.allclose(m, conv_matrix, atol=1.e-4))

    def test_to_euler_angles(self):
        quaternion_in_list = [[-0.1964498, 0.6910764, -0.1814247, 0.6714953],
                              [0.627765, 0.3268382, 0.5890927, 0.3899457],
                              [0.1041695, -0.1699891, -0.5120093, 0.8355232]]
        # from https://www.andre-gaschler.com/rotationconverter/ Angle order YZX. -> Put 231 order
        euler_out = [[1.595304, -0.5412123, -0.0152541],
                     [-1.3826454, 1.0547636, 2.9281693],
                     [-0.4014257, -1.0995574, 0.0]]
        for q, e in zip(quaternion_in_list, euler_out):
            quaternion = Quaternion.from_list(q)
            conv_euler = quaternion.to_euler_angles()
            self.assertTrue(np.allclose(e, conv_euler, atol=1.e-4))

    def test_multiplication(self):
        a = Quaternion(-0.1964498, 0.6910764, -0.1814247, 0.6714953)
        b = Quaternion(0.627765, 0.3268382, 0.5890927, 0.3899457)
        a_inv = a.inverse()
        ab = a * b
        ba = b * a
        ca = a_inv * a
        cb = a_inv * b
        self.assertTrue(np.allclose(ab.to_list(), [0.811341, 0.4907876, -0.1732137, 0.2661768], atol=1.e-4))
        self.assertTrue(np.allclose(ba.to_list(), [-0.1214681, 0.4871175, 0.822868, 0.2661768], atol=1.e-4))
        self.assertTrue(np.allclose(ba.to_list(), [-0.1214681, 0.4871175, 0.822868, 0.2661768], atol=1.e-4))
        self.assertTrue(np.allclose(ca.to_list(), [0, 0, 0, 1], atol=1.e-4))
        self.assertTrue(np.allclose(cb.to_list(), [0.03174144, -0.051847, 0.9643596, 0.25751], atol=1.e-4))

    def test_inverse(self):
        a = Quaternion(-0.1964498, 0.6910764, -0.1814247, 0.6714953)
        a_inv = a.inverse()
        self.assertTrue(np.allclose(a_inv.to_list(), [0.1964498, -0.6910764, 0.1814247, 0.6714953], atol=1.e-4))

    def test_rotate(self):
        from src.scene.vector3 import Vector3
        q = Quaternion(-0.1964498, 0.6910764, -0.1814247, 0.6714953)
        p = Vector3(1.12, 2.42, -1.88)
        p_new = q.rotate(p)
        self.assertTrue(np.allclose(p_new.to_list(), [-1.969828, 1.472329, -2.144114], atol=1.e-4))
