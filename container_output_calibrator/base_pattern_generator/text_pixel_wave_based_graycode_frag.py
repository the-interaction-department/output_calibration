const vec2 res = uTDOutputInfo.res.zw;
uniform int pattern_index;
uniform int num_patterns;
uniform bool is_horizontal;

out vec4 fragColor;

void main()
{
	vec4 color = vec4(1.0);
	float orientation = is_horizontal ? vUV.s : vUV.t;
	float orientation_resolution = is_horizontal ? res.x : res.y;
	
	// Offset is used to make the first pattern (index 0) all white.
	// Order of declaration matters
	float offset = 0.25;

	// Generate gray code patterns from coarse to fine
	int true_index = num_patterns - pattern_index;
	
	// Because we are showing each pattern AND its inverse we divide the true index by 2
	true_index = int(ceil(true_index / 2.0));
	
	// Generate a square wave
	float period = orientation_resolution / pow(2.0, true_index + 1);
	float scaled =  orientation * period;
	float fractional = fract(scaled + offset);
	float wave = step(0.5, fractional); 

	color = vec4(vec3(wave), 1.0);
	
	// Inverted patterns occur on odd indices
	if (pattern_index % 2 != 0) {
		color.rgb = 1.0 - color.rgb;
	}

	color = color * 2 - 1;

    fragColor = TDOutputSwizzle(color);
}
