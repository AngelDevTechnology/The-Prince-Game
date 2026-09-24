#version 330 core

layout (location = 0) in vec3 a_position;

uniform float time;

void main()
{
    float offset = sin(time) * 0.5;

    gl_Position = vec4(
        a_position.x + offset,
        a_position.y,
        a_position.z,
        1.0
    );
}