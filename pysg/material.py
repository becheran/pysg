# -*- coding: utf-8 -*-
""" Materials are used to compute the RGB values of a 3D model.
"""
from pysg.constants import color


class Material:

    def __init__(self):
        """ Base material class which all other materials need to inherit from."""
        # TODO implement


class BasicMaterial(Material):

    def __init__(self, color=color.rgb['white']):
        """ Very basic material which is not affected by lights.

        Args:
            material_color: The color of the whole mesh.
        """
        super().__init__()
        self.color = color
