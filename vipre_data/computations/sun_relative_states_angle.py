import numpy as np
from numpy import linalg as la

def sun_relative_states_angle(R_b_s,R_b_e,R,V):
	# compute sun and earth relative angles for column vectors

	# inputs:
	#    R: position of spacecraft relative to body (assumed to be at time of entry)
	#    V: Orbital Velocity
	#    R_b_s: psition from body to sun
	#    R_b_e:position from body to earth

	# outputs:
	#    solar_phase: solar phase angle -> angle between Sun-Body line and interplanetary V infinity
	#    solar_conj: solar conjunction angle -> Sun-Earth-S/C angle
	#    solar_incidence: solar incidence angle -> angle between sun and entry position 

	solar_phase=np.arccos(np.diag(np.dot(R_b_s.T,V))/la.norm(V,axis=0)/la.norm(R_b_s,axis=0));#angle between sun and V
	solar_conj=np.arccos(np.diag(np.dot(R_b_s.T,R_b_e))/la.norm(R_b_e,axis=0)/la.norm(R_b_s,axis=0));#conjunction angle
	solar_incidence=np.arccos(np.diag(np.dot(R_b_s.T,R))/la.norm(R,axis=0)/la.norm(R_b_s,axis=0));#angle between sun and entry position

	return(solar_phase,solar_conj,solar_incidence)