# Vertex Shader for SSAO

#version 330 core

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;

out vec2 FragPos;

void main()
{
    gl_Position = vec4(in_position, 1.0);
    FragPos = in_position.xy;
}

# Fragment Shader for SSAO

#version 330 core

out float FragColor;

in vec2 FragPos;

uniform sampler2D depth_map; // Depth map sampler
uniform sampler2D noise_map; // Noise map sampler

const float radius = 0.5; // SSAO radius
const float bias = 0.025; // SSAO bias

void main()
{
    vec2 noise = texture(noise_map, FragPos * 0.25).rg; // Sample noise map
    vec2 texcoord = FragPos * 0.5 + 0.5; // Convert from [-1,1] to [0,1] range

    float occlusion = 0.0;
    for (int i = -3; i <= 3; i++)
    {
        for (int j = -3; j <= 3; j++)
        {
            vec2 sample = texcoord + noise * vec2(float(i), float(j)) * radius;
            float sample_depth = texture(depth_map, sample).r;
            occlusion += (FragPos.z - bias) >= sample_depth ? 1.0 : 0.0;
        }
    }
    occlusion /= 49.0; // Number of samples
    FragColor = 1.0 - occlusion;
}
