# -*- coding: utf-8 -*-
"""The base of all objects which are displayed in the scene.
"""

import numpy as np
from pyrr import Matrix44, Vector3, Quaternion

from pysg.math import compose_matrix, quaternion_to_euler_angles, euler_angles_to_quaternion
from pysg.util import pyrr_type_checker, parameters_as_angles_deg_to_rad


class Node3D:
    """Node object of the scene graph. Contains transforms of objects in the scene."""

    def __init__(self, name: str = "New Node"):
        """ Scene is the base node. All other nodes need to be added to the scene.

        Args:
            name: Name for string representation.
        """
        self.children = list()
        self._parent = None
        self.name = name

        self._local_position = Vector3()
        self._world_position = Vector3()

        self._scale = Vector3([1., 1., 1.])

        self._local_quaternion = Quaternion()
        self._world_quaternion = Quaternion()
        self._world_matrix = Matrix44.identity()
        self._local_matrix = Matrix44.identity()
        # TODO Rotation as matrix33

        self.__matrix_needs_update = True

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: 'Node3D') -> None:
        self._parent = parent
        self._local_quaternion = self._local_quaternion * parent.world_quaternion.inverse
        self._local_position = self._local_quaternion * (self.world_position - parent.world_position)
        # TODO UPDATE scale

    @property
    def local_position(self):
        return self._local_position

    @local_position.setter
    def local_position(self, local_position: Vector3) -> None:
        local_position = pyrr_type_checker(local_position, Vector3)
        self.__matrix_needs_update = True
        self._local_position = local_position
        world_position_from_rotation = self._world_quaternion * self._local_position
        if self._parent is None:
            self.world_position = world_position_from_rotation
        else:
            self.world_position = self._parent.world_position + world_position_from_rotation

    @property
    def world_position(self):
        return self._world_position

    @world_position.setter
    def world_position(self, world_position: Vector3) -> None:
        world_position = pyrr_type_checker(world_position, Vector3)
        self.__matrix_needs_update = True
        self._world_position = world_position
        if self._parent is None:
            self._local_position = world_position
        for child in self.children:
            child.world_position = child.local_position + self._world_position

    @property
    def local_quaternion(self):
        return self._local_quaternion

    @local_quaternion.setter
    def local_quaternion(self, local_quaternion: Quaternion) -> None:
        local_quaternion = pyrr_type_checker(local_quaternion, Quaternion)
        self.__matrix_needs_update = True
        self._local_quaternion = local_quaternion
        if self._parent is None:
            self.world_quaternion = local_quaternion
        else:
            self.world_quaternion = local_quaternion * self._parent.world_quaternion

    @property
    def world_quaternion(self):
        return self._world_quaternion

    @world_quaternion.setter
    def world_quaternion(self, world_quaternion: Quaternion) -> None:
        world_quaternion = pyrr_type_checker(world_quaternion, Quaternion)
        self.__matrix_needs_update = True
        self._world_quaternion = world_quaternion
        if self._parent is None:
            self._local_quaternion = world_quaternion
        for child in self.children:
            child.world_quaternion = child.world_quaternion * self.world_quaternion

    @property
    def local_euler_angles(self):
        """  Euler Angles as Vector of length 3.
        The used rotation order is YZX.

        Please have a look at the :ref:`rotations` section for more details.
        """
        return quaternion_to_euler_angles(self.local_quaternion)

    @local_euler_angles.setter
    @parameters_as_angles_deg_to_rad('euler')
    def local_euler_angles(self, euler: Vector3):
        self.local_quaternion = euler_angles_to_quaternion(euler)

    @property
    def world_euler_angles(self):
        return quaternion_to_euler_angles(self.world_quaternion)

    @parameters_as_angles_deg_to_rad('euler')
    @world_euler_angles.setter
    def world_euler_angles(self, euler: Vector3):
        self.world_quaternion = euler_angles_to_quaternion(euler)

    @parameters_as_angles_deg_to_rad('angle')
    def rotate_x(self, angle: float, local_space: bool = True) -> None:
        """ Rotate object around its x-axis.

        Args:
            angle: The rotation angle in degrees.
            local_space: If True rotate in local coordinate system. Otherwise in world space.
        """
        rotation_quaternion = Quaternion.from_x_rotation(angle)
        if local_space:
            self.local_quaternion *= rotation_quaternion
        else:
            self.world_quaternion *= rotation_quaternion

    @parameters_as_angles_deg_to_rad('angle')
    def rotate_y(self, angle: float, local_space: bool = True) -> None:
        """ Rotate object around its y-axis.

        Args:
            angle: The rotation angle in degrees.
            local_space: If True rotate in local coordinate system. Otherwise in world space.
        """
        rotation_quaternion = Quaternion.from_y_rotation(angle)
        if local_space:
            self.local_quaternion *= rotation_quaternion
        else:
            self.world_quaternion *= rotation_quaternion

    @parameters_as_angles_deg_to_rad('angle')
    def rotate_z(self, angle: float, local_space: bool = True) -> None:
        """ Rotate object around its z-axis.

        Args:
            angle: The rotation angle in degrees.
            local_space: If True rotate in local coordinate system. Otherwise in world space.
        """
        rotation_quaternion = Quaternion.from_z_rotation(angle)
        if local_space:
            self.local_quaternion *= rotation_quaternion
        else:
            self.world_quaternion *= rotation_quaternion

    @property
    def scale(self, scale):
        # TODO implement
        self._scale = scale

    # TODO SETTER SCALE.

    # TODO LOSSY scale for global scale??

    @property
    def local_matrix(self):
        if self.__matrix_needs_update:
            self.__matrix_needs_update = False
            self._local_matrix = compose_matrix(self.local_position, self.local_quaternion, self.scale)
        return self._local_matrix

    @property
    def world_matrix(self):
        return self._world_matrix

    @property
    def scale(self):
        return self._scale

    def __repr__(self):
        return "Node(%s)" % self.name

    def add(self, node_3d: 'Node3D') -> None:
        """ Adds another node as a child of this node to the scene graph.
        It is very important to note, that the world position and rotation will remain the same of the added child, but
        all its local transforms will be updated relative to the new parent.

        Args:
            node_3d (Node3D): The child node which shall be added to the scene graph.
        """
        self.children.append(node_3d)
        # Update local transform of child!
        node_3d.parent = self

    def remove(self, node_3d: 'Node3D') -> None:
        """ Remove a child from the scene graph.

        Args:
            node_3d (Node3D): The child node which shall be removed from the scene graph.
        """
        self.children.remove(node_3d)

    def update_world_matrix(self) -> None:
        """ Updates the world matrix for a given node in the render scene graph."""
        if self._parent is None:
            self._world_matrix = self.local_matrix
        else:
            self._world_matrix = self.parent.world_matrix * self.local_matrix

        for child in self.children:
            child.update_world_matrix()

    # TODO Add check function as parameter
    def get_leaf_nodes(self) -> list:
        """ Recursively goes over all node children and returns Node3D list.

        Returns:
            list: Node3D list of all children and object itself.
        """
        leafs = []

        def _get_leaf_nodes(node):
            if node is not None:
                leafs.append(node)
                for n in node.children:
                    _get_leaf_nodes(n)

        _get_leaf_nodes(self)
        return leafs
