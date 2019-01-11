# -*- coding: utf-8 -*-
"""Geometry defines the vertices layout of a 3D object
"""
from pyrr import geometry


class Geometry:

    def __init__(self):
        """Base class for all geometry objects"""
        self._vertex_position = None
        self._vertex_indices = None
        # TODO Add NORMALS and COLOR

    @property
    def vertex_position(self):
        return self._vertex_position

    @property
    def vertex_indices(self):
        return self._vertex_indices


class BoxGeometry(Geometry):

    def __init__(self, width: float, height: float, depth: float):
        """Creates a simple cube geometry

        Args:
            width (float): Width of cube in meters.
            height (float): Height of cube in meters.
            depth (float): Depth of cube in meters.
        """
        super().__init__()
        self._width = width
        self._height = height
        self._depth = depth
        self._update_geometry()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def depth(self):
        return self._depth

    @width.setter
    def width(self, width):
        self._width = width
        self._update_geometry()

    @height.setter
    def height(self, height):
        self._height = height
        self._update_geometry()

    @depth.setter
    def depth(self, depth):
        self._depth = depth
        self._update_geometry()

    def _update_geometry(self):
        cube_geo = geometry.create_cube((self._width, self._height, self._depth))
        self._vertex_position = cube_geo[0]
        self._vertex_indices = cube_geo[1]
