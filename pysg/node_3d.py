# -*- coding: utf-8 -*-
"""The base of all objects which are displayed in the scene.
"""

from pyrr import Matrix44, Vector3, Quaternion


class Node3D:
    """Node object of the scene graph. Contains transforms of objects in the scene."""

    def __init__(self, name: str = "New Node"):
        """ Scene is the base node. All other nodes need to be added to the scene.

        Args:
            name: Name for string representation.
        """
        self.children = list()
        self.parent = None
        self.name = name

        self._local_position = Vector3()
        self._world_position = Vector3()

        self._scale = Vector3()
        # TODO global scale?

        self._local_quaternion = Quaternion()
        self._world_quaternion = Quaternion()
        self._local_eulerAngles = Vector3()
        self._world_eulerAngles = Vector3()
        self._world_matrix = Matrix44.identity()
        self._local_matrix = Matrix44.identity()
        # TODO Rotation as matrix33

        self.__matrix_needs_update = False

    @property
    def local_position(self):
        return self._local_position

    @local_position.setter
    def local_position(self, local_position):
        self.__matrix_needs_update = True
        self._local_position = local_position

    @property
    def world_position(self):
        return self._world_position

    @world_position.setter
    def world_position(self, world_position):
        self.__matrix_needs_update = True
        # TODO UPDATE CHILDREN
        self._world_position = world_position

    @property
    def local_matrix(self):
        if self.__matrix_needs_update:
            self.__matrix_needs_update = False
            # TODO
        return self._local_matrix

    @property
    def world_matrix(self):
        if self.__matrix_needs_update:
            self.__matrix_needs_update = False
        return self._world_matrix

    def __repr__(self):
        return "Node(%s)" % self.name

    def add(self, node_3d: 'Node3D') -> None:
        """ Adds another node as a child of this node to the scene graph.

        Args:
            node_3d (Node3D): The child node which shall be added to the scene graph.
        """
        self.children.append(node_3d)
        node_3d.parent = self

    def remove(self, node_3d: 'Node3D') -> None:
        """ Remove a child from the scene graph.

        Args:
            node_3d (Node3D): The child node which shall be removed from the scene graph.
        """
        self.children.remove(node_3d)

    def update_world_matrix(self) -> None:
        """ Updates the world matrix for a given node in the render scene graph."""
        if self.parent is None:
            self._world_matrix = self._local_matrix
        else:
            self._world_matrix = self.parent.world_matrix * self._local_matrix

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
