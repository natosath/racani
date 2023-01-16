shader_type spatial;

uniform float curvature = -1.5;
uniform sampler2D noise;
uniform sampler2D normalmap;
uniform float pulse_speed = 5.0; // also has inverse relationship with radius size

varying vec2 tex_position;

float dist_from_center(vec2 position){
	return sqrt(pow(position.x - 0.5, 2.0) 
		+ pow(position.y - 0.5, 2.0));
}

void vertex() {
	VERTEX.y = curvature * (0.7 - dist_from_center(UV)); // 0.7 ~= 1/sqrt(2)
}

void fragment() {
	vec2 pos = VERTEX.xz;
	tex_position = VERTEX.xz / 2.0 + 0.5;
	vec4 tex = texture(noise, tex_position);
	float dist = dist_from_center(UV);
	ALBEDO = tex.xyz;
	if(dist <= 0.4){
		ALBEDO -=  pulse_speed * abs(sin(TIME)) * dist;
	} else{
		ALBEDO -= vec3(1,1,1);
	}
}