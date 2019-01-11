# -*- coding: utf-8 -*-
"""The root of the scene graph

All children added to this node can be rendered via a renderer.

"""
from pysg import color
from pysg.model_3d import Model3D
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
        self._render_list = list()

    @property
    def render_list(self) -> list:
        return self._render_list

    def add(self, node_3d: 'Node3D') -> None:
        """ Overrides base class of Node3D to add renderable objects to render list.

        Args:
            node_3d (Node3D): The child node which shall be added to the scene graph.
        """

        for n in (node_3d.get_leaf_nodes()):
            self._render_list.append(n)

        super(Scene, self).add(node_3d)

    def remove(self, node_3d: 'Node3D') -> None:
        """ Overrides base class of Node3D to removes a renderable objects from render list.

        Args:
            node_3d (Node3D): The child node which shall be removed.
        """

        for n in (node_3d.get_leaf_nodes()):
            self._render_list.remove(n)

        super(Scene, self).remove(node_3d)
