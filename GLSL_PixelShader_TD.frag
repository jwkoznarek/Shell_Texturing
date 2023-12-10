uniform float uShellCount;
uniform float uDensity;
uniform vec2 uNoise;
uniform float uThickness;
uniform float uReset;
uniform vec4 uColor;

vec4 newColor;

//NEW 
float hash (uint n){
	n = (n << 13U) ^ n;
	n = n * (n * n * 15731U + 0x789221U) + 0x1376312;
	return float(n & uint(0x7fffffffU)) / float(0x7fffffff);
}

out vec4 fragColor;
void main()
{	
	//Color
	float alpha = uTDCurrentDepth + 1;
	float taper = alpha / uShellCount;

	// 'uReset' references a Constant -> Feedback -> Math CHOP network. Each channel in the constant is referenced at each of the uniforms above.
	// Whenever a change is applied to any constants, the Feedback -> Math returns the amount that value changed by,
	// and this 'if' wipes the 2D array before it's redrawn with the updated values.
	if(uReset != 0) newColor = vec4(0.0);
	else {
	vec3 newUV = vUV * uDensity;
	vec3 localUV = fract(newUV) * 2 - 1;
	float localDistanceFromCenter = length(localUV.xy);
	uvec3 tid = uvec3(newUV);
	uint seed = tid.x + 60 * tid.y + 100 * 10;
	float rand = mix(uNoise.x, uNoise.y, hash(seed));
	float h = uTDCurrentDepth / uShellCount;
	bool outsideThickness = (localDistanceFromCenter) > (uThickness * (rand - h));
	bool newShellIndex = uTDCurrentDepth > 0;
	if (outsideThickness && newShellIndex) discard;
	newColor = vec4(taper*uColor.rgb, uColor.a);
	}

	vec4 color = newColor;
	fragColor = TDOutputSwizzle(color);
}
