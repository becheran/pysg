from unittest import TestCase

import numpy as np
from pyrr import Vector3

from pysg.error import PyrrTypeError
from pysg.testing import CustomAssertions
from pysg.util import pyrr_type_checker, parameters_as_angles_deg_to_rad


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
