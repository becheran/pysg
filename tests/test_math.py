from unittest import TestCase

import numpy as np
import pyrr
from pyrr import Quaternion, Vector3

from pysg.math import ray_intersect_sphere, quaternion_are_equal, euler_angles_to_quaternion, quaternion_to_euler_angles
from pysg.testing import CustomAssertions


class TestMath(TestCase, CustomAssertions):
    def test_ray_intersect_sphere_no_solution_1(self):
        ray = pyrr.ray.create([0, 2, 0], [1, 0, 0])
        sphere = pyrr.sphere.create([0, 0, 0], 1)
        intersections = ray_intersect_sphere(ray, sphere)
        self.assertEqual(len(intersections), 0)

    def test_ray_intersect_sphere_no_solution_2(self):
        ray = pyrr.ray.create([0, 0, 0], [1, 0, 0])
        sphere = pyrr.sphere.create([0, 2, 0], 1)
        intersections = ray_intersect_sphere(ray, sphere)
        self.assertEqual(len(intersections), 0)

    def test_ray_intersect_sphere_one_solution_1(self):
        ray = pyrr.ray.create([0, 0, 0], [1, 0, 0])
        sphere = pyrr.sphere.create([0, 0, 0], 1)
        intersections = ray_intersect_sphere(ray, sphere)
        self.assertEqual(len(intersections), 1)
        np.testing.assert_array_almost_equal(intersections[0], np.array([1, 0, 0]), decimal=2)

    def test_ray_intersect_sphere_two_solutions_1(self):
        ray = pyrr.ray.create([-2, 0, 0], [1, 0, 0])
        sphere = pyrr.sphere.create([0, 0, 0], 1)
        intersections = ray_intersect_sphere(ray, sphere)
        self.assertEqual(len(intersections), 2)
        np.testing.assert_array_almost_equal(intersections[0], np.array([1, 0, 0]), decimal=2)
        np.testing.assert_array_almost_equal(intersections[1], np.array([-1, 0, 0]), decimal=2)

    def test_ray_intersect_sphere_two_solutions_2(self):
        ray = pyrr.ray.create([2.48, 1.45, 1.78], [-3.1, 0.48, -3.2])
        sphere = pyrr.sphere.create([1, 1, 0], 1)
        intersections = ray_intersect_sphere(ray, sphere)
        self.assertEqual(len(intersections), 2)
        np.testing.assert_array_almost_equal(intersections[0], np.array([0.44, 1.77, -0.32]), decimal=2)
        np.testing.assert_array_almost_equal(intersections[1], np.array([1.41, 1.62, 0.67]), decimal=2)

    def test_quaternion_are_equal_1(self):
        self.assertTrue(quaternion_are_equal(Quaternion([1, 0, 0, 0]), Quaternion([-1, 0, 0, 0])))

    def test_quaternion_are_equal_2(self):
        self.assertFalse(quaternion_are_equal(Quaternion([0, 1, 0, 0]), Quaternion([-1, 0, 0, 0])))

    def test_quaternion_are_equal_3(self):
        self.assertTrue(quaternion_are_equal(Quaternion([1, 0, 0, 0]), Quaternion([1, 0, 0, 0])))

    def test_euler_to_quaternion_1(self):
        v = np.radians(Vector3([0, 0, 0]))
        self.assertQuaternionAreEqual(euler_angles_to_quaternion(v), (Quaternion([0, 0, 0, 1])))
        v = np.radians([0, 0, 180])
        self.assertQuaternionAreEqual(euler_angles_to_quaternion(v), (Quaternion([0, 0, 1, 0])))
        v = np.radians([0, 180, 0])
        self.assertQuaternionAreEqual(euler_angles_to_quaternion(v), (Quaternion([0, 1, 0, 0])))
        v = np.radians([180, 0, 0])
        self.assertQuaternionAreEqual(euler_angles_to_quaternion(v), (Quaternion([1, 0, 0, 0])))

    def test_euler_to_quaternion_2(self):
        v = np.radians([0, 0, 360])
        self.assertQuaternionAreEqual(euler_angles_to_quaternion(v), (Quaternion([0, 0, 0, 1])))

    def test_euler_to_quaternion_3(self):
        v = np.radians(Vector3([90, 70, 45]))
        e = euler_angles_to_quaternion(v)
        self.assertQuaternionAreEqual(e, Quaternion([0.6903455, 0.5963678, -0.1530459, 0.3799282]), epsilon=1e-5)

    def test_quaternion_to_euler_1(self):
        q = Quaternion([0, 0, 0, 1])
        e = quaternion_to_euler_angles(q)
        np.testing.assert_almost_equal(np.array(e), np.array([0., 0., 0.]))

    def test_quaternion_to_euler_2(self):
        q = Quaternion([0, 0, 1, 0])
        e = quaternion_to_euler_angles(q)
        # Rotation [180, 180, 0] and [0,0,180] are the same thing.
        np.testing.assert_almost_equal(np.array(e), np.array([180., 180., 0.]))

    def test_quaternion_to_euler_3(self):
        q = Quaternion([0, 1, 0, 0])
        e = quaternion_to_euler_angles(q)
        np.testing.assert_almost_equal(np.array(e), np.array([0., 180., 0.]))

    def test_quaternion_to_euler_4(self):
        q = Quaternion([1, 0, 0, 0])
        e = quaternion_to_euler_angles(q)
        np.testing.assert_almost_equal(np.array(e), np.array([180., 0., 0.]))

    def test_quaternion_to_euler_5(self):
        q = Quaternion([0.3711136, 0.0742227, 0.519559, 0.7660444])
        e = quaternion_to_euler_angles(q)
        np.testing.assert_almost_equal(np.array(e), np.array([69.4060045, -31.1935729, 58.3315948]), decimal=5)
