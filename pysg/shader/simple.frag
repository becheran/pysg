#version 330

uniform vec3 Color;

out vec4 f_color;

void main() {
    f_color = vec4(Color, 1.0);
}