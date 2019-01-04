# -*- coding: utf-8 -*-
"""The root of the scene graph

Transform is added to every node.

"""
from pysg.math.quaternion import Quaternion
from pysg.math.vector3 import Vector3


class Transform:
    """Every object in the scene graph has a transform which indicates the position and rotation in 3D space."""

    def __init__(self, x, y, z, qx, qy, qz, qw):
        self.position = Vector3(x, y, z)
        self.rotation = Quaternion(qx, qy, qz, qw)

    @classmethod
    def from_pos_rot(cls, position, rotation):
        return cls(position.x, position.y, position.z, rotation.x, rotation.y, rotation.z, rotation.w)

    @classmethod
    def from_list(cls, trans):
        if len(trans) != 7:
            raise Exception('Array must be length 7 to create transform from list')
        return cls(trans[0], trans[1], trans[2], trans[3], trans[4], trans[5], trans[6])

    def to_list(self):
        return self.position.to_list() + self.rotation.to_list()

    def __str__(self):
        return "Pos %.4f, %.4f, %.4f Rot: %.4f, %.4f, %.4f, %.4f" % (
            self.position.x, self.position.y, self.position.z, self.rotation.x, self.rotation.y, self.rotation.z,
            self.rotation.w)

    def __iter__(self):
        return iter(self.to_list())

    # Returns local transform relative to parent object
    def to_local_transform(self, parent):
        relative_rotation = parent.rotation.inverse() * self.rotation
        relative_position = parent.rotation.inverse().rotate(self.position - parent.position)
        return Transform.from_pos_rot(relative_position, relative_rotation)

    # Returns global transform relative to parent object
    def to_global_transform(self, parent):
        global_rotation = parent.rotation * self.rotation
        global_position = parent.rotation.rotate(self.position) + parent.position
        return Transform.from_pos_rot(global_position, global_rotation)
