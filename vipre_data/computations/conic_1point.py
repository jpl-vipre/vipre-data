import numpy as np
from numpy import linalg as la


def conic_1point(r_1, v_1, t_1, ta_step, mu, time_flag) -> float:
    """
    Compute an array of N points along a conic orbit from one postion of the trajectory.
    Input vectors and arrays of vectors are expected as 3xN np.arrays where rows are x,y,z
    components and N is the number of array entries.

    :inputs:
    r_i: sun centered position at time i [km]
    v_i: conic velocity at time i[km/s]
    t_i: time i [days past high noon 1/1/2000]. Unused if not performing revolution check
    ta_step: true anomaly angular step count
    mu: gravity constant of central body [km3/s2]
    revolutions based on input time. 1 to toggle on
    time_flag: flag indication whether or not to compute the time at each
    orbit point. 1 to toggle on
    :return:
    pos_set: position vector along trajectory in ta_step evenly spaced true anomaly steps
    vel_set: velocity vector along trajectory in ta_step evenlyspaced true anomaly steps
    time_set: time vector along trajectory in ta_step evenly spaced true anomaly steps. Must be specified in call

    Example inputs 1:
    ta_step=15
    mu=37931206.1590105
    r_1=np.array([[[-52570775.9381423],[-48053033.8464909],[-18714087.8322127]]])
    r_2=np.array([[[-5244.70404103397],[-28361.2929499602],[-54124.8468055892]]])
    rev_check=1
    t_1=np.array([[13701.5]])
    t_2=np.array([[13801.5]])
    time_flag=1
    v_1=np.array([[[5.92245272612931],[5.41349858784282],[2.08599922052923]]])
    v_2=np.array([[[-6.2516040802002],[5.34768724441528],[0.149426251649857]]])

    Example outputs 1:
    pos_set=[[[-5.25707759e+07 -1.21673667e+06 -5.31592774e+05 -3.07759404e+05
    -1.99866707e+05 -1.37785365e+05 -9.81666234e+04 -7.10857609e+04
    -5.16421229e+04 -3.71548327e+04 -2.60432933e+04 -1.73206216e+04
    -1.03420092e+04 -4.67031830e+03 -9.45874490e-10]] --->x position

    [[-4.80530338e+07 -1.11217472e+06 -4.85909617e+05 -2.81311676e+05
    -1.82690886e+05 -1.25944590e+05 -8.97305393e+04 -6.49769081e+04
    -4.72041859e+04 -3.39618809e+04 -2.38052270e+04 -1.58321501e+04
    -9.45325434e+03 -4.26896806e+03  3.03475645e-08]] ---y position

    [[-1.87140878e+07 -6.03207544e+05 -3.43148505e+05 -2.49076994e+05
    -1.98398914e+05 -1.65776165e+05 -1.42541635e+05 -1.24881780e+05
    -1.10836482e+05 -9.92852651e+04 -8.95360511e+04 -8.11354197e+04
    -7.37722072e+04 -6.72247139e+04 -6.13300000e+04]]] ---z position

    vel_set=[[[ 5.92245273  7.50255478  9.02927236 10.48916923 11.86939726
    13.15780942 14.34306677 15.41473819 16.36339218 17.18067991
    17.85940865 18.39360511 18.77856795 19.01090924 19.08858421]] --->x velocity

    [[ 5.41349859  6.8578124   8.25332939  9.58776802 10.84938424
    12.02707493 13.11047556 14.09005141 14.95718152 15.7042345
    16.32463575 16.8129253  17.16480583 17.37718055 17.44818041]] --->y velocity

    [[ 2.08599922  2.75728912  3.62623146  4.68517891  5.92481198
    7.33422099  8.90100212 10.61136658 12.4502619  14.40150449
    16.447922   18.57150447 20.75356284 22.97489341 25.21594688]]] --->z velocity

    time_set=[[[13701.5        13799.97685882 13800.95895667 13801.22754334
    13801.34002581 13801.39770096 13801.43114571 13801.4522512
    13801.46643116 13801.47643514 13801.48377758 13801.48934696
    13801.49369156 13801.49716419 13801.5       ]]]

    Example inputs 2:
    ta_step=12
    mu=132712440041.279
    r_1=np.array([[[-490781577.445248],[665883634.267565],[8483597.29825115]],[[-507338731.981395],[662408807.107071],[9041504.31209764]],[[-52570775.9381423],[-48053033.8464909],[-18714087.8322127]]])
    r_2=np.array([[[-1272998893.0951],[556745185.1877],[41012437.6064022]],[[-1284198529.59937],[533637648.158208],[41859341.5064153]],[[-5244.70404103397],[-28361.2929499602],[-54124.8468055892]]])
    rev_check=1
    t_1=np.array([[13079.7579005001],[13103.0297838546],[13701.5]])
    t_2=np.array([[13771.5],[13801.5],[13801.5]])
    time_flag=1
    v_1=np.array([[[-15.98380387215],[0.854676233590379],[0.614597010939183]],[[-15.8104622005541],[0.487581744461126],[0.6163084862148]],[[5.92245272612931],[5.41349858784282],[2.08599922052923]]])
    v_2=np.array([[[-10.739749897275],[-3.33432341479318],[0.476430938814154]],[[-10.4910612381906],[-3.60317735118423],[0.474128964364346]],[[-6.2516040802002],[5.34768724441528],[0.149426251649857]]])

    Example outsputs 2 exclude for brevity. X,Y,Z components will be stacked in pos, vel arrays as [[[X1],[X2],[X3]],[[Y1],[Y2],[Y3]],[[Z1],[Z2],[Z3]]]

    """

    # conic geometry
    h = np.cross(r_1, v_1, axis=1)  # angular momentum vector
    h_hat = (h.T[0] / la.norm(h, axis=1).T)[None].T  # unit vector of h
    r_hat = (r_1.T[0] / la.norm(r_1, axis=1).T)[None].T  # unit vector of r_1
    th_hat = np.cross(h_hat, r_hat, axis=1)  # tangential unit vector

    p = la.norm(h, axis=1) ** 2 / mu  # semi latus rectum
    energy = la.norm(v_1, axis=1) ** 2 / 2.0 - mu / la.norm(r_1, axis=1)  # orbital energy
    sma = -mu / (2.0 * energy)  # semi major axis
    ecc = np.sqrt(1.0 + (2.0 * energy * la.norm(h, axis=1) ** 2) / mu**2)  # eccentricity
    ta_1 = get_true_anomaly(p, ecc, r_1, v_1)  # true anomaly for point 1
    ta_2 = (
        np.pi * 15.0 / 180.0 * np.ones(np.shape(ta_1))
    )  # get_true_anomaly(p,ecc,r_2,v_2)#true anomaly for point 2
    inc = np.arccos(h_hat.T[0][2])[None].T  # inclination
    th = np.arctan2(r_hat.T[0][2], th_hat.T[0][2])[None].T  # orbit angle
    raan = np.arctan2(h_hat.T[0][0], -h_hat.T[0][1])[None].T  # right ascension of ascending node
    aop = th - ta_1  # argument of periapsis

    # generate positions
    ta = ta_2 - ta_1  # compute change in true anomaly
    wrap_ind = np.where(ta < 0)  # identify rotation wrap around
    if len(wrap_ind) > 0:
        ta[wrap_ind] = ta_2[wrap_ind] - ta_1[wrap_ind] + 2.0 * np.pi  # perform rotation wrapping

    ell_ind = np.where(ecc < 1.0)  # identifty elliptical cases
    period = np.zeros(np.shape(ta))
    revs = np.zeros(np.shape(ta))
    # if rev_check and len(ell_ind)>0:#count total number of orbits if specified
    # 	period[ell_ind]=2.*np.pi*np.sqrt(sma[ell_ind]**3/mu)#orbit period
    # 	revs[ell_ind]=np.floor((t_2[ell_ind]\
    # 		-t_1[ell_ind])*86400./period[ell_ind])#count revolutions based on time difference

    (E, P, H) = kep2cart_array(
        raan, aop, inc
    )  # conversion unit vectors from keplerian elements to cartesian
    ta_set = (
        np.linspace(np.zeros(np.shape(ta)), ta + 2.0 * np.pi * revs, ta_step, axis=1)
        + ta_1.T[None].T
    )  # true anomaly campling

    pos_set_E = (
        p.T[None].T / (1.0 + ecc.T[None].T * np.cos(ta_set)) * np.cos(ta_set)
    )  # E direction position
    pos_set_P = (
        p.T[None].T / (1.0 + ecc.T[None].T * np.cos(ta_set)) * np.sin(ta_set)
    )  # P direction position
    pos_set = (
        np.transpose(E, axes=[2, 0, 1]) * np.transpose(pos_set_E, axes=[2, 0, 1]).T
        + np.transpose(P, axes=[2, 0, 1]) * np.transpose(pos_set_P, axes=[2, 0, 1]).T
    ).T

    # generate velocities
    vel_set_E = -np.sqrt(mu / p.T[None].T) * np.sin(ta_set)  # E direction velocity
    vel_set_P = np.sqrt(mu / p.T[None].T) * (ecc.T[None].T + np.cos(ta_set))  # P direction velocity
    vel_set = (
        np.transpose(E, axes=[2, 0, 1]) * np.transpose(vel_set_E, axes=[2, 0, 1]).T
        + np.transpose(P, axes=[2, 0, 1]) * np.transpose(vel_set_P, axes=[2, 0, 1]).T
    ).T

    # generate times
    time_set = np.zeros((np.shape(np.transpose(ta_set, axes=[2, 0, 1]))))
    if time_flag == 1:
        dta_set = (
            np.transpose(ta_set, axes=[2, 0, 1]).T[1:].T[0]
            - np.transpose(ta_set, axes=[2, 0, 1]).T[0]
        )  # true anomaly differences
        time_set[0].T[0] = t_1.T  # initial time setting
        tof = (
            find_tof(
                np.transpose(pos_set, axes=[2, 0, 1])[0][None],
                np.transpose(pos_set, axes=[2, 0, 1])[1:],
                p,
                dta_set,
                mu,
            )
            / 86400.0
        )  # calculate time of flight
        rev_count = np.floor(dta_set / (2.0 * np.pi))  # count orbits
        revs_adjust = np.where((tof < 0))  # adjust for TOF algorithm angle wrapping
        rev_count[revs_adjust] = rev_count[revs_adjust] + 1
        time_set[0].T[1:] = (t_1 + tof + rev_count * period / 86400.0).T  # generate time array
    return (pos_set, vel_set, time_set)
    pass


