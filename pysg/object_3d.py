# -*- coding: utf-8 -*-
""" This module contains all geometric 3D objects which can be added to a scene. All 3D objects inherit from
the Object3D base class. 3D objects are defined via a color, the object size, and a name."""

import pysg.constants.color
from pysg.node_3d import Node3D


class Object3D(Node3D):

    def __init__(self, name: str = "Object3D", color=pysg.constants.color.rgb['white']):
        """ A Object3D instances can be added to a scene and rendered.

        Args:
            name (str): Name of Object3D node.
        """

        super().__init__(name=name)
        self.size = (1, 1, 1)
        self.color = color


class CubeObject3D(Object3D):

    def __init__(self, width: float, height: float, depth: float, color=pysg.constants.color.rgb['white'],
                 name: str = "CubeObject"):
        """Creates a simple cube geometry

        Args:
            width (float): Width of cube.
            height (float): Height of cube.
            depth (float): Depth of cube.
            color (tuple): Color of 3D object.
            name (str): Name of object.
        """
        super().__init__(color=color, name=name)
        self.size = (width, height, depth)


class PlaneObject3D(Object3D):

    def __init__(self, width: float, height: float, color=pysg.constants.color.rgb['white'],
                 name: str = "PlaneObject"):
        """Creates a simple plane geometry.

        .. note:: Per default, only the front face of a plane gets rendered. If you want to also show the
                backface, you have to configure the moderngl render context. See :ref:`renderer` section
                for more information.

        Args:
            width (float): Width of plane.
            height (float): Height of plane.
            color (tuple): Color of 3D object.
            name (str): Name of object.
        """
        super().__init__(color=color, name=name)
        self.size = (width, 1, height)


class CircleObject3D(Object3D):

    def __init__(self, radius: float, color=pysg.constants.color.rgb['white'],
                 name: str = "CircleObject"):
        """Creates a simple circle geometry.

        .. note:: Per default, only the front face of a plane gets rendered. If you want to also show the
                backface, you have to configure the moderngl render context. See :ref:`renderer` section
                for more information.

        Args:
            radius (float): Radius of circle.
            color (tuple): Color of 3D object.
            name (str): Name of object.
        """
        super().__init__(color=color, name=name)
        self.size = (radius, 1, radius)


class IcosahedronObject3D(Object3D):

    def __init__(self, radius: float, color=pysg.constants.color.rgb['white'],
                 name: str = "IcosahedronObject"):
        """Creates a icosahedron geometry.

        Args:
            radius (float): Radius of icosahedron.
            color (tuple): Color of 3D object.
            name (str): Name of object.
        """
        super().__init__(color=color, name=name)
        self.size = (radius, radius, radius)


class TriangleObject3D(Object3D):

    def __init__(self, width: float, height: float, color=pysg.constants.color.rgb['white'],
                 name: str = "TriangleObject"):
        """Creates a icosahedron geometry.

        Args:
            width (float): Width of triangle.
            height (float): Height of triangle.
            color (tuple): Color of 3D object.
            name (str): Name of object.
        """
        super().__init__(color=color, name=name)
        self.size = (width, 1, height)


class CylinderObject3D(Object3D):

    def __init__(self, height: float, radius: float, color=pysg.constants.color.rgb['white'],
                 name: str = "CylinderObject"):
        """Creates a icosahedron geometry.

        Args:
            width (float): Width of triangle.
            height (float): Height of triangle.
            color (tuple): Color of 3D object.
            name (str): Name of object.
        """
        super().__init__(color=color, name=name)
        self.size = (radius * 2, height, radius * 2)


class TetrahedralObject3D(Object3D):

    def __init__(self, radius: float, color=pysg.constants.color.rgb['white'],
                 name: str = "BoxObject"):
        """Creates a tetrahedral geometry.

        Args:
            radius (float): radius of edge points lying on unit sphere.
            color (tuple): Color of 3D object.
            name (str): Name of object.
        """
        super().__init__(color=color, name=name)
        self.size = (radius, radius, radius)


class PyramidObject3D(Object3D):

    def __init__(self, base_size: float, height: float, color=pysg.constants.color.rgb['white'],
                 name: str = "PyramidObject"):
        """Creates a square base pyramide geometry.

        Args:
            base_size (float): Size of the pyramid square base.
            height (float): Pyramid height.
            color (tuple): Color of 3D object.
            name (str): Name of object.
        """
        super().__init__(color=color, name=name)
        self.size = (base_size, height, base_size)
