shader_type spatial;

uniform sampler2D noise;
uniform sampler2D normalmap;
uniform float frequency = 1.0;
uniform float scale = 1.5;

varying vec2 tex_position;

void vertex() {
	tex_position = VERTEX.xz / 2.0 + 0.5;
	float height = texture(noise, tex_position).x;
	float z =  texture(noise, tex_position).y;
	VERTEX.y += (height * sin(TIME * VERTEX.x * frequency) * scale);
	VERTEX.z = z * height;
}

void fragment() {
	ALBEDO = vec3(VERTEX.x, VERTEX.y, VERTEX.z);
}