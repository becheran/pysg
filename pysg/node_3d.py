# -*- coding: utf-8 -*-
"""The base of all objects which are displayed in the scene.
"""


class Node3D:
    """Node object of the scene graph. Contains transforms of objects in the scene."""

    def __init__(self):
        """ Scene is the base node. All other nodes need to be added to the scene.
        """
        self.child = None

    def add(self, node_3d):
        """ Adds another node as a child of this node to the scene graph.

        Args:
            node_3d (Node3D): The child node which shall be added to the scene graph.
        """
        self.child = node_3d
