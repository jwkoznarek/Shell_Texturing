// uniform float exampleUniform;

//uniform int uShellIndex;
uniform int uShellCount;
uniform float uDensity;
uniform float uNoiseMin, uNoiseMax;
uniform float uThickness;

uniform sampler2DArray name;

float i;


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
	float localDistanceFromCenter = length(localUV);
	uvec3 tid = uvec3(newUV);
	uint seed = tid.x + 100 * tid.y + 100 * 10;
	float shellCount = uShellCount;
	float rand = mix(uNoiseMin, uNoiseMax, hash(seed));
	/*
	float shellIndex = uShellIndex;
	float h = shellIndex / shellCount;
	bool outsideThickness = (localDistanceFromCenter) > (uThickness * (rand - h));
	bool newShellIndex = uShellIndex > 0;
	if (outsideThickness && newShellIndex) discard;
	vec4 color = vec4(localUV, 1.0);
	fragColor = TDOutputSwizzle(color);
	*/

	for (i = 0; i <= uShellCount; i++) {
		/*
		vec3 newUV = vUV * uDensity;
		vec3 localUV = fract(newUV) * 2 - 1;
		float localDistanceFromCenter = length(localUV);
		uvec3 tid = uvec3(newUV);
		uint seed = tid.x + 100 * tid.y + 100 * 10;
		float shellCount = uShellCount;
		float rand = mix(uNoiseMin, uNoiseMax, hash(seed));
		*/
		float shellIndex = i;
		float h = shellIndex / shellCount;
		bool outsideThickness = (localDistanceFromCenter) > (uThickness * (rand - h));
		bool newShellIndex = shellIndex > 0;
		if (outsideThickness && newShellIndex) discard;
		vec4 color = vec4(localUV.rg, 0.0, 1.0);
		fragColor = TDOutputSwizzle(color);
	}
}
