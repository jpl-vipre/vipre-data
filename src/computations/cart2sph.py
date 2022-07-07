import numpy as np
from numpy import linalg as la

def cart2sph(x,y,z) -> float:
	"""
	Convert from body centered cartesian coordinates to spherical coordinate (lat, lon, r). Does not account for rotation of body, ie not body fixed

	:inputs:
	x: x components of vector, x should be the direction of the prime meridian
	y: y components of vector
	z: z components of vector, y should be the 

	:return:
	r: radius from origin in units of input
	el: elevation in deg, 90 deg at north pole, -90 deg at south pole
	az: azimuth in deg, 0 is x-aligned and right handed
	
	"""

	r=np.sqrt(np.square(x)+np.square(y)+np.square(z))
	el=np.arctan2(z,np.sqrt(np.square(x)+np.square(y)))
	az=np.arctan2(y,x)
	return(r,np.rad2deg(el),np.rad2deg(az))