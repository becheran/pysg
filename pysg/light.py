# -*- coding: utf-8 -*-
"""
TODO

"""


class Light:
    """The base light class which all other lights need to inherit from."""

    def __init__(self, auto_update=True):
        """
        Args:
            auto_update: If true the object transform will be updated automatically.
            Otherwise you have to do it manually.
        """
        self.auto_update = auto_update
