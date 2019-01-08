"""
    Renders a simple cube
"""
# TODO remove once api is released
import sys
sys.path.append("..")  # Adds higher directory to python modules path.

from pysg.material import BasicMaterial
from pysg.model_3d import Model3D
from pysg.camera import PerspectiveCamera
from pysg.scene import Scene
from pysg.renderer import GLRenderer
from pysg.geometry import BoxGeometry

width = 800
height = 600
camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
scene = Scene()
renderer = GLRenderer(scene, camera)

geometry = BoxGeometry(1, 1, 1)
material = BasicMaterial()
cube = Model3D(geometry, material)
scene.add(cube)

camera.position.z = 5
