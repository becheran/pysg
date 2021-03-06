""" Renders a scene with a tree structure. """
import math

from example_qt5_window import Example, run_example
from pyrr import Vector3

from pysg.camera import PerspectiveCamera
from pysg.constants import color
from pysg.light import PointLight
from pysg.object_3d import CubeObject3D
from pysg.renderer import GLRenderer
from pysg.scene import Scene


class HierarchyScene(Example):
    def __init__(self):
        width = self.WINDOW_SIZE[0]
        height = self.WINDOW_SIZE[1]
        self.camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
        scene = Scene(background_color=color.rgb["white"], ambient_light=(0.2, 0.2, 0.2))
        light = PointLight(color=(0.8, 0.8, 0.8))
        light.world_position = Vector3([2, 2, 2])
        scene.add(light)
        self.cube_1 = CubeObject3D(1, 1, 1, name="Cube_1", color=(0.9, 0.5, 0.4))
        self.cube_2 = CubeObject3D(1, 1, 1, name="Cube_2", color=(0.5, 0.9, 0.4))
        self.cube_3 = CubeObject3D(1, 1, 1, name="Cube_3", color=(0.4, 0.5, 0.9))
        self.cube_1.add(self.cube_2)
        self.cube_2.add(self.cube_3)
        self.cube_2.local_position = Vector3([5., 0, 0])
        self.cube_3.local_position = Vector3([0, 3, 0])
        self.camera.local_position = Vector3([0, 0, 30])
        scene.add(self.cube_1)
        self.renderer = GLRenderer(scene, self.camera)

    def update(self):
        rot = self.wnd.time * 100
        scale = math.fabs(math.sin(self.wnd.time)) + 1
        self.cube_1.local_euler_angles = Vector3([0, rot, 0])
        self.cube_2.local_euler_angles = Vector3([0, -rot, rot])
        self.cube_1.scale = Vector3([scale, scale, scale])
        self.cube_2.scale = Vector3([scale, scale, scale]) * 0.5
        self.cube_3.scale = Vector3([scale, scale, scale])
        self.renderer.viewport = self.wnd.viewport
        self.renderer.render()


if __name__ == "__main__":
    try:
        run_example(HierarchyScene)
    except Exception as e:
        print(e)
