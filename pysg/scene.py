# -*- coding: utf-8 -*-
"""The root of the scene graph

All children added to this node can be rendered via a renderer.

"""
from pysg import color
from pysg.node_3d import Node3D


class Scene(Node3D):

    # TODO tuple type color
    def __init__(self, background_color: object = color.rgb["black"], auto_update: bool = True):
        """ The scene object. Must always bee the root node of the scene graph.
        Args:
            background_color:
            auto_update: If true the object transform will be updated automatically.
            Otherwise you have to do it manually.
        """
        super().__init__()
        self.auto_update = auto_update
        self.background_color = background_color
