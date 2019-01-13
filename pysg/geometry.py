# -*- coding: utf-8 -*-
"""Geometry defines the vertices layout of a 3D object
"""
from pyrr import geometry
import numpy as np


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

    def _update_geometry(self):
        cube_geo = geometry.create_cube((self._width, self._height, self._depth))
        x = self._width / 2.0
        y = self._height / 2.0
        z = self._depth / 2.0
        self._vertex_position = np.array([
            # front
            -x, -y, z,
            x, -y, z,
            x, y, z,
            -x, y, z,
            # back
            -x, -y, -z,
            x, -y, -z,
            x, y, -z,
            -x, y, -z])
        self._vertex_indices = np.array([
            # front
            0, 1, 2,
            2, 3, 0,
            # right
            1, 5, 6,
            6, 2, 1,
            # back
            7, 6, 5,
            5, 4, 7,
            # left
            4, 0, 3,
            3, 7, 4,
            # bottom
            4, 5, 1,
            1, 0, 4,
            # top
            3, 2, 6,
            6, 7, 3
        ])

        # self._vertex_position = cube_geo[0]
        # self._vertex_indices = cube_geo[1]
