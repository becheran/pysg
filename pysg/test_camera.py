from unittest import TestCase

from pysg.camera import PerspectiveCamera
from pysg.error import Error


class TestCamera(TestCase):

    def test_init(self):
        # TODO
        self.assertFalse(True)


class TestPerspectiveCamera(TestCase):

    def test_input_errors(self):
        # Different invalid configurations which should through built-in errors

        # Field of view
        with self.assertRaises(Error):
            PerspectiveCamera(fov=-1, aspect=1, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=0, aspect=1, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=390, aspect=1, near=0.1, far=100)

        # Aspect ratio
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=-0.1, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=-1, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.0, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0, near=0.1, far=100)

        # Near and far
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=-1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=0, far=0)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=-1, far=1)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=0, far=-1)

    def test_matrix(self):
        # TODO
        self.assertFalse(True)
