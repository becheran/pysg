from unittest import TestCase

import numpy as np
import pyrr

from pysg.math import ray_intersect_sphere


class TestMath(TestCase):
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
