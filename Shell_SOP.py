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
	
	p = page.appendInt('Radial', label='Radial Segments')[0]
	p.min = 1
	p.max = 50
	p.normMin = p.min
	p.normMax = p.max
	p.clampMin = True
	p.clampMax = True
	
	p = page.appendFloat('Fdeg', label='Top Shell Max Size')[0]
	p.min = 0.0
	p.max = 1.0
	p.normMin = p.min
	p.normMax = p.max
	p.clampMin = True
	p.clampMax = True

	p = page.appendFloat('Shelldist', label='Shell Distance')[0]
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
	p.clampMax = True

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
	rseg = op.par.Radial.eval()
	Fdeg = op.par.Fdeg.eval()
	Shellnum = op.par.Shellnum.eval()
	sdist = op.par.Shelldist.eval()
	csize = op.par.Conesize.eval()
	Densityz = op.par.Densityz.eval()
	Densityx = op.par.Densityx.eval()
	dist = op.par.Distance.eval()

  ############
  # POINT CALC
  ############
  
	for l in range(Densityz):
		for k in range(Densityx):
			for i in range(Shellnum):
				for j in range(rseg - 1, -1, -1):
					p = op.appendPoint()
					h = i / Shellnum
					newRadius = (csize - (h - (Fdeg * h)))
					p.x = math.cos(math.pi * 2 * j / rseg) * newRadius + (k * dist)
					p.y = i * (sdist * 0.1)
					p.z = math.sin(math.pi * 2 * j / rseg) * newRadius + (l * dist)
  ################
  # PRIMITIVE CALC
  ################
  
	total = int(Shellnum * Densityx * Densityz)
	for i in range(total):
		poly = op.appendPoly(rseg, closed=True, addPoints=False)
		for j in range(rseg):
			n = j + (i * rseg)
			poly[j].point = op.points[n]
		
	print('points ' + str(i * rseg) + ' polygons: ' + str(i))
	return
