# -*- coding: utf-8 -*-
""" Materials are used to compute the RGB values of a 3D model.
"""


class Material:

    def __init__(self):
        """ Base material class which all other materials need to inherit from."""
        # TODO implement


class BasicMaterial(Material):

    def __init__(self):
        """ Very basic material which is not affected by lights."""
        super().__init__()
        # TODO implment
