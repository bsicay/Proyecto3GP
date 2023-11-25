# mediante el lenguaje GLSL: 
vertex_shader ='''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

out vec2 TexCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    TexCoords = texcoords;    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
}
'''

fragment_shader ='''
#version 450 core

out vec4 fragColor;

in vec2 TexCoords;

uniform sampler2D tex;

void main()
{    
    fragColor = texture(tex, TexCoords);
}

'''

# !+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

vertex_shader_animation ='''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 norms;
out vec3 pos;

void main()
{    
    UVs = texcoords;           
    norms = normals;
    pos = (modelMatrix * vec4(position + (normals * sin(time * 3)) / 10, 1.0)).xyz;
     
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position + (normals * sin(time * 3)) / 10, 1.0);
}
'''

fragment_shader_animation ='''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;

uniform sampler2D tex;

void main()
{        
    float intensity = dot(norms, normalize(pointLight - pos));
    fragColor = texture(tex, UVs);
}
'''

# !+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

vertex_shader_color ='''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec4 vertexColor;
out vec2 TexCoords;

void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    TexCoords = texcoords;    
    vertexColor = vec4(0, 1.0, 0, 1.0);
}
'''

fragment_shader_color ='''
#version 450 core

out vec4 fragColor;

in vec4 vertexColor;

in vec2 TexCoords;
uniform sampler2D tex;

void main()
{
    fragColor = texture(tex, TexCoords) * vertexColor;
}
'''

# !+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

vertex_shader_best = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

out vec2 TexCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 Normal;
out vec2 UVs;
out vec3 pos;

void main()
{
    UVs = texcoords;           
    Normal = normals;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
}

'''

toon_shader_fs = '''
#version 450 core

out vec4 fragColor;

in vec3 Normal;
in vec3 pos;

uniform vec3 pointLight;

in vec2 TexCoords;

uniform sampler2D tex;

void main()
{    
    float intensity = dot(normalize(pointLight - pos), Normal);
    
    vec4 newColor;
    if (intensity < 0.20)       newColor = vec4(0.2, 0.2, 0.2, 1.0);
    else if (intensity < 0.50)  newColor = vec4(0.4, 0.4, 0.4, 1.0);
    else if (intensity < 0.80)  newColor = vec4(0.7, 0.7, 0.7, 1.0);
    else if (intensity <= 1)    newColor = vec4(1.0, 1.0, 1.0, 1.0);

    fragColor = texture(tex, TexCoords) * newColor;
}
'''

# !+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
rainbow_fs = '''
#version 450 core

out vec4 fragColor;

in vec3 Normal;
in vec3 pos;

uniform vec3 pointLight;

in vec2 TexCoords;

uniform sampler2D tex;

void main()
{
    float intensity = dot(normalize(pointLight - pos), Normal);
    
    vec4 newColor  = vec4(1.0, 0.0, 1.0, 1.0);
    if (intensity > 0.80)      newColor = vec4(0.0, 0.0, 1.0, 1.0);
    else if(intensity > 0.60)  newColor = vec4(0.0, 1.0, 0.0, 1.0);
    else if(intensity > 0.40)  newColor = vec4(0.0, 0.5, 0.0, 1.0);
    else if(intensity > 0.20)  newColor = vec4(1.0, 1.0, 0.0, 1.0);
    
    fragColor = texture(tex, TexCoords) * newColor;
}
'''

# !+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

party_extreme_vs = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 UVs;
out vec3 norms;

out vec2 TexCoords;

out vec3 vertexRed;
out vec3 vertexBlue;
out vec3 vertexGreen;

void main()
{    
    TexCoords = texcoords;       
    norms = normals;    
    vertexRed = vec3(1.0, 0.0, 0.0);
    vertexBlue = vec3(0.0, 1.0, 0.0);
    vertexGreen = vec3(0.0, 0.0, 1.0);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);;
}
'''

multicolor_shader = '''
#version 450 core

out vec4 fragColor;

in vec2 TexCoords;
in vec3 norms;

uniform float time;

uniform sampler2D tex;

in vec3 vertexRed;
in vec3 vertexBlue;
in vec3 vertexGreen;

void main()
{        
    float theta = time * 5.0;
    
    vec3 dir1 = vec3(cos(theta), 0, sin(theta)); 
    vec3 dir2 = vec3(sin(theta), 0, cos(theta));
    vec3 dir3 = vec3(cos(theta), sin(theta), 0);
    
    float diffuse1 = pow(dot(norms, dir1), 2.0);
    float diffuse2 = pow(dot(norms, dir2), 2.0);
    float diffuse3 = pow(dot(norms, dir3), 2.0);
    
    vec3 color1 = diffuse1 * vertexBlue;
    vec3 color2 = diffuse2 * vertexGreen;
    vec3 color3 = diffuse3 * vertexRed;
  
    vec4 newColor;
    newColor = vec4(color1 + color2 + color3, 1.0);
    fragColor = texture(tex, TexCoords) * newColor;
}
'''

# !+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

mix_two_textures_vs = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

out vec2 TexCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    TexCoords = vec2(texcoords.x, texcoords.y);
}
'''

mix_two_textures_fs = '''
#version 450 core

out vec4 fragColor;

in vec2 TexCoords;

uniform sampler2D tex;
uniform sampler2D tex2;

void main()
{        
    fragColor = mix(texture(tex, TexCoords), texture(tex2, TexCoords), 0.3);
}
'''

# !+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++