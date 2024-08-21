#version 330 core
out vec4 FragColor;

in vec2 TexCoords;
in vec3 FragPos;
in vec3 Normal;

uniform sampler2D texture1;

struct Light {
    vec3 position;
    vec3 color;
};

uniform Light lights[4]; // Support up to 4 lights
uniform vec3 viewPos;

void main()
{
    vec3 ambient = 0.1 * vec3(texture(texture1, TexCoords));
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);

    vec3 result = ambient;

    for (int i = 0; i < 4; ++i) {
        vec3 lightDir = normalize(lights[i].position - FragPos);
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = diff * vec3(texture(texture1, TexCoords));

        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
        vec3 specular = lights[i].color * spec;

        result += (diffuse + specular) * lights[i].color;
    }

    FragColor = vec4(result, 1.0);
}
