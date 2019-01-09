"""
    Renders a simple cube
"""
# TODO remove once api is released
import sys
sys.path.append("..")  # Adds higher directory to python modules path.

from pysg import color
from pysg.material import BasicMaterial
from pysg.model_3d import Model3D
from pysg.camera import PerspectiveCamera, Camera
from pysg.scene import Scene
from pysg.renderer import GLRenderer
from pysg.geometry import BoxGeometry

from example_qt5_window import Example, run_example


class SimpleScene(Example):
    def __init__(self):
        width = self.WINDOW_SIZE[0]
        height = self.WINDOW_SIZE[1]
        camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
        scene = Scene(background_color=color.rgb["blue"], auto_update=True)
        geometry = BoxGeometry(1, 1, 1)
        material = BasicMaterial()
        cube = Model3D(geometry, material)
        scene.add(cube)  # TODO camera.position.z = 5
        self.renderer = GLRenderer(scene, camera)

    def update(self):
        self.renderer.viewport = self.wnd.viewport
        self.renderer.render()


try:
    run_example(SimpleScene)
except Exception as e:
    print(e)
