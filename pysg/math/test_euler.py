from unittest import TestCase

import numpy as np

from src.scene.rotation.euler import Euler


class TestEuler(TestCase):
    def test_to_list(self):
        in_list = [1, 0, 0]
        euler = Euler.from_list(in_list)
        out_list = euler.to_list()
        self.assertEqual(in_list, out_list)

    def test_to_quaternion(self):
        # from https://www.andre-gaschler.com/rotationconverter/ Angle order YZX. -> Put 231 order
        euler_in_list = [[1.595304, -0.5412123, -0.0152541],
                         [-1.3826454, 1.0547636, 2.9281693]]
        quaternion_out_list = [[-0.1964498, 0.6910764, -0.1814247, 0.6714953],
                               [0.627765, 0.3268382, 0.5890927, 0.3899457]]
        for e, q in zip(euler_in_list, quaternion_out_list):
            euler = Euler.from_list(e)
            quaternion = euler.to_quaternion()
            self.assertTrue(np.allclose(q, quaternion))
