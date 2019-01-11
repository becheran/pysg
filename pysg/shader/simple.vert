#version 330

uniform mat4 Mvp;

in vec3 in_vert;
// TODO in vec3 in_norm;
// TODO in vec3 in_text;

// TODO out vec3 v_vert;
// TODO out vec3 v_norm;
// TODO out vec3 v_text;

void main() {
	// TODO v_vert = in_vert;
	// TODO v_norm = in_norm;
	// TODO v_text = in_text;
	gl_Position = Mvp * vec4(in_vert, 1.0);
}
