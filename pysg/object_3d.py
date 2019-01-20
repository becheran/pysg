# -*- coding: utf-8 -*-
""" Object3D methods and class"""

import pysg.constants.color
from pysg.node_3d import Node3D


class Object3D(Node3D):

    def __init__(self, name: str = "Model3D", color=pysg.constants.color.rgb['white']):
        """ A Object3D instances can be added to a scene and rendered.

        Args:
            name (str): Name of Object3D node.
        """

        super().__init__(name=name)
        self.size = (1, 1, 1)
        self.color = color


class BoxObject3D(Object3D):

    def __init__(self, width: float, height: float, depth: float, color=pysg.constants.color.rgb['white'],
                 name: str = "BoxObject"):
        """Creates a simple cube geometry

        Args:
            width (float): Width of cube in meters.
            height (float): Height of cube in meters.
            depth (float): Depth of cube in meters.
            color (tuple): Color of 3D object.
            name (str): Name of object.
        """
        super().__init__(color=color, name=name)
        self.size = (width, height, depth)
