""" Renders a simple cube. """
from example_qt5_window import Example, run_example
from pyrr import Vector3

from pysg.camera import PerspectiveCamera
from pysg.light import PointLight
from pysg.object_3d import CubeObject3D
from pysg.renderer import GLRenderer
from pysg.scene import Scene


class SimpleScene(Example):
    def __init__(self):
        width = self.WINDOW_SIZE[0]
        height = self.WINDOW_SIZE[1]
        camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
        scene = Scene(background_color=(1, 1, 1), ambient_light=(0.2, 0.2, 0.2))
        light = PointLight(color=(0.8, 0.8, 0.8))
        light.world_position = Vector3([1, 1, 1])
        scene.add(light)
        self.cube = CubeObject3D(1, 1, 1, color=(0.4, 0.5, 0.9))
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
