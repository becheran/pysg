# -*- coding: utf-8 -*-
"""Geometry defines the vertices layout of a 3D object
"""
import numpy as np


class Geometry:

    def __init__(self):
        """Base class for all geometry objects"""
        self._vertices_position = None
        self._vertices_index = None
        self._texture_coordinates = None
        self._normals = None

    @property
    def vertices_position(self):
        return self._vertices_position

    @property
    def vertex_indices(self):
        return self._vertices_index

    @property
    def texture_coordinates(self):
        return self._texture_coordinates

    @property
    def normals(self):
        return self._normals


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
        vertices, indices, texture, normals = self.create_cube(self._width, self._height, self._depth)
        self._vertices_position = vertices
        self._vertices_index = indices
        self._texture_coordinates = texture
        self._normals = normals

    @staticmethod
    def create_cube(width, height, depth, dtype='float32'):
        # half dimension
        width /= 2.
        height /= 2.
        depth /= 2.

        vertices = np.array([
            # front
            # top right
            (width, height, depth,),
            # top left
            (-width, height, depth,),
            # bottom left
            (-width, -height, depth,),
            # bottom right
            (width, -height, depth,),

            # right
            # top right
            (width, height, -depth),
            # top left
            (width, height, depth),
            # bottom left
            (width, -height, depth),
            # bottom right
            (width, -height, -depth),

            # back
            # top right
            (-width, height, -depth),
            # top left
            (width, height, -depth),
            # bottom left
            (width, -height, -depth),
            # bottom right
            (-width, -height, -depth),

            # left
            # top right
            (-width, height, depth),
            # top left
            (-width, height, -depth),
            # bottom left
            (-width, -height, -depth),
            # bottom right
            (-width, -height, depth),

            # top
            # top right
            (width, height, -depth),
            # top left
            (-width, height, -depth),
            # bottom left
            (-width, height, depth),
            # bottom right
            (width, height, depth),

            # bottom
            # top right
            (width, -height, depth),
            # top left
            (-width, -height, depth),
            # bottom left
            (-width, -height, -depth),
            # bottom right
            (width, -height, -depth),
        ], dtype=dtype)

        # default st values
        texture = np.tile(
            np.array([
                (1.0, 1.0,),
                (0.0, 1.0,),
                (0.0, 0.0,),
                (1.0, 0.0,),
            ], dtype=dtype),
            (6, 1,)
        )

        # For triangle type counter clockwise
        # top right -> top left -> bottom left
        # top right -> bottom left -> bottom right
        indices = np.tile(np.array([0, 1, 2, 0, 2, 3], dtype='int'), (6, 1))
        for face in range(6):
            indices[face] += (face * 4)
        indices.shape = (-1,)

        # TODO normals
        normals = vertices

        return vertices, indices, texture, normals
