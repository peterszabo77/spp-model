import numpy as np
from parameters import *

def getRandom3DUnitVector(): # Generates a random 3D unit vector (direction) with a uniform spherical distribution
	## method 1
	#phi = np.random.uniform(0,np.pi*2)
	#costheta = np.random.uniform(-1,1)
	#theta = np.arccos( costheta )
	#x = np.sin( theta) * np.cos( phi )
	#y = np.sin( theta) * np.sin( phi )
	#z = np.cos( theta )
	#return (x,y,z)
	# method 2
	xyz = np.random.randn(3)
	xyz /= np.sum(xyz**2)**0.5
	return xyz

def getUgridCellIndices(i,j,k):
	idxs = []
	ijk=np.array([i,j,k])
	chvalues = (0,1,-1)
	for chi in chvalues:
		for chj  in chvalues:
			for chk in chvalues:
				ch = np.array([chi,chj,chk]) 
				cellidxs = np.mod(ijk+ch,UGRIDLENGTH)
				idxs.append(cellidxs.tolist())
	return idxs
