# vertex shader for shadow map

#version 330 core

layout(location = 0) in vec3 in_position;
uniform mat4 light_space_matrix;

void main()
{
    gl_Position = light_space_matrix * vec4(in_position, 1.0);
}

# fragment shader for shadow map

#version 330 core

void main()
{
}

# vertex shader

#version 330 core

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;

out vec3 FragPos;
out vec3 Normal;
out vec4 ShadowCoord; // Shadow coordinate

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 light_space_matrix; // Light space matrix for shadow mapping

void main()
{
    FragPos = vec3(model * vec4(in_position, 1.0));
    Normal = mat3(transpose(inverse(model))) * in_normal;  
    gl_Position = projection * view * vec4(FragPos, 1.0);
    
    // Calculate shadow coordinate
    ShadowCoord = light_space_matrix * vec4(FragPos, 1.0);
}

# fragment shader

#version 330 core

out vec4 FragColor;

struct Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
};

struct Light {
    vec3 position;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

uniform Material material;
uniform Light light;
uniform sampler2DShadow shadow_map; // Shadow map sampler

in vec3 FragPos;
in vec3 Normal;
in vec4 ShadowCoord;

float CalcShadow(sampler2DShadow shadowMap, vec4 shadowCoord) {
    vec3 projCoords = shadowCoord.xyz / shadowCoord.w;
    float depth = projCoords.z;
    vec2 texCoord = projCoords.xy;
    
    float shadow = 1.0;
    float bias = 0.005;
    
    if (texture(shadowMap, vec3(texCoord, (depth - bias))) < depth) {
        shadow = 0.0;
    }
    
    return shadow;
}

void main()
{
    // Calculate shadow factor
    float shadow = CalcShadow(shadow_map, ShadowCoord);
    
    // Ambient
    vec3 ambient = light.ambient * material.ambient;
    
    // Diffuse 
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(light.position - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = light.diffuse * (diff * material.diffuse) * shadow;
    
    // Specular
    vec3 viewDir = normalize(-FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = light.specular * (spec * material.specular) * shadow;
    
    vec3 result = ambient + diffuse + specular;
    FragColor = vec4(result, 1.0);
}
