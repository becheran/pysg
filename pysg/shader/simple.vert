#version 330

uniform mat4 Mvp;

in vec3 in_vert;

void main() {
    gl_Position = Mvp * vec4(in_vert, 1.0);
}