shader_type spatial;

uniform sampler2D noise;
uniform sampler2D normalmap;
uniform float rotation_speed = 2.0;
uniform float emission_intensity = 3.0;
uniform vec3 sun_color = vec3(0.756 ,0.266, 0.05);

varying vec2 tex_position;

vec3 rotateYaxis(vec3 base, float rotation)
{
    mat3 rotation_matrix=mat3(vec3(cos(rotation), 0, -sin(rotation)),
	                       vec3(0, 1, 0),
                           vec3(sin(rotation), 0, cos(rotation)));
	return base * rotation_matrix;
}

vec3 rotateXaxis(vec3 base, float rotation)
{
    mat3 rotation_matrix=mat3(vec3(1, 0, 0),
	                       vec3(0, cos(rotation), -sin(rotation)),
                           vec3(0, sin(rotation), cos(rotation)));
	return base * rotation_matrix;
}

void vertex() {
	float rotation = mod(TIME, 6.3) * rotation_speed;
	VERTEX = rotateYaxis(VERTEX, rotation); // spin
	VERTEX = rotateXaxis(VERTEX, 0.4); // tilt
}

void fragment() {
	vec2 pos = VERTEX.xz;
	vec4 tex = texture(noise, UV);
	METALLIC = 0.0;
  	ROUGHNESS = 1.51;
	NORMALMAP = texture(normalmap, tex_position).xyz;
	ALBEDO = (sun_color - tex.xyz * 0.5);
	EMISSION = ALBEDO * emission_intensity * abs(sin(TIME));
}

//void light() {
//}