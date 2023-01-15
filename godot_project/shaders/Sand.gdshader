shader_type spatial;
render_mode ambient_light_disabled;

uniform sampler2D noise;
uniform sampler2D extraNoise;
uniform sampler2D normalmap;
uniform vec3 sand_color = vec3(0.9, 0.2, 0.1);
uniform float bump = 2.0;
uniform float waviness = 70.0;
uniform float wave_frequency = 13.0;
uniform float depth = 1.0;
uniform vec2 velocity = vec2(0.5,0);


// Wave function modified a code snippet from url:
// https://godotshaders.com/shader/anime-esque-quicksand-shader/
// It is shared under an MIT license
vec3 get_wave(vec2 pos){
	pos += velocity; // add TIME to animate
	return normalize( vec3( sin( sin( pos.y * waviness ) * bump + pos.x * wave_frequency ) * 0.2 + sand_color) );
}

float height(vec2 pos){
	vec3 wave = get_wave(pos);
	return bump * wave.y;
}

void vertex() {
	VERTEX.y = height(UV);
	vec4 tex = texture(noise, UV);
	VERTEX +=  tex.xyz * 0.3;
}

void fragment(){
	vec4 tex = texture(extraNoise, UV);
	RIM = 0.001;
	ROUGHNESS = 1.2;
	NORMALMAP = get_wave(UV);
	NORMALMAP += tex.xzy;
	NORMALMAP_DEPTH = depth;
	ALBEDO = sand_color;
}