from unittest import TestCase

import numpy as np

from src.scene.rotation.axis_angle import AxisAngle


class TestAxisAngle(TestCase):
    def test_to_list(self):
        in_list = [1, 0, 0]
        aa = AxisAngle.from_list(in_list)
        out_list = aa.to_list()
        self.assertEqual(in_list, out_list)

    def test_to_quaternion(self):
        axis_angle_in_list = [[2.1004758, 1.3459287, 1.4707513],
                              [0.4582703, 2.3068084, -3.5400594],
                              [0.7704549, 1.1376989, 3.0222776]]
        quaternion_out_list = [[0.7198474, 0.4612589, 0.5040365, 0.1225037],
                               [0.0916833, 0.4615087, -0.7082375, -0.5263112],
                               [0.2311454, 0.3413228, 0.9067183, -0.0890646]]
        for aa, q in zip(axis_angle_in_list, quaternion_out_list):
            axis_angle = AxisAngle.from_list(aa)
            quaternion = axis_angle.to_quaternion()
            self.assertTrue(np.allclose(q, quaternion))
