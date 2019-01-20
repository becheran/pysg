""" Renders a simple cube
"""
# TODO remove once api is released
import math
import sys

from pyrr import Vector3

from pysg.light import PointLight

sys.path.append("..")  # Adds higher directory to python modules path.

from pysg.constants import color
from pysg.object_3d import BoxObject3D
from pysg.camera import PerspectiveCamera
from pysg.scene import Scene
from pysg.renderer import GLRenderer

from example_qt5_window import Example, run_example


class SimpleScene(Example):
    def __init__(self):
        width = self.WINDOW_SIZE[0]
        height = self.WINDOW_SIZE[1]
        camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
        scene = Scene(background_color=color.rgb["black"], ambient_light=(0.2, 0.2, 0.2))
        light = PointLight(color=(0.8, 0.8, 0.8))
        light.world_position = Vector3([1, 1, 1])
        scene.add(light)
        self.cube = BoxObject3D(1, 1, 1, color=color.rgb["red"])
        self.cube.name = "Cube_1"
        camera.local_position += Vector3([0, 0, 10])
        scene.add(self.cube)
        self.renderer = GLRenderer(scene, camera)

    def update(self):
        self.renderer.viewport = self.wnd.viewport
        self.renderer.render()
        self.cube.local_euler_angles = Vector3([0, self.wnd.time * 100, 0])


try:
    run_example(SimpleScene)
except Exception as e:
    print(e)
