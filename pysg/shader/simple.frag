#version 330

uniform vec3 ObjectColor;
uniform vec3 AmbientLight;
uniform vec3 PointLightPosition;
uniform vec3 PointLightColor;
uniform mat4 ModelMatrix;

in vec3 v_vert;
in vec3 v_norm;

out vec4 f_color;

void main() {
    mat3 normalMatrix = transpose(inverse(mat3(ModelMatrix)));
    vec3 normal = normalize(normalMatrix * v_norm);
    vec3 fragPosition = vec3(ModelMatrix * vec4(v_vert, 1));

    vec3 surfaceToLight = PointLightPosition - fragPosition;
    //float diff = max(dot(normal, surfaceToLight), 0.);
    float brightness = dot(normal, surfaceToLight) / (length(surfaceToLight) * length(normal));
    float diff = clamp(brightness, 0, 1);

    vec3 diffuse = diff * PointLightColor;

    f_color = vec4(ObjectColor * (AmbientLight + diffuse),1);
}