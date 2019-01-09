# -*- coding: utf-8 -*-
"""Geometry defines the vertices layout of a 3D object
"""


class Geometry:
    """Base class for all geometry objects"""

    def __init__(self):
        """
        Args:
            TODO:
        """
        pass


class BoxGeometry(Geometry):

    def __init__(self, width: float, height: float, depth: float):
        """Creates a simple cube geometry

        Args:
            width (float): Width of cube in meters.
            height (float): Height of cube in meters.
            depth (float): Depth of cube in meters.
        """
        super().__init__()
        self.width = width
        self.height = height
        self.depth = depth
