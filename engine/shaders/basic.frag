#version 330 core

out vec4 FragColor;

uniform vec3 color;
uniform float time;

void main()
{
    float pulse = 0.5 + 0.5 * sin(time);
    FragColor = vec4(color * pulse, 1.0);
}