def get_true_anomaly(p, ecc, r, v) -> float:
    """
    Compute true anomaly from position, velocity, Keplerian elements.
    Inputs can be scalar or 1xN np arrays

    :inputs:
    p: semi parameter of orbit [km]
    ecc: eccentricity
    r: positon vector in Cartesian space [km]
    v: velocity vector in Cartesian space [km/s]

    :return:
    ta: true anomaly [rad]
    """
    ta = np.arccos((p / la.norm(r, axis=1) - 1.0) / ecc)  # true anomaly
    quad_check = np.diag(np.dot(np.transpose(r, axes=[2, 0, 1]), v)[0].T[0])
    quad_ind = np.where(quad_check < 0)

    if len(quad_ind) > 0:
        ta[quad_ind] = 2.0 * np.pi - ta[quad_ind]  # apply quadrant fix
    return ta
    pass


def kep2cart_array(raan, aop, inc) -> float:
    """
    compute rotation from keplerian orbit elements to cartesian space as
    arrays: Vallado p. 126 algorithm 10 (COE2RV)
    Inputs can be scalar or 1xN np arrays

    :inputs:
    raan: array of right ascension of ascending node [rad]
    aop: array of argument of periapsis [rad]
    inc: array of inclination [rad]

    :return:
    E: eccentricity unit vector in Cartesian coordinates
    P: semi-latus rectum unit vector in Cartesian coordinates
    H: angular momentum unit vector in Cartesian coordinates
    """
    E = (
        np.array(
            [
                np.cos(raan) * np.cos(aop) - np.sin(raan) * np.sin(aop) * np.cos(inc),
                np.sin(raan) * np.cos(aop) + np.cos(raan) * np.sin(aop) * np.cos(inc),
                np.sin(aop) * np.sin(inc),
            ]
        )
        .T[0]
        .T[None]
        .T
    )  # eccentricity vector
    P = (
        np.array(
            [
                -np.cos(raan) * np.sin(aop) - np.sin(raan) * np.cos(aop) * np.cos(inc),
                -np.sin(raan) * np.sin(aop) + np.cos(raan) * np.cos(aop) * np.cos(inc),
                np.cos(aop) * np.sin(inc),
            ]
        )
        .T[0]
        .T[None]
        .T
    )  # semilatus rectum vector
    H = (
        np.array([np.sin(raan) * np.sin(inc), -np.cos(raan) * np.sin(inc), np.cos(inc)])
        .T[0]
        .T[None]
        .T
    )  # angular momentum vector

    return (E, P, H)
    pass


