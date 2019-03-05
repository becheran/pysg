# -*- coding: utf-8 -*-
""" Lights can be added to the scene to illuminate the objects.
"""

from pysg.node_3d import Node3D


class Light(Node3D):

    def __init__(self, color: tuple, name: str = "Light") -> 'Light':
        """ Base class of all lights which can be added to the scene.
        """
        super().__init__(name)
        self.color = color


class PointLight(Light):

    def __init__(self, color: tuple, name: str = "PointLight") -> 'PointLight':
        """ Point light emits light in all directions from a single point.

        Args:
            color: The light intensity of light source.
        """
        super().__init__(color, name)
