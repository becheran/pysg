from unittest import TestCase

import numpy as np
from pyrr import Vector3, Quaternion

from pysg import Node3D
from pysg.testing import CustomAssertions


class TestNode3D(TestCase, CustomAssertions):
    def setUp(self):
        # Root
        #   |  \
        #  C_1, Child_2
        #        /  \
        #     C_2_1 C_2_2

        self.root = Node3D("root")
        self.child_1 = Node3D("child_1")
        self.child_2 = Node3D("child_2")
        self.child_2_1 = Node3D("child_2_1")
        self.child_2_2 = Node3D("child_2_2")
        self.root.add(self.child_1)
        self.root.add(self.child_2)
        self.child_2.add(self.child_2_1)
        self.child_2.add(self.child_2_2)

    def test_local_position_updates_world(self):
        self.child_1.local_position = [1, 0, 0]
        self.assertEqual(self.child_1.local_position, self.child_1.world_position)

    def test_init_world_position(self):
        self.root.world_position = Vector3([1, 0, 0])
        child = Node3D()
        child.local_position = Vector3([1, 0, 0])
        self.root.add(child)
        # Child local position is now relative to parent
        self.assertEqual(0, child.local_position[0])

    def test_position_change_hierarchy(self):
        self.root.local_position += 1
        self.assertEqual(self.root.local_position, self.child_2_2.world_position)
        self.child_2.local_position += 1
        self.assertEqual(self.child_2.world_position, self.child_2_2.world_position)
        self.assertEqual(self.root.world_position, self.child_1.world_position)

    def test_rotate_x_1(self):
        self.root.rotate_x(180)
        self.assertQuaternionAreEqual(self.root.local_quaternion, Quaternion([1, 0, 0, 0]))

    def test_rotate_x_2(self):
        self.root.rotate_x(360)
        self.assertQuaternionAreEqual(self.root.local_quaternion, Quaternion([0, 0, 0, 1]))

    def test_rotate_x_3(self):
        self.root.rotate_x(720)
        self.assertQuaternionAreEqual(self.root.local_quaternion, Quaternion([0, 0, 0, 1]))

    def test_rotate_y_1(self):
        self.root.rotate_y(180)
        self.assertQuaternionAreEqual(self.root.local_quaternion, Quaternion([0, 1, 0, 0]))

    def test_rotate_y_2(self):
        self.root.rotate_y(360)
        self.assertQuaternionAreEqual(self.root.local_quaternion, Quaternion([0, 0, 0, 1]))

    def test_rotate_z_1(self):
        self.root.rotate_z(180)
        self.assertQuaternionAreEqual(self.root.local_quaternion, Quaternion([0, 0, 1, 0]))

    def test_rotate_z_2(self):
        self.root.rotate_z(360)
        self.assertQuaternionAreEqual(self.root.local_quaternion, Quaternion([0, 0, 0, 1]))

    def test_rotate_z_3(self):
        self.root.rotate_z(720)
        self.assertQuaternionAreEqual(self.root.local_quaternion, Quaternion([0, 0, 0, 1]))

    def test_rotate_z_4(self):
        self.root.rotate_z(180, local_space=False)
        self.assertQuaternionAreEqual(self.root.local_quaternion, Quaternion([0, 0, 1, 0]))
        self.assertQuaternionAreEqual(self.root.world_quaternion, Quaternion([0, 0, 1, 0]))

    def test_euler_1(self):
        self.root.local_euler_angles = Vector3([180, 0, 0])
        self.assertQuaternionAreEqual(self.root.local_quaternion, Quaternion([1, 0, 0, 0]))

    def test_euler_2(self):
        self.child_1.local_euler_angles = Vector3([80, 40, 10])
        np.testing.assert_almost_equal(np.array(self.child_1.local_euler_angles), np.array([80, 40, 10]))

    def test_euler_3(self):
        self.child_2.local_euler_angles = Vector3([180, 0, 0])
        self.assertQuaternionAreEqual(self.child_2.local_quaternion, Quaternion([1, 0, 0, 0]))

    def test_euler_4(self):
        angles = Vector3([45, 78, 54])
        self.child_2.local_euler_angles = angles
        np.testing.assert_almost_equal(np.array(self.child_2.local_euler_angles), np.array(angles))

    def test_quaternion_1(self):
        self.root.local_quaternion = [0.5, 0.5, 0.5, 0.5]
        self.assertQuaternionAreEqual(self.child_2.world_quaternion, self.root.local_quaternion)

    def test_quaternion_2(self):
        self.root.local_quaternion = [-0.5, 0.5, 0.5, 0.5]
        self.assertQuaternionAreEqual(self.child_2.world_quaternion, self.root.local_quaternion)

    def test_quaternion_3(self):
        self.root.world_quaternion = [-0.5, 0.5, 0.5, 0.5]
        self.assertQuaternionAreEqual(self.child_2.world_quaternion, self.root.local_quaternion)

    def test_quaternion_4(self):
        self.root.world_quaternion = [1, 0, 0, 0]
        self.child_2.local_quaternion = [1, 0, 0, 0]
        self.assertQuaternionAreEqual(self.child_2.world_quaternion, Quaternion([0, 0, 0, 1]))

    def test_scale_1(self):
        self.root.scale = Vector3([1., 2., 3.])
        np.testing.assert_almost_equal(np.array(self.root.scale), np.array([1., 2., 3.]))

    def test_scale_2(self):
        self.root.scale *= 2.
        np.testing.assert_almost_equal(np.array(self.root.scale), np.array([2., 2., 2.]))

    def test_scale_3(self):
        self.root.scale *= -2.
        np.testing.assert_almost_equal(np.array(self.root.scale), np.array([-2., -2., -2.]))

    def test_position_1(self):
        self.root.local_position += 2.
        np.testing.assert_almost_equal(np.array(self.root.local_position), np.array([2., 2., 2.]))
        np.testing.assert_almost_equal(np.array(self.root.world_position), np.array([2., 2., 2.]))

    def test_position_2(self):
        self.root.local_position += 2.
        np.testing.assert_almost_equal(np.array(self.child_1.world_position), np.array([2., 2., 2.]))
        np.testing.assert_almost_equal(np.array(self.child_2_1.world_position), np.array([2., 2., 2.]))

    def test_add_1(self):
        new_child = Node3D("new_child")
        self.root.add(new_child)
        self.assertEqual(new_child.parent, self.root)

    def test_add_2(self):
        new_child = Node3D("new_child")
        new_child.local_position = Vector3([1, 2, 3])
        np.testing.assert_almost_equal(np.array(new_child.world_position), np.array([1., 2., 3.]))
        self.root.local_position = Vector3([1, 1, 1])
        self.root.add(new_child)
        np.testing.assert_almost_equal(np.array(new_child.local_position), np.array([0., 1., 2.]))
        np.testing.assert_almost_equal(np.array(new_child.world_position), np.array([1., 2., 3.]))

    def test_remove(self):
        new_child = Node3D("new_child")
        self.root.add(new_child)
        self.assertTrue(new_child in self.root.children)
        self.root.remove(new_child)
        self.assertEqual(new_child.parent, None)
        self.assertFalse(new_child in self.root.children)
