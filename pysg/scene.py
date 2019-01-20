# -*- coding: utf-8 -*-
"""The root of the scene graph

All children added to this node can be rendered via a renderer.

"""
from pysg.constants import color
from pysg.light import Light, PointLight
from pysg.node_3d import Node3D
from pysg.object_3d import Object3D


class Scene(Node3D):

    def __init__(self, background_color: tuple = color.rgb["black"],
                 ambient_light: tuple = (0., 0., 0.), auto_update: bool = True):
        """ The scene object. Must always bee the root node of the scene graph.
        Args:
            background_color: The clear color of the scene.
            ambient_light: Light value which will be applied to all objects in scene.
            auto_update: If true the object transform will be updated automatically.
            Otherwise you have to do it manually.
        """
        super().__init__()
        self.auto_update = auto_update
        self.background_color = background_color
        self.ambient_light = ambient_light
        self._render_list = list()
        self._light_list = list()

    @property
    def render_list(self) -> list:
        return self._render_list

    @property
    def light_list(self) -> list:
        return self._light_list

    def add(self, node_3d: 'Node3D') -> None:
        """ Overrides base class of Node3D to add an objects to render por light list.

        Args:
            node_3d (Node3D): The child node which shall be added to the scene graph.
        """

        for n in (node_3d.get_leaf_nodes()):
            if issubclass(type(n), Light):
                self._light_list.append(n)
            elif issubclass(type(n), Object3D):
                self._render_list.append(n)

        super(Scene, self).add(node_3d)

    def remove(self, node_3d: 'Node3D') -> None:
        """ Overrides base class of Node3D to removes an object from render or light list.

        Args:
            node_3d (Node3D): The child node which shall be removed.
        """

        for n in (node_3d.get_leaf_nodes()):
            if type(n) is Light:
                self._light_list.remove(n)
            elif type(n) is Object3D:
                self._render_list.remove(n)

        super(Scene, self).remove(node_3d)
