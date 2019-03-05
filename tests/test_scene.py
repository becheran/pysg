from unittest import TestCase

from pysg import CubeObject3D, PointLight, Scene
from pysg.testing import CustomAssertions


class TestScene(TestCase, CustomAssertions):
    def setUp(self):
        self.scene = Scene()

    def test_add_1(self):
        cube = CubeObject3D(1, 1, 1)
        self.scene.add(cube)
        self.assertEqual(self.scene.render_list.geometry[0], cube)

    def test_add_2(self):
        light = PointLight(color=(1, 1, 1))
        self.scene.add(light)
        self.assertEqual(self.scene.render_list.point_lights[0], light)
        light2 = PointLight(color=(1, 1, 1))
        self.scene.add(light2)
        # Only one point light per scene is possible
        self.assertEqual(len(self.scene.render_list.point_lights), 1)

    def test_remove(self):
        cube = CubeObject3D(1, 1, 1)
        self.scene.add(cube)
        self.scene.remove(cube)
        self.assertEqual(len(self.scene.render_list.geometry), 0)

    def test_clear(self):
        cube = CubeObject3D(1, 1, 1)
        self.scene.add(cube)
        self.scene.clear()
        self.assertEqual(len(self.scene.render_list.geometry), 0)
        self.assertEqual(len(self.scene.children), 0)
