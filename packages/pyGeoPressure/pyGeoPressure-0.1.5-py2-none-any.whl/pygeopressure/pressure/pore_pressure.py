# -*- coding: utf-8 -*-
"""
Routines to calculate pore pressure
"""
from __future__ import division, print_function, absolute_import

__author__ = "yuhao"

import numpy as np


def bowers(v, obp, u, start_idx, a, b, vmax, end_idx=None):
    """
    Compute pressure using Bowers equation.

    Parameters
    ----------
    v : 1-d ndarray
        velocity array whose unit is m/s.
    obp : 1-d ndarray
        Overburden pressure whose unit is Pa.
    v0 : float, optional
        the velocity of unconsolidated regolith whose unit is m/s.
    a : float, optional
        coefficient a
    b : float, optional
        coefficient b

    Notes
    -----
    .. math:: P = S - \\left[\\frac{(V-V_{0})}{a}\\right]^{\\frac{1}{b}}

    [3]_

    .. [3] Bowers, G. L. (1994). Pore pressure estimation from velocity data:
       accounting from overpressure mechanisms besides undercompaction:
       Proceedings of the IADC/SPE drilling conference, Dallas, 1994,
       (IADC/SPE), 1994, pp 515–530. In International Journal of Rock
       Mechanics and Mining Sciences & Geomechanics Abstracts (Vol. 31,
       p. 276). Pergamon.
    """
    sigma_max = ((vmax-1524)/a)**(1/b)
    ves = ((v - 1524) / a)**(1.0 / b)
    ves_fe = sigma_max*(((v-1524)/a)**(1/b)/sigma_max)**u
    ves[start_idx: end_idx] = ves_fe[start_idx: end_idx]
    return obp - ves


def bowers_varu(v, obp, u, start_idx, a, b, vmax, buf=20, end_idx=None, end_buffer=10):
    """
    Bowers Method with buffer zone above unloading zone

    Parameters
    ----------
    v : 1-d ndarray
        velocity array whose unit is m/s.
    obp : 1-d ndarray
        Overburden pressure whose unit is Pa.
    u : float
        coefficient u
    start_idx : int
        index of start of fluid expansion
    a : float, optional
        coefficient a
    b : float, optional
        coefficient b
    vmax : float
    buf : int, optional
        len of buffer interval, buf should be smaller than start_idx
    end_idx : int
        end of fluid expasion
    end_buffer : int
        len of end buffer interval
    """
    u_array = np.ones(v.shape)
    u_array[start_idx: end_idx] = u
    # start buffer
    u_buffer = np.linspace(1, u, buf)
    u_array[start_idx-buf+1: start_idx + 1] = u_buffer
    # end buffer
    if end_idx is not None:
        u_array[end_idx: end_idx + end_buffer] = np.linspace(u, 1, end_buffer)
    sigma_max = ((vmax-1524)/a)**(1/b)
    ves = sigma_max*(((v-1524)/a)**(1/b)/sigma_max)**u_array
    return obp - ves


def virgin_curve(sigma, a, b):
    "Virgin curve in Bowers' method."
    v0 = 1524
    return v0 + a * sigma**b


def invert_virgin(v, a, b):
    "invert of virgin curve."
    v0 = 1524
    return ((v-v0)/a)**(1/b)


def unloading_curve(sigma, a, b, u, v_max):
    "Unloading curve in Bowers's method."
    sigma_max = ((v_max-1524)/a)**(1/b)
    independent = sigma_max*(sigma/sigma_max)**(1/u)
    return virgin_curve(independent, a, b)


def invert_unloading(v, a, b, u, v_max):
    "invert of Unloading curve in Bowers's method."
    sigma_max = invert_virgin(v_max, a, b)
    sigma_vc = invert_virgin(v, a, b)
    return sigma_max * (sigma_vc/sigma_max)**u


def eaton(v, vn, hydrostatic, lithostatic, n=3):
    """
    Compute pore pressure using Eaton equation.

    Parameters
    ----------
    v : 1-d ndarray
        velocity array whose unit is m/s.
    vn : 1-d ndarray
        normal velocity array whose unit is m/s.
    hydrostatic : 1-d ndarray
        hydrostatic pressure in mPa
    lithostatic : 1-d ndarray
        Overburden pressure whose unit is mPa.
    v0 : float, optional
        the velocity of unconsolidated regolith whose unit is ft/s.
    n : float, optional
        eaton exponent

    Notes
    -----
    .. math:: P = S - {\\sigma}_{n}\\left(\\frac{V}{V_{n}}\\right)^{n}

    [4]_

    .. [4] Eaton, B. A., & others. (1975). The equation for geopressure
       prediction from well logs. In Fall Meeting of the Society of Petroleum
       Engineers of AIME. Society of Petroleum Engineers.
    """
    ves = (lithostatic - hydrostatic) * (v / vn)**n
    pressure = lithostatic - ves
    return pressure


