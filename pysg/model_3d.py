# -*- coding: utf-8 -*-
""" Model3D methods and class"""

from pysg.geometry import Geometry
from pysg.material import Material
from pysg.node_3d import Node3D


class Model3D(Node3D):
    """A 3D object which can be added to the scene graph and rendered."""

    def __init__(self, geometry: Geometry, material: Material):
        """ A Model3D instances can be added to a scene and rendered.

        Args:
            geometry (Geometry): Defines the 3D geometry of the object
            material (Material): Material which shall be used to render the object
        """

        super().__init__()
        self.geometry = geometry
        self.material = material
