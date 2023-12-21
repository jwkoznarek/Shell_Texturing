def onSetupParameters(op):
	page = op.appendCustomPage('Custom')
	return

def onPulse(par):
	return

def onCook(op):
	import math

	op.clear()

	rseg = 10
	radius = 1
	hseg = 3

  ##
  # POINTS
  ##
  
	for i in range(hseg):
		for j in range(rseg - 1, -1, -1):
			p = op.appendPoint()
			newRadius = radius / (i + 1) # size should be normalized between 0 and 1 for additional shells
			p.x = math.cos(math.pi * 2 * j / rseg) * newRadius
			p.y = i
			p.z = math.sin(math.pi * 2 * j / rseg) * newRadius

  ##
  # PRIMITIVES
  ##
  
	k = 0

	for i in range (hseg):
		poly = op.appendPoly(rseg, closed=True, addPoints=False)
		for j in range(rseg):
			n = j + i * rseg
			poly[j].point = op.points[n]
			print(j)
		
	return
