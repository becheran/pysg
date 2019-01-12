from unittest import TestCase

from pyrr import Vector3

from pysg.error import PyrrTypeError
from pysg.util import pyrr_type_checker


class TestUtil(TestCase):
    def test_pyrr_type_checker_fail(self):
        in_var = [2, 1, 2, 4]
        with self.assertRaises(PyrrTypeError):
            pyrr_type_checker(in_var, Vector3)

    def test_pyrr_type_checker_success(self):
        in_var = [2, 1, 2]
        checked_var = pyrr_type_checker(in_var, Vector3)
        self.assertEqual(Vector3, type(checked_var))
