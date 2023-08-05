# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["quadratic"]

import numpy as np


def quadratic(data, uncertainty=None, axis=0, x0=0.0, dx=1.0):
    """Compute the quadratic estimate of the centroid of a line in a data cube

    The use case that we expect is a data cube with spatiotemporal coordinates
    in all but one dimension. The other dimension (given by the ``axis``
    parameter) will generally be wavelength, frequency, or velocity. This
    function estimates the centroid of the *brightest* line along the ``axis''
    dimension, in each spatiotemporal pixel.

    Args:
        data (ndarray): The data cube as an array with at least one dimension.
        uncertainty (Optional[ndarray or float]): The uncertainty on the
            intensities given by ``data``. If this is a scalar, all
            uncertainties are assumed to be the same. If this is an array, it
            must have the same shape as ``data'' and give the uncertainty on
            each intensity. If not provided, the uncertainty on the centroid
            will not be estimated.
        axis (Optional[int]): The axis along which the centroid should be
            estimated. By default this will be the zeroth axis.
        x0 (Optional[float]): The wavelength/frequency/velocity/etc. value for
            the zeroth pixel in the ``axis'' dimension.
        dx (Optional[float]): The pixel scale of the ``axis'' dimension.

    Returns:
        x_max (ndarray): The centroid of the brightest line along the ``axis''
            dimension in each pixel.
        x_max_sig (ndarray or None): The uncertainty on ``x_max''. If
            ``uncertainty'' was not provided, this will be ``None''.
        y_max (ndarray): The predicted value of the intensity at maximum.
        y_max_sig (ndarray or None): The uncertainty on ``y_max''. If
            ``uncertainty'' was not provided, this will be ``None''.

    """
    # Cast the data to a numpy array
    data = np.atleast_1d(data)

    # Find the maximum velocity pixel in each spatial pixel
    idx = np.argmax(data, axis=axis)

    # Deal with edge effects by keeping track of which pixels are right on the
    # edge of the range
    idx_bottom = idx == 0
    idx_top = idx == len(data) - 1
    idx = np.clip(idx, 1, len(data)-2)

    # Extract the maximum and neighboring pixels
    get_slice = lambda delta: tuple(range(s) if i != axis else idx + delta  # NOQA
                                    for i, s in enumerate(data.shape))
    f_minus = data[get_slice(-1)]
    f_max = data[get_slice(0)]
    f_plus = data[get_slice(1)]

    # Work out the polynomial coefficients
    a0 = f_max
    a1 = 0.5 * (f_plus - f_minus)
    a2 = 0.5 * (f_plus + f_minus - 2*f_max)

    # Compute the maximum of the quadratic
    x_max = idx - 0.5 * a1 / a2
    y_max = a0 - 0.25 * a1**2 / a2

    # Set sensible defaults for the edge cases
    if len(data.shape) > 1:
        x_max[idx_bottom] = 0
        x_max[idx_top] = len(data) - 1
        y_max[idx_bottom] = f_minus
        y_max[idx_bottom] = f_plus
    else:
        if idx_bottom:
            x_max = 0
            y_max = f_minus
        elif idx_top:
            x_max = len(data) - 1
            y_max = f_plus

    # If no uncertainty was provided, end now
    if uncertainty is None:
        return x0 + dx * x_max, None, y_max, None

    # Compute the uncertainty
    try:
        uncertainty = float(uncertainty)

    except TypeError:
        # An array of errors was provided
        uncertainty = np.atleast_1d(uncertainty)
        if data.shape != uncertainty.shape:
            raise ValueError("the data and uncertainty must have the same "
                             "shape")

        df_minus = uncertainty[get_slice(-1)]**2
        df_max = uncertainty[get_slice(0)]**2
        df_plus = uncertainty[get_slice(1)]**2

        x_max_var = 0.0625*(a1**2*(df_minus + df_plus) +
                            a1*a2*(df_minus - df_plus) +
                            a2**2*(4.0*df_max + df_minus + df_plus))/a2**4

        y_max_var = 0.015625*(a1**4*(df_minus + df_plus) +
                              2.0*a1**3*a2*(df_minus - df_plus) +
                              4.0*a1**2*a2**2*(df_minus + df_plus) +
                              64.0*a2**4*df_max)/a2**4

        return (x0 + dx * x_max, dx * np.sqrt(x_max_var),
                y_max, np.sqrt(y_max_var))

    else:
        # The uncertainty is a scalar
        x_max_sig = uncertainty*np.sqrt(0.125*a1**2 + 0.375*a2**2)/a2**2
        y_max_sig = uncertainty*np.sqrt(0.03125*a1**4 + 0.125*a1**2*a2**2 +
                                        a2**4)/a2**2
        return x0 + dx * x_max, dx * x_max_sig, y_max, y_max_sig
