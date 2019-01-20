# -*- coding: utf-8 -*-
""" Object3D methods and class"""
import numpy as np

import pysg.constants.color
from pysg.node_3d import Node3D


class Object3D(Node3D):

    def __init__(self, name: str = "Model3D", color=pysg.constants.color.rgb['white']):
        """ A Object3D instances can be added to a scene and rendered.

        Args:
            name (str): Name of Object3D node.
        """

        self._vertex_positions = None
        self._vertex_indices = None
        self._normals = None
        self.color = color
        super().__init__(name=name)

    @property
    def vertex_positions(self):
        return self._vertex_positions

    @property
    def vertex_indices(self):
        return self._vertex_indices

    @property
    def normals(self):
        return self._normals


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
        vertices, indices, normals = self._create_cube(width, height, depth)
        self._vertex_positions = vertices
        self._vertex_indices = indices
        self._normals = normals

    @staticmethod
    def _create_cube(width, height, depth, dtype='float32'):
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

        # For triangle type counter clockwise
        # top right -> top left -> bottom left
        # top right -> bottom left -> bottom right
        indices = np.tile(np.array([0, 1, 2, 0, 2, 3], dtype='int'), (6, 1))
        for face in range(6):
            indices[face] += (face * 4)
        indices.shape = (-1,)

        normals = np.array([
            # front
            (0, 0, 1,),
            (0, 0, 1,),
            (0, 0, 1,),
            (0, 0, 1,),

            # right
            (1, 0, 0,),
            (1, 0, 0,),
            (1, 0, 0,),
            (1, 0, 0,),

            # back
            (0, 0, -1,),
            (0, 0, -1,),
            (0, 0, -1,),
            (0, 0, -1,),

            # left
            (-1, 0, 0,),
            (-1, 0, 0,),
            (-1, 0, 0,),
            (-1, 0, 0,),

            # top
            (0, 1, 0,),
            (0, 1, 0,),
            (0, 1, 0,),
            (0, 1, 0,),

            # bottom
            (0, -1, 0,),
            (0, -1, 0,),
            (0, -1, 0,),
            (0, -1, 0,),
        ], dtype=dtype)

        return vertices, indices, normals
