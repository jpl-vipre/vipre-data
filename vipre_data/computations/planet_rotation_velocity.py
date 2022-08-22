import numpy as np
from numpy import linalg as la

def planet_rotation_velocity(R,period):
	# Compute planetary rotation velocity in body frame at specified position. Subtract this from V_entry to get relative velocity in planet atmosphere or on surface

	# inputs:
	#    R: position on planet, column vectors
	#    period: rotational period in days

	# outputs:
	#    V: rotational velocity

	w=np.tile(np.array([[0.],[0.],[2.*np.pi/period/86400.]]),(1,np.shape(R)[1]))#angular velocity
	V=np.cross(R,w,axis=0)
	return V