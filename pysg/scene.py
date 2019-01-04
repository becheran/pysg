# -*- coding: utf-8 -*-
"""The root of the scene graph

All children added to this node can be rendered via a renderer.

"""


class Scene:
    """The scene object"""

    def __init__(self, auto_update=True):
        """
        Args:
            auto_update: If true the object transform will be updated automatically.
            Otherwise you have to do it manually.
        """
        self.auto_update = auto_update
