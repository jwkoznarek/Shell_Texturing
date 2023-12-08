uniform float uShellCount;
uniform float uDensity;
uniform vec2 uNoise;
uniform float uThickness;

float hash(uint n){
	n = (n << 13U) ^ n;
	n = n * (n * n * 15731U + 0x789221U) + 0x1376312;
	return float(n & uint(0x7fffffffU)) / float(0x7fffffff);
}
out vec4 fragColor;
void main()
{
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
	vec4 color = vec4(localUV.rg, 0.0, 1.0);
	fragColor = TDOutputSwizzle(color);
}
