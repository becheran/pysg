from unittest import TestCase

from pyrr import Vector3, Quaternion

from pysg.math import quaternion_are_equal
from pysg.node_3d import Node3D


class TestNode3D(TestCase):
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
        self.assertTrue(quaternion_are_equal(self.root.local_quaternion, Quaternion([1, 0, 0, 0])))

    def test_rotate_x_2(self):
        self.root.rotate_x(360)
        self.assertTrue(quaternion_are_equal(self.root.local_quaternion, Quaternion([0, 0, 0, 1])))

    def test_rotate_x_3(self):
        self.root.rotate_x(720)
        self.assertTrue(quaternion_are_equal(self.root.local_quaternion, Quaternion([0, 0, 0, 1])))

    def test_rotate_y_1(self):
        self.root.rotate_y(180)
        self.assertTrue(quaternion_are_equal(self.root.local_quaternion, Quaternion([0, 1, 0, 0])))

    def test_rotate_y_2(self):
        self.root.rotate_y(360)
        self.assertTrue(quaternion_are_equal(self.root.local_quaternion, Quaternion([0, 0, 0, 1])))

    def test_rotate_z_1(self):
        self.root.rotate_z(180)
        self.assertTrue(quaternion_are_equal(self.root.local_quaternion, Quaternion([0, 0, 1, 0])))

    def test_rotate_z_2(self):
        self.root.rotate_z(360)
        self.assertTrue(quaternion_are_equal(self.root.local_quaternion, Quaternion([0, 0, 0, 1])))

    def test_rotate_z_3(self):
        self.root.rotate_z(720)
        self.assertTrue(quaternion_are_equal(self.root.local_quaternion, Quaternion([0, 0, 0, 1])))

    def test_rotate_z_4(self):
        self.root.rotate_z(180, local_space=False)
        self.assertTrue(quaternion_are_equal(self.root.local_quaternion, Quaternion([0, 0, 0, 1])))
        self.assertTrue(quaternion_are_equal(self.root.world_quaternion, Quaternion([0, 0, 1, 0])))

    def test_scale(self):
        self.fail()