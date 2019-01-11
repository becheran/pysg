# -*- coding: utf-8 -*-
"""The base of all objects which are displayed in the scene.
"""

from pyrr import Matrix44, Vector3


class Node3D:
    """Node object of the scene graph. Contains transforms of objects in the scene."""

    def __init__(self, name: str = "New Node"):
        """ Scene is the base node. All other nodes need to be added to the scene.
        """
        self.children = list()
        self.parent = None
        self.name = name

        self.matrix_world = Matrix44.identity()
        self.matrix = Matrix44.identity()
        self.eulerAngles = Vector3()

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
            self.matrix_world = self.matrix
        else:
            self.matrix_world = self.matrix_world * self.matrix

        # TODO execute in multiple worker threads?
        for child in self.children:
            child.update_world_matrix()

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
