#version 330

uniform mat4 ModelMatrix;
uniform mat4 ViewProjectionMatrix;
uniform vec3 ModelSize;

in vec3 in_vert;
in vec3 in_norm;

out vec3 v_vert;
out vec3 v_norm;

void main() {
    gl_Position = ViewProjectionMatrix * ModelMatrix * vec4(in_vert * ModelSize, 1.0);
    v_norm = in_norm;
    v_vert = in_vert;
}