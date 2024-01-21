def onSetupParameters(op):
	#Everything in this section exposes a different variable to the Script SOP parameter page.
	page = op.appendCustomPage('Custom')

	p = page.appendInt('Shellnum', label='Shell Count')[0]
	p.min = 2
	p.max = 50
	p.normMin = p.min
	p.normMax = p.max
	p.clampMin = True
	p.clampMax = True
	
	p = page.appendInt('Radialsegments', label='Radial Segments')[0]
	p.min = 1
	p.max = 50
	p.normMin = p.min
	p.normMax = p.max
	p.clampMin = True
	p.clampMax = True
	
	p = page.appendFloat('Topshellmaxsize', label='Top Shell Max Size')[0]
	p.min = 0.0
	p.max = 1.0
	p.normMin = p.min
	p.normMax = p.max
	p.clampMin = True
	p.clampMax = True

	p = page.appendFloat('Height', label='Shape Height')[0]
	p.min = 1
	p.max = 50
	p.normMin = p.min
	p.normMax = p.max
	p.clampMin = True
	p.clampMax = True

	p = page.appendFloat('Conesize', label='Cone Size')[0]
	p.min = 1
	p.max = 10
	p.normMin = p.min
	p.normMax = p.max
	p.clampMin = True
	p.clampMax = True

	p = page.appendFloat('Distance', label='Distance')[0]
	p.min = 1
	p.max = 100
	p.normMin = p.min
	p.normMax = p.max
	p.clampMin = True
	p.clampMax = False

	p = page.appendInt('Densityx', label='Columns (x)')[0]
	p.min = 1
	p.max = 100
	p.normMin = p.min
	p.normMax = p.max
	p.clampMin = True
	p.clampMax = True

	p = page.appendInt('Densityz', label='Rows (z)')[0]
	p.min = 1
	p.max = 100
	p.normMin = p.min
	p.normMax = p.max
	p.clampMin = True
	p.clampMax = True

	p = page.appendToggle('Normals', label='Compute Normals')[0]


	return

def onPulse(par):
	return

def onCook(op):
	import math

	op.clear()

	# Applies parameters to variables
	radseg = op.par.Radialsegments.eval()
	topsize = op.par.Topshellmaxsize.eval()
	Shellnum = op.par.Shellnum.eval()
	height = op.par.Height.eval()
	size = op.par.Conesize.eval()
	Densityz = op.par.Densityz.eval()
	Densityx = op.par.Densityx.eval()
	dist = op.par.Distance.eval()
	norm = op.par.Normals

	stepsize = (topsize * size) / (Shellnum - 1)
	heightstep = height / (Shellnum - 1)

  ############
  # POINT CALC
  ############
	
	# calculates where each point goes
	for l in range(Densityz):
		for k in range(Densityx):
			for i in range(Shellnum):
				newHeight = i * heightstep
				for j in range(radseg - 1, -1, -1):
					p = op.appendPoint()
					newRadius = size - (stepsize * i)
					p.x = math.cos(math.pi * 2 * j / radseg) * newRadius + (k * dist)
					p.y = newHeight
					p.z = math.sin(math.pi * 2 * j / radseg) * newRadius + (l * dist)

					# applies point normals to each point
					if (norm):
						op.pointAttribs.create('N')
						p.N = (0, 1, 0)
	

  ################
  # PRIMITIVE CALC
  ################

	# this ineligant monstrosity splits each of the "shell plates" into triangles
	# and draws primatives accordingly
	total = int(Shellnum * Densityx * Densityz)
	for i in range(total):
		for j in range(radseg - 2):
			pt1 = j + 1
			if (radseg % 2 and pt1 < (radseg/2)):
				pt2 = pt1 - 1
				pt3 = (radseg - 1) - j
			elif (pt1 < (radseg/2)):
				pt2 = pt1 - 1
				pt3 = (radseg - 1) - j
			elif (pt1 == (radseg/2)):
				pt2 = pt1 - 1
				pt3 = pt3
			else:
				if (radseg % 2):
					pt2 = pt2
					pt3 = pt3 + 1
				else:
					pt2 = pt2 - 1
					pt3 = pt3 + 1
			apt1 = int(pt1 + (i * radseg))
			apt2 = int(pt2 + (i * radseg))
			apt3 = int(pt3 + (i * radseg))
			poly = op.appendPoly(3, closed=True, addPoints=False)
			poly[0].point = op.points[apt3]
			poly[1].point = op.points[apt2]
			poly[2].point = op.points[apt1]
			if (pt1 > (radseg/2)):
				if (radseg % 2):
					pt2 = pt2 - 1
		
	return
