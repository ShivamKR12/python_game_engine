# Vertex Shader for Reflection Mapping

#version 330 core

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;

out vec3 FragPos;
out vec3 Normal;
out vec3 ReflectDir; // Reflection direction

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    FragPos = vec3(model * vec4(in_position, 1.0));
    Normal = mat3(transpose(inverse(model))) * in_normal;  
    gl_Position = projection * view * vec4(FragPos, 1.0);
    
    // Calculate reflection direction
    ReflectDir = reflect(normalize(FragPos - cameraPos), Normal);
}

# Fragment Shader for Reflection Mapping

#version 330 core

out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;
in vec3 ReflectDir;

uniform samplerCube skybox; // Cube map for reflection

void main()
{
    // Sample from the cube map
    vec3 reflection = texture(skybox, ReflectDir).rgb;
    FragColor = vec4(reflection, 1.0);
}