def invert_multivariate_virgin(vel, phi, vsh, a_0, a_1, a_2, a_3, B):
    """
    Calculate effective stress using multivariate virgin curve

    Parameters
    ----------
    vel : 1-d ndarray
        velocity array whose unit is m/s.
    phi : 1-d ndarray
        porosity array
    vsh : 1-d ndarray
        shale volume
    a_0, a_1, a_2, a_3 : scalar
        coefficients

    Returns
    -------
    sigma: 1-d ndarray
    """
    return ((vel - a_0 + a_1 * phi + a_2 * vsh) / a_3)**(1 / B)


def multivariate_virgin(sigma, phi, vsh, a_0, a_1, a_2, a_3, B):
    """
    Calculate velocity using multivariate virgin curve

    Parameters
    ----------
    sigma : 1-d ndarray
        effective pressure
    phi : 1-d ndarray
        effective porosity
    vsh : 1-d ndarray
        shale volume
    a_0, a_1, a_2, a_3 : float
        coefficients of equation
    B : float
        effective pressure exponential

    Returns
    -------
    out : 1-d ndarray
        velocity array

    Notes
    -----
    .. math:: V = a_0 + a_1\\phi + a_2{V}_{sh} + a_3 {\\sigma}^{B}

    [5]_

    .. [5] Sayers, C., Smit, T., van Eden, C., Wervelman, R., Bachmann, B.,
       Fitts, T., et al. (2003). Use of reflection tomography to predict
       pore pressure in overpressured reservoir sands. In submitted for
       presentation at the SEG 2003 annual meeting.
    """
    return a_0 - a_1 * phi - a_2 * vsh + a_3 * sigma**B


def multivariate_unloading(sigma, phi, vsh, a_0, a_1, a_2, a_3, B, U, vmax):
    """
    Calculate velocity using multivariate unloading curve
    """
    sigma_max = invert_multivariate_virgin(vmax, phi, vsh, a_0, a_1, a_2, a_3, B)
    sigma_vc = sigma_max*(sigma/sigma_max)**(1/U)
    return multivariate_virgin(sigma_vc, phi, vsh, a_0, a_1, a_2, a_3, B)


def invert_multivariate_unloading(vel, phi, vsh, a_0, a_1, a_2, a_3, B, U, vmax):
    """
    Calculate effective stress using multivariate unloading curve
    """
    sigma_max = invert_multivariate_virgin(vmax, phi, vsh, a_0, a_1, a_2, a_3, B)
    sigma_vc = invert_multivariate_virgin(vel, phi, vsh, a_0, a_1, a_2, a_3, B)
    return sigma_max * (sigma_vc/sigma_max)**U


def effective_stress_multivariate(vel, phi, vsh, a_0, a_1, a_2, a_3,
                                  B, U, vmax, start_idx, end_idx=None):
    ves = invert_multivariate_virgin(vel, phi, vsh, a_0, a_1, a_2, a_3, B)
    unloading = invert_multivariate_unloading(vel, phi, vsh, a_0, a_1, a_2, a_3, B, U, vmax)
    ves[start_idx: end_idx] = unloading[start_idx: end_idx]
    return ves


def pressure_multivariate(obp, vel, phi, vsh, a_0, a_1, a_2, a_3,
                          B, U, vmax, start_idx, end_idx=None):
    """
    Pressure Prediction using multivariate model
    """
    ves = effective_stress_multivariate(
        vel, phi, vsh, a_0, a_1, a_2, a_3, B, U, vmax, start_idx, end_idx)
    return obp - ves


def pressure_multivariate_varu(obp, vel, phi, vsh, a_0, a_1, a_2, a_3,
                               B, U, vmax, start_idx, buf=20,
                               end_idx=None, end_buffer=10):
    """
    Pressure Prediction using multivariate model
    """
    ves = effective_stress_multivariate_varu(
        vel, phi, vsh, a_0, a_1, a_2, a_3,
        B, U, vmax, start_idx, buf, end_idx, end_buffer)
    return obp - ves


def effective_stress_multivariate_varu(vel, phi, vsh, a_0, a_1, a_2, a_3,
                                       B, U, vmax, start_idx, buf=20,
                                       end_idx=None, end_buffer=10):
    u_array = np.ones(vel.shape)
    u_array[start_idx: end_idx] = U
    # start buffer
    u_buffer = np.linspace(1, U, buf)
    u_array[start_idx-buf+1: start_idx + 1] = u_buffer
    # end buffer
    if end_idx is not None:
        u_array[end_idx: end_idx + end_buffer] = np.linspace(U, 1, end_buffer)
    ves = invert_multivariate_unloading(vel, phi, vsh, a_0, a_1, a_2, a_3,
                                        B, u_array, vmax)
    return ves
