# -*- coding: utf-8 -*-
""" All rendering related functions and classes

"""
import os

import moderngl
from pyrr import Vector3

from pysg.camera import Camera
from pysg.geometry import create_cube, create_plane
from pysg.scene import Scene


class Renderer:
    def __init__(self, scene: Scene, camera: Camera):
        """Base class which takes a scene and camera and render.

        Args:
            scene (Scene): Scene which shall be rendered.
            camera (Camera): Camera which is used to view scene.

        """
        self.scene = scene
        self.camera = camera
        self.ctx = None

    def _setup(self):
        """ Call this method from children as soon as context object was create.
        """
        self.ctx.enable(moderngl.CULL_FACE)
        self.ctx.front_face = 'ccw'
        self.ctx.enable(moderngl.DEPTH_TEST)
        shader_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'shader')
        self.prog = self.ctx.program(
            vertex_shader=open(os.path.join(shader_path, 'simple.vert')).read(),
            fragment_shader=open(os.path.join(shader_path, 'simple.frag')).read())
        self.object_color = self.prog['ObjectColor']
        self.ambient_light = self.prog['AmbientLight']
        self.point_light_position = self.prog['PointLightPosition']
        self.point_light_color = self.prog['PointLightColor']
        self.model_matrix = self.prog['ModelMatrix']
        self.view_projection_matrix = self.prog['ViewProjectionMatrix']
        self.model_size = self.prog['ModelSize']

        # Cube geometry buffers
        vertices, indices, normals = create_cube()
        vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        ibo = self.ctx.buffer(indices.astype('i4').tobytes())
        nbo = self.ctx.buffer(normals.astype('f4').tobytes())
        vao_content = [
            (vbo, '3f', 'in_vert'),
            (nbo, '3f', 'in_norm')
        ]
        self.cube_vao = self.ctx.vertex_array(self.prog, vao_content, index_buffer=ibo)

        # Plane geometry buffers
        v_plane, i_plane, n_plane = create_plane()
        vbo_plane = self.ctx.buffer(v_plane.astype('f4').tobytes())
        ibo_plane = self.ctx.buffer(i_plane.astype('i4').tobytes())
        nbo_plane = self.ctx.buffer(n_plane.astype('f4').tobytes())
        vao_content_plane = [
            (vbo_plane, '3f', 'in_vert'),
            (nbo_plane, '3f', 'in_norm')
        ]
        self.plane_vao = self.ctx.vertex_array(self.prog, vao_content_plane, index_buffer=ibo_plane)

    def _render(self) -> None:
        """ Call this method from subclasses to render all objects in the scene
        """
        self.ctx.clear(*self.scene.background_color)

        # Update projection matrices
        if self.scene.auto_update:
            self.scene.update_world_matrix()

        if self.camera._parent is None:
            self.camera.update_world_matrix()

        view_projection_mat44 = self.camera.projection_matrix * self.camera.world_matrix.inverse
        self.view_projection_matrix.write(view_projection_mat44.astype('f4').tobytes())
        self.ambient_light.value = self.scene.ambient_light

        # TODO implement several light sources and other types
        if len(self.scene.render_list.point_lights) > 0:
            self.point_light_color.value = self.scene.render_list.point_lights[0].color
            self.point_light_position.value = tuple(self.scene.render_list.point_lights[0].world_position)

        # Render all cubes
        for box_object_3d in self.scene.render_list.boxes:
            self.model_matrix.write(box_object_3d.world_matrix.astype('f4').tobytes())
            self.object_color.value = box_object_3d.color
            self.model_size.value = box_object_3d.size
            self.cube_vao.render(moderngl.TRIANGLES)

        for plane_object_3d in self.scene.render_list.planes:
            self.model_matrix.write(plane_object_3d.world_matrix.astype('f4').tobytes())
            self.object_color.value = plane_object_3d.color
            self.model_size.value = plane_object_3d.size
            self.plane_vao.render(moderngl.TRIANGLES)

    def render(self):
        raise NotImplementedError()


class GLRenderer(Renderer):

    def __init__(self, scene: Scene, camera: Camera):
        """Render the scene to a given viewport.

        Args:
            scene (Scene): Scene which shall be rendered.
            camera (Camera): Camera which is used to view scene.
        """
        super().__init__(scene, camera)
        self.ctx = moderngl.create_context()
        super()._setup()

        # Viewport is a tuple of size four (x, y, width, height).
        self.viewport = None

    def render(self) -> None:
        self.ctx.viewport = self.viewport
        super()._render()


class HeadlessGLRenderer(Renderer):

    def __init__(self, scene: Scene, camera: Camera, *, width: int, height: int):
        """Render the scene to a framebuffer which can be read to CPU RAM to be used as an image.

        Args:
            scene (Scene): Scene which shall be rendered.
            camera (Camera): Camera which is used to view scene.
            width (float): Width of output image in pixel
            height (float): Height of output image in pixel
        """

        super().__init__(scene, camera)
        self.ctx = moderngl.create_standalone_context()
        super()._setup()

        self.fbo = self.ctx.framebuffer(
            self.ctx.renderbuffer((width, height)),
            self.ctx.depth_renderbuffer((width, height)),
        )

    def render(self) -> None:
        """ Render the current scene and camera into a buffer.
        The buffer can later be returned with the 'current_image' method.
        """
        self.fbo.use()
        super()._render()

    def current_image(self) -> bytes:
        """ Render the current scene and camera into a buffer.
        The buffer can later be returned with the 'current_image' method.

        Returns:
            bytes: The rendered byte array. Copy from vRAM to RAM.
        """
        return self.fbo.read(components=3, alignment=1)
