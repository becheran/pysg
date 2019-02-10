from unittest import TestCase

from pysg import PerspectiveCamera, OrthographicCamera
from pysg.error import Error


class TestPerspectiveCamera(TestCase):

    def test_parameter_errors_FOV(self):
        with self.assertRaises(Error):
            PerspectiveCamera(fov=-1, aspect=1, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=0, aspect=1, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=390, aspect=1, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=186, aspect=1, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=180, aspect=1, near=0.1, far=100)

    def test_parameter_errors_aspect_ratio(self):
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=-0.1, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=-1, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.0, near=0.1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0, near=0.1, far=100)

    def test_parameter_errors_near_far(self):
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=-1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=0, far=0)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=-1, far=1)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=0, far=-1)


class TestOrthographicCamera(TestCase):

    def test_parameter_errors_left_right(self):
        with self.assertRaises(Error):
            OrthographicCamera(left=100, right=-100, top=100, bottom=-100, near=0.1, far=100)
        with self.assertRaises(Error):
            OrthographicCamera(left=0, right=0, top=100, bottom=-100, near=0.1, far=100)
        with self.assertRaises(Error):
            OrthographicCamera(left=100, right=100, top=100, bottom=-100, near=0.1, far=100)

    def test_parameter_errors_top_bottom(self):
        with self.assertRaises(Error):
            OrthographicCamera(left=-100, right=100, top=-100, bottom=100, near=0.1, far=100)
        with self.assertRaises(Error):
            OrthographicCamera(left=-100, right=100, top=100, bottom=100, near=0.1, far=100)
        with self.assertRaises(Error):
            OrthographicCamera(left=-100, right=100, top=0, bottom=0, near=0.1, far=100)

    def test_parameter_errors_near_far(self):
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=-1, far=100)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=0, far=0)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=-1, far=1)
        with self.assertRaises(Error):
            PerspectiveCamera(fov=45, aspect=0.2, near=0, far=-1)
