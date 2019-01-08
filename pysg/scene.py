# -*- coding: utf-8 -*-
"""The root of the scene graph

All children added to this node can be rendered via a renderer.

"""
from pysg.node_3d import Node3D


class Scene(Node3D):
    """The scene object"""

    def __init__(self, auto_update=True):
        """
        Args:
            auto_update: If true the object transform will be updated automatically.
            Otherwise you have to do it manually.
        """
        super().__init__()
        self.auto_update = auto_update
        self.background_color = color.black
