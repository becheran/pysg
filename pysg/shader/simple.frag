#version 330

// TODO in vec3 v_color;
out vec4 f_color;

void main() {
    f_color = vec4(0.3, 0.5, 1.0, 1.0);
    // TODO We're not interested in changing the alpha value
    // TODO f_color = vec4(v_color, 1.0);
}