def find_tof(r0, r, p, delta_ta, mu):
    """
    compute conic orbit time of flight: Vallado p. 134 algorithm 11 (FINDTOF)
    Inputs can be scalar or MxN np arrays

    :inputs:
    r0: initial position vector on orbit [km]
    r: position vector on orbit after computed time of flight [km]. Excludes initial time value
    p: conic semi-parameter[km]
    delta_ta: change in true anomaly [rad]. Excludes initial time value
    mu: gravity constant of central body [km3/s2]

    :return:
    TOF: time of flight between r0 and r [sec]
    """

    # compute coefficients and f,g functions
    cos_delta_ta = np.cos(delta_ta)
    sin_delta_ta = np.sin(delta_ta)
    k = (la.norm(r0, axis=1) * la.norm(r, axis=1)).T * (1.0 - cos_delta_ta)
    l = (la.norm(r0, axis=1) + la.norm(r, axis=1)).T
    m = (la.norm(r0, axis=1) * la.norm(r, axis=1)).T * (1.0 + cos_delta_ta)
    a = m * k * p / ((2 * m - l**2) * p**2 + 2 * k * l * p - k**2)
    f = 1 - (la.norm(r, axis=1)).T * (1 - cos_delta_ta) / p
    g = (la.norm(r0, axis=1) * la.norm(r, axis=1)).T * sin_delta_ta / np.sqrt(mu * p)

    # check for conic types
    ellipse_check = np.unique(np.argwhere(a > 0).T[0])  # ellipse or circle condition
    parabola_check = np.unique(np.argwhere(a == 0).T[0])  # parabola condition
    hyperbola_check = np.unique(np.argwhere(a < 0).T[0])  # hyperbola condition

    TOF = np.zeros(np.shape(delta_ta))  # prepare time of flight array
    # ellipse case
    if len(ellipse_check) > 0:
        tan_half_delta_ta = sin_delta_ta[ellipse_check] / (1.0 + cos_delta_ta[ellipse_check])
        f_dot = (
            np.sqrt(mu / p[ellipse_check])
            * tan_half_delta_ta
            * (
                (1.0 - cos_delta_ta[ellipse_check]) / p[ellipse_check]
                - 1.0 / la.norm(r0.T[ellipse_check], axis=1)
                - 1.0 / la.norm(r.T[ellipse_check], axis=1)
            )
        )
        sin_delta_E = (
            -la.norm(r0.T[ellipse_check], axis=1)
            * la.norm(r.T[ellipse_check], axis=1)
            * f_dot
            / np.sqrt(mu * a[ellipse_check])
        )  # sin of change in eccentric anomaly
        cos_delta_E = (
            1.0
            - la.norm(r0.T[np.unique(ellipse_check)], axis=1)
            * (1.0 - f[ellipse_check])
            / a[ellipse_check]
        )  # cosine of change in eccentric anomaly
        delta_E = np.arctan2(sin_delta_E, cos_delta_E)  # change in eccentric anomal
        TOF[ellipse_check] = g[ellipse_check] + np.sqrt(a[ellipse_check] ** 3 / mu) * (
            delta_E - sin_delta_E
        )  # elliptical time of flight

    # parabola case
    if len(parabola_check) > 0:
        c = np.sqrt(
            la.norm(r0.T[parabola_check], axis=1) ** 2
            + la.norm(r.T[parabola_check], axis=1) ** 2
            - 2.0
            * la.norm(r0.T[parabola_check], axis=1)
            * la.norm(r.T[parabola_check], axis=1)
            * cos_delta_ta[parabola_check]
        )
        s = (la.norm(r0.T[parabola_check], axis=1) + la.norm(r.T[parabola_check], axis=1) + c) / 2.0
        TOF[parabola_check] = (
            2.0 / 3.0 * np.sqrt(s**3.0 / (2.0 * mu)) * (1.0 - ((s - c) / s) ** (3.0 / 2.0))
        )  # parabolic time of flight

    # hyperbola case
    if len(hyperbola_check) > 0:
        delta_H = np.arccosh(
            1
            + (f[hyperbola_check] - 1) * la.norm(r0.T[hyperbola_check], axis=1) / a[hyperbola_check]
        )  # change in hyperbolic anomaly
        TOF[hyperbola_check] = g[hyperbola_check] + np.sqrt((-a[hyperbola_check]) ** 3 / mu) * (
            np.sinh(delta_H) - delta_H
        )  # hyperbolic time of flight
    return TOF
    pass
