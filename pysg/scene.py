# -*- coding: utf-8 -*-
"""The root of the scene graph

All children added to this node can be rendered via a renderer.

"""
from pysg.constants import color
from pysg.light import PointLight
from pysg.node_3d import Node3D


class RenderLists:

    def __init__(self):
        """ Data object containing lights and geometry list for rendering. """
        self.geometry = list()
        self.point_lights = list()


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
        self._render_lists = RenderLists()

    @property
    def render_list(self) -> RenderLists:
        """ The current render list containing all the 3D objects and lights for rendering.

        Returns:
            RenderLists: A RenderLists object containing all elements for rendering.
        """
        return self._render_lists

    def add(self, node_3d: 'Node3D') -> None:
        """ Overrides base class of Node3D to add an objects to render or light list.

        Args:
            node_3d (Node3D): The child node which shall be added to the scene graph.
        """

        for n in (node_3d.get_leaf_nodes()):
            object_3d_type = type(n)
            if issubclass(object_3d_type, PointLight):
                if len(self.render_list.point_lights) < 1:
                    self.render_list.point_lights.append(n)
                else:
                    print('Warning! Not more than one point light in a scene is possible right now.')
            else:
                self.render_list.geometry.append(n)

        super(Scene, self).add(node_3d)

    def remove(self, node_3d: 'Node3D') -> None:
        """ Overrides base class of Node3D to removes an object from render or light list.

        Args:
            node_3d (Node3D): The child node which shall be removed.
        """

        for n in (node_3d.get_leaf_nodes()):
            if issubclass(type(n), PointLight):
                self.render_list.point_lights.remove(n)
            else:
                self.render_list.geometry.remove(n)

        super().remove(node_3d)

    def clear(self) -> None:
        """ Clears render lists and scene graph. """

        self.render_list.point_lights = list()
        self.render_list.geometry = list()
        self.children = list()
