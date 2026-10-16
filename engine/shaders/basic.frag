
#version 330 core

in vec3 FragPos;
in vec3 Normal;

out vec4 FragColor;

uniform vec3 color;
uniform vec3 viewPos;

const int MAX_LIGHTS = 4;

uniform int lightCount;
uniform vec3 lightPositions[MAX_LIGHTS];
uniform vec3 lightColors[MAX_LIGHTS];

void main()
{
    vec3 N = normalize(Normal);
    vec3 V = normalize(viewPos - FragPos);

    vec3 result = 0.12 * color;

    for (int i = 0; i < lightCount; i++)
    {
        vec3 lightVector = lightPositions[i] - FragPos;
        float distanceToLight = length(lightVector);
        vec3 L = normalize(lightVector);


        float diff = max(dot(N, L), 0.0);
        vec3 diffuse = diff * color * lightColors[i];

        float spec = 0.0;

        if (diff > 0.0)
        {
            vec3 R = reflect(-L, N);
            spec = pow(max(dot(V, R), 0.0), 32.0);
        }

        vec3 specular = 0.3 * spec * lightColors[i];

        float attenuation = 1.0 / (
            1.0
            + 0.09 * distanceToLight
            + 0.032 * distanceToLight * distanceToLight
        );

        result += attenuation * (diffuse + specular);
    }

    FragColor = vec4(result, 1.0);
}
