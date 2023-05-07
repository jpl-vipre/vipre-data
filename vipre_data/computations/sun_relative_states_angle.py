# Copyright (c) 2021-2023 California Institute of Technology ("Caltech"). U.S.
# Government sponsorship acknowledged.
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Caltech nor its operating division, the Jet Propulsion
#   Laboratory, nor the names of its contributors may be used to endorse or
#   promote products derived from this software without specific prior written
#   permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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