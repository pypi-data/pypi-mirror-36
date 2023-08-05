"""
Util functions for ANDROMEDA.
"""
from __future__ import division, print_function

__author__ = 'Ralf Farkas'
__all__ = []


import numpy as np


def robust_std(x):
    """
    Calculate and return the *robust* standard deviation of a point set.

    Corresponds to the *standard deviation* of the point set, without taking
    into account the outlier points.

    Parameters
    ----------
    x : array_like
        point set

    Returns
    -------
    std : np.float64
        robust standard deviation of the point set

    Notes
    -----
    based on ``LibAndromeda/robust_stddev.pro`` v1.1 2016/02/16

    """
    median_absolute_deviation = np.median(np.abs(x - np.median(x)))
    return median_absolute_deviation / 0.6745


def create_distance_matrix(n, cx=None, cy=None):
    """
    Create matrix with euclidian distances from a reference point (cx, cy).

    Parameters
    ----------
    n : int
        output image shape is (n, n)
    cx,cy : float
        reference point. Defaults to the center.

    Returns
    -------
    im : ndarray with shape (n, n)


    Notes
    -----
    This is a simplified version of ``DISTC``, as it is used in ANDROMEDA.
    Called in ``andromeda_core``, ``diff_images`` and ``normalize_snr``

    Examples
    --------
    .. code:: python

        # These are equivalent:

        >>> tempo = _dist_circle(img_w, xcen, ycen)
        >>> tempo = _distc(img_w, cx=xcen, cy=ycen)
        >>> tempo = create_distance_matrix(img_w, xcen, ycen)

        IDL> DIST_CIRCLE, tepo, img_w, xcen, ycen
        IDL> ...

    """
    im = np.zeros((n, n))

    if cx is None:
        cx = (n - 1) / 2
    if cy is None:
        cy = (n - 1) / 2

    x = (np.arange(n) - cx)**2
    y = (np.arange(n) - cy)**2

    for i in range(n):
        im[i] = np.sqrt(x + y[i])

    return im


def idl_round(x):
    """
    Round to the *nearest* integer, half-away-from-zero.

    Parameters
    ----------
    x : array-like
        Number or array to be rounded

    Returns
    -------
    r_rounded : array-like
        note that the returned values are floats

    Notes
    -----
    IDL ``ROUND`` rounds to the *nearest* integer (commercial rounding),
    unlike numpy's round/rint, which round to the nearest *even*
    value (half-to-even, financial rounding) as defined in IEEE-754
    standard.

    """
    return np.trunc(x + np.copysign(0.5, x))


def idl_where(array_expression):
    """
    Return a list of indices matching the ``array_expression``.

    Port of IDL's ``WHERE`` function.

    Parameters
    ----------
    array_expression : array_like / expression
        an expression like ``array > 0``

    Returns
    -------
    res : ndarray
        list of 'good' indices


    Notes
    -----
    - The IDL version returns ``[-1]`` when no match was found, this function
      returns ``[]``, which is more "pythonic".

    """
    res = np.array([i for i, e in enumerate(array_expression.flatten()) if e])
    return res
