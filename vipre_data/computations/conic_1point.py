from typing import Tuple, Any

import numpy as np
from numpy import linalg as la, ndarray


def conic_1point(
    r_1, v_1, t_1, ta_step, mu, rev_check, time_flag
) -> tuple[ndarray, ndarray, ndarray]:
    """
    Compute an array of N points along a conic orbit between two postions of the trajectory.
    Input vectors and arrays of vectors are expected as 3xN np.arrays where rows are x,y,z
    components and N is the number of array entries.
    :param r_1: sun centered position at time 1 [km]
    :param v_1: conic velocity at time 1 [km/s]
    :param t_1: time 1 [seconds past high noon 1/1/2000]. Unused if not performing revolution check
    :param ta_step: true anomaly angular step count
    :param mu: gravity constant of central body [km3/s2]
    :param rev_check: flag indicating whether to check for multiple revolutions based on input time. 1 to toggle on
    :param time_flag: flag indication whether to compute the time at each orbit point. 1 to toggle on
    :return:
        pos_set: position vector along trajectory in ta_step evenly spaced true anomaly steps
        vel_set: velocity vector along trajectory in ta_step evenlyspaced true anomaly steps
        time_set: time vector along trajectory in ta_step evenly spaced true anomaly steps. Must be specified in call
    See conic_2point for example use
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

    ell_ind = np.where(ecc < 1.0)  # identify elliptical cases
    period = np.zeros(np.shape(ta))
    revs = np.zeros(np.shape(ta))
    # if rev_check and len(ell_ind) > 0:  # count total number of orbits if specified
    #     period[ell_ind] = 2.0 * np.pi * np.sqrt(sma[ell_ind] ** 3 / mu)  # orbit period
    #     revs[ell_ind] = np.floor(
    #         (t_2[ell_ind] - t_1[ell_ind]) * 86400.0 / period[ell_ind]
    #     )  # count revolutions based on time difference

    (E, P, H) = kep2cart_array(
        raan, aop, inc
    )  # conversion unit vectors from keplerian elements to cartesian
    ta_set = (
        np.linspace(np.zeros(np.shape(ta)), ta + 2.0 * np.pi * revs, ta_step, axis=1)
        + ta_1.T[None].T
    )  # true anomaly sampling

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
    if time_flag:
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
        time_set[0].T[1:] = 86400. * (t_1 / 86400.0 + tof + rev_count * period / 86400.0).T  # generate time array
    return pos_set, vel_set, time_set

def get_true_anomaly(p, ecc, r, v) -> np.ndarray:
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
