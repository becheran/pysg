""" Render all types of 3D objects to images. """

from PIL import Image
from pyrr import Vector3

from pysg.camera import PerspectiveCamera
from pysg.light import PointLight
from pysg.object_3d import CubeObject3D, IcosahedronObject3D, PlaneObject3D, CircleObject3D, TriangleObject3D, \
    CylinderObject3D, TetrahedralObject3D, PyramidObject3D
from pysg.renderer import HeadlessGLRenderer
from pysg.scene import Scene

width = 300
height = 300
camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
camera.local_position += Vector3([0, 0, 2])
scene = Scene(background_color=(1, 1, 1), ambient_light=(0.2, 0.2, 0.2))
light = PointLight(color=(0.8, 0.8, 0.8), name="PointLight")
light.world_position = Vector3([0.2, 0.5, 2])
renderer = HeadlessGLRenderer(scene, camera, width=width, height=height)

objects = [
    CubeObject3D(1, 1, 1, name="Cube"),
    IcosahedronObject3D(1, name="Icosahedron"),
    CylinderObject3D(0.7, 0.3, name="Cylinder"),
    TetrahedralObject3D(1, name="Tetrahedral"),
    PyramidObject3D(1, 1.5, name="Pyramid"),
    PlaneObject3D(1, 1, name="Plane"),
    CircleObject3D(0.7, name="Circle"),
    TriangleObject3D(1, 1, name="Triangle"),
]

angles = [
    Vector3([0, 45, 0]),
    Vector3([20, 45, 30]),
    Vector3([25, 0, 0]),
    Vector3([0, 25, 12]),
    Vector3([25, 45, 0]),
    Vector3([-90, 0, 0]),
    Vector3([-90, 0, 0]),
    Vector3([-90, 180, 0]),
]


colors = [
    (0.9, 0.5, 0.4),
    (0.5, 0.4, 0.9),
    (0.5, 0.9, 0.4),
    (0.9, 0.9, 0.3),
    (0.3, 0.9, 0.9),
    (0.9, 0.3, 0.9),
    (0.2, 0.3, 0.9),
    (0.2, 0.9, 0.3),
]

for obj, ang, color in zip(objects, angles, colors):
    scene.clear()
    obj.color = color
    scene.add(obj)
    scene.add(light)
    obj.local_euler_angles = ang
    renderer.render()
    current_image_data = renderer.current_image()
    img = Image.frombytes('RGB', (width, height), current_image_data, 'raw', 'RGB', 0, -1)
    img.save("../docs/img/objects_3d/" + obj.name + ".jpg")
