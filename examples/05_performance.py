""" Renders a scene with a tree structure
"""
# TODO remove once api is released
import sys

from pyrr import Vector3

from pysg.light import PointLight

sys.path.append("..")  # Adds higher directory to python modules path.

from pysg.constants import color
from pysg.object_3d import CubeObject3D
from pysg.camera import PerspectiveCamera
from pysg.scene import Scene
from pysg.renderer import GLRenderer

from example_qt5_window import Example, run_example


class PerformanceScene(Example):
    def __init__(self):
        GRID_SIZE = 15
        width = self.WINDOW_SIZE[0]
        height = self.WINDOW_SIZE[1]
        self.camera = PerspectiveCamera(fov=45, aspect=width / height, near=1.0, far=1000)
        # It is very important to set auto_update to false for huge performance gain
        scene = Scene(background_color=color.rgb["white"], ambient_light=(0.2, 0.2, 0.2), auto_update=False)
        light = PointLight(color=(0.8, 0.8, 0.8))
        light.world_position = Vector3([GRID_SIZE / 2., GRID_SIZE / 2., GRID_SIZE / 2.])
        scene.add(light)
        for i in range(0, GRID_SIZE):
            for j in range(0, GRID_SIZE):
                for k in range(0, GRID_SIZE):
                    cube = CubeObject3D(0.3, 0.3, 0.3, name="Cube(%d, %d, %d)" % (i, j, k), color=(0.9, 0.5, 0.4))
                    cube.local_position = [i, j, k]
                    scene.add(cube)
        self.camera.local_position = Vector3([GRID_SIZE / 2. - 0.5, GRID_SIZE / 2. - 0.5, GRID_SIZE / 2. - 0.5])
        # Update matrices once because auto update is disabled
        scene.update_world_matrix()
        self.renderer = GLRenderer(scene, self.camera)

    def update(self):
        rot = self.wnd.time * 40
        self.camera.local_euler_angles = [0., rot % 90, 0.]
        self.renderer.viewport = self.wnd.viewport
        self.renderer.render()


try:
    run_example(PerformanceScene)
except Exception as e:
    print(e)
