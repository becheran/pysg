from unittest import TestCase

from pyrr import Vector3, Quaternion

from pysg.testing import CustomAssertions
from pysg.error import PyrrTypeError
from pysg.math import quaternion_are_equal
from pysg.util import pyrr_type_checker, parameters_as_angles_deg_to_rad
import numpy as np


class TestUtil(TestCase, CustomAssertions):
    def test_pyrr_type_checker_fail(self):
        in_var = [2, 1, 2, 4]
        with self.assertRaises(PyrrTypeError):
            pyrr_type_checker(in_var, Vector3)

    def test_pyrr_type_checker_success(self):
        in_var = [2, 1, 2]
        checked_var = pyrr_type_checker(in_var, Vector3)
        self.assertEqual(Vector3, type(checked_var))

    def test_parameters_as_angles_deg_to_rad(self):
        @parameters_as_angles_deg_to_rad('angle')
        def test(angle, result):
            self.assertAlmostEqual(angle, result, delta=5)

        test(45, 0.785398)
        test(0, 0)
        test(-280, -4.88692)

    def test_parameters_as_angles_deg_to_rad_array(self):
        @parameters_as_angles_deg_to_rad('angle')
        def test(angle, result):
            np.testing.assert_almost_equal(np.array(angle), np.array(result), decimal=5)

        test(Vector3([45, 0, -280]), Vector3([0.785398, 0, -4.88692]))

    def test_quaternion_to_euler_angles(self):
        v = np.radians(Vector3([0, 0, 0]))
        self.assertQuaternionAreEqual(Quaternion.from_eulers(v), (Quaternion([0, 0, 0, 1])))
        v = np.radians([0, 0, 180])
        self.assertQuaternionAreEqual(Quaternion.from_eulers(v), (Quaternion([0, 0, 1, 0])))
        v = np.radians([0, 0, 360])
        self.assertQuaternionAreEqual(Quaternion.from_eulers(v), (Quaternion([0, 0, 0, 1])))
        v = np.radians([90, 70, 45])
        e = Quaternion.from_eulers(v)  # [-0.69034553 -0.15304592  0.15304592  0.69034553]
        print(e)
        self.assertQuaternionAreEqual(Quaternion.from_eulers(v),
                                      Quaternion([0.69034553, 0.15304592, -0.15304592, 0.69034553]))
