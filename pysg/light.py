# -*- coding: utf-8 -*-
""" Lights can be added to the scene.
Some materials like the BasicMaterial ignores any light sources and simply outputs a color.
"""
from pysg.node_3d import Node3D


class Light(Node3D):

    def __init__(self):
        """ Base class of all lights which can be added to the scene.
        """
        # TODO Implement
        super().__init__()
