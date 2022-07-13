import numpy as np
from numpy import linalg as la


def cart2sph(x, y, z) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert from body centered cartesian coordinates to spherical coordinate (lat, lon, radius).
    Does not account for rotation of body, ie not body fixed

    :param x: x components of vector, x should be the direction of the prime meridian
    :param y: y components of vector
    :param z: z components of vector, y should be the

    :return:
        radius: radius from origin in units of input
        elevation: elevation in deg, 90 deg at north pole, -90 deg at south pole
        azimuth: azimuth in deg, 0 is x-aligned and right handed

    """

    radius = np.sqrt(np.square(x) + np.square(y) + np.square(z))
    elevation = np.arctan2(z, np.sqrt(np.square(x) + np.square(y)))
    azimuth = np.arctan2(y, x)
    return radius, np.rad2deg(elevation), np.rad2deg(azimuth)
