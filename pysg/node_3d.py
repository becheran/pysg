# -*- coding: utf-8 -*-
""" The base of all objects which can be aggregated to describe a 3D scene.
Every Node3D element contains the local and world transformations in 3D space. Every node has one parent node
and a list of child nodes. Every transformation such as, position, rotation, or scale, also affects the
child objects of a node.

The following code example shows how nodes can be created and combined to describe a simple scene with the
following node hierarchy:

Create Hierarchy
    ::

        #     root
        #     /  \\
        #   c_1, c_2
        #       /   \\
        #    c_2_1  c_2_2

        root = Node3D("root")
        c_1 = Node3D("child_1")
        c_2 = Node3D("child_2")
        c_2_1 = Node3D("child_2_1")
        c_2_2 = Node3D("child_2_2")
        root.add(c_1)
        root.add(c_2)
        c_2.add(c_2_1)
        c_2.add(c_2_2)

All Node3D objects can now be individually transformed in 3D space.

Change position of root node
    ::

        root.local_position = Vector([2,1,1])

After executing the code above, all child nodes and the root node itself are moved to the position of the root node.

Change child node local position
    ::

        c_2.local_position += Vector([1,0,0])

The root node and node c_1 are still at position [2,1,1] since they are not affected by the transforms
of the c_2 child node. Both child nodes c_2_1 and c_2_2 and node c_2 itself are shifted 1 unit
towards the local x-axis away from the root node. This means that these nodes are now at
world coordinates [3,1,1].

"""
from copy import copy

from pyrr import Matrix44, Vector3, Quaternion

from pysg.pyrr_extensions import compose_matrix, quaternion_to_euler_angles, euler_angles_to_quaternion
from pysg.util import pyrr_type_checker, parameters_as_angles_deg_to_rad


class Node3D:

    def __init__(self, name: str = "New Node"):
        """  Node element of scene graph (tree structure).

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

        self.__matrix_needs_update = True

    @property
    def parent(self):
        """ The parent of the current node element.

        Returns:
            Node3D: Parent node.

        """
        return self._parent

    @parent.setter
    def parent(self, parent: 'Node3D') -> None:
        self._parent = parent
        if parent is None:
            # If parent is set to None local and world transform are the same
            self._world_position = self._local_position
            self._world_quaternion = self._local_quaternion
        else:
            # If new root node is added the local transform will be set relative to new root node
            self._local_quaternion = self._local_quaternion * parent.world_quaternion.inverse
            self._local_position = self._local_quaternion * (self.world_position - parent.world_position)

    @property
    def local_position(self):
        """ The local position is relative to the transform of the parent node.

        .. note:: The return value is a copy of the original vector and can not be edited directly.
                 This means that code like node.local_position.x += 2 will not work as you might expect it to!

        Returns:
            Vector3: Position of node relative to parent node.

        """
        return copy(self._local_position)

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
        """ The world position of a node.

        .. note:: The return value is a copy of the original vector and can not be edited directly.
                 This means that code like node.world_position.x += 2 will not work as you might expect it to!

        Returns:
            Vector3: Position of node in world space.

        """
        return copy(self._world_position)

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
        """ The local rotation as quaternion.

        .. note:: The return value is a copy of the original quaternion and can not be edited directly.
                Use the quaternion setter instead.

        Returns:
            Quaternion: Quaternion rotation relative to parent node.

        """
        return copy(self._local_quaternion)

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
        """ The world rotation as quaternion.

        .. note:: The return value is a copy of the original quaternion and can not be edited directly.
                Use the quaternion setter instead.

        Returns:
            Quaternion: Rotation in world space as quaternion.

        """
        return copy(self._world_quaternion)

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
        """ Local rotation in euler angle representation as Vector of length 3.
        Internally quaternions are used. The used rotation order is YZX.

        .. seealso:: Please have a look at the :ref:`rotations` section for more details.
        """
        return quaternion_to_euler_angles(self.local_quaternion)

    @local_euler_angles.setter
    @parameters_as_angles_deg_to_rad('euler')
    def local_euler_angles(self, euler: Vector3):
        self.local_quaternion = euler_angles_to_quaternion(euler)

    @property
    def world_euler_angles(self):
        """  World rotation in euler angle representation as Vector of length 3.
        Internally quaternions are used. The used rotation order is YZX.

        .. seealso:: Please have a look at the :ref:`rotations` section for more details.
        """
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
    def local_matrix(self) -> Matrix44:
        """ Local translation matrix (read only).

        Returns:
            Matrix44: 4x4 local translation matrix of the current node.

        """
        if self.__matrix_needs_update:
            self.__matrix_needs_update = False
            self._local_matrix = compose_matrix(self.local_position, self.local_quaternion, self.scale)
        return self._local_matrix

    @property
    def world_matrix(self) -> Matrix44:
        """ World translation matrix (read only).

        Returns:
            Matrix44: 4x4 translation matrix of the current node in world space.

        """
        return self._world_matrix

    @property
    def scale(self) -> Vector3:
        """ Local scale of current node.

        Returns:
            Vector3: X, Y and Z scale as Vector3.

        """
        return copy(self._scale)

    @scale.setter
    def scale(self, scale: Vector3) -> None:
        self.__matrix_needs_update = True
        self._scale = scale

    def __repr__(self):
        return "Node(%s)" % self.name

    def add(self, node_3d: 'Node3D') -> None:
        """ Adds another node as child of this node. It is important to note, that the world position and
        rotation will remain the same of the added child, but all its local transforms will be updated relative
        to the new parent.

        Args:
            node_3d (Node3D): The child node which shall be added to the scene graph.
        """
        self.children.append(node_3d)
        # Local transforms will be updated when setting the parent property
        node_3d.parent = self

    def remove(self, node_3d: 'Node3D') -> None:
        """ Remove a child from the scene graph.

        Args:
            node_3d (Node3D): The child node which shall be removed from the scene graph.
        """
        node_3d.parent = None
        self.children.remove(node_3d)

    def update_world_matrix(self) -> None:
        """ Updates the world matrix for a given node in the render scene graph."""
        if self._parent is None:
            self._world_matrix = self.local_matrix
        else:
            self._world_matrix = self.parent.world_matrix * self.local_matrix

        for child in self.children:
            child.update_world_matrix()

    def get_leaf_nodes(self) -> list:
        """ Recursively iterate over all children and return list with all leaf Node3Ds (no more children).

        Returns:
            list: List of all children with no more child nodes. Type of list elements is Node3D.
        """
        leafs = []

        def _get_leaf_nodes(node):
            if node is not None:
                leafs.append(node)
                for n in node.children:
                    _get_leaf_nodes(n)

        _get_leaf_nodes(self)
        return leafs
