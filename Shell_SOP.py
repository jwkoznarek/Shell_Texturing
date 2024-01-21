def onSetupParameters(op):
	#Everything in this section exposes a different variable to the Script SOP parameter page.
	page = op.appendCustomPage('Custom')

	p = page.appendInt('Shellnum', label='Shell Count')[0]
	p.min = 1
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
	stepsize = (topsize * size) / (Shellnum - 1)
	heightstep = height / (Shellnum - 1)

  ############
  # POINT CALC
  ############
	
  
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

  ################
  # PRIMITIVE CALC
  ################
  
	total = int(Shellnum * Densityx * Densityz)
	for i in range(total):
		poly = op.appendPoly(radseg, closed=True, addPoints=False)
		for j in range(radseg):
			n = j + (i * radseg)
			poly[j].point = op.points[n]
		
	print('points ' + str(i * radseg) + ' polygons: ' + str(i))
	return
