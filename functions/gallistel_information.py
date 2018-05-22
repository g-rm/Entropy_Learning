import numpy as np
import pandas as pd
from scipy.stats import ttest_ind


def gallistel_information(us_times, cs_times, dt, range):
	"""
    Calculates the information gain by receiving the CS,
	according to the difference in entropy between the
	distributions.

	Source : https://www.ncbi.nlm.nih.gov/pubmed/23384660

    Parameters
    ----------
    us_times : array
        the latency to US given previous US

    cs_times : array
        latency to US given previous CS

    dt : float
        the timestep to be used to calculate pdfs

    range : tuple (min, max)
        the range of support for the pdfs or
		the lower and upper range of interval of observation
    """

	h_us_us = entropy_calculation(us_times, range, dt)
	h_cs_us = entropy_calculation(cs_times, range, dt)

	return h_us - h_cs


def reyes_cp(timeseries,full_window_size=60):
    """
    Change-point analysis algorithm. Window-walks a timeseries calculating
    the odds of a simple t_test between the window's first and second half.
    Parameters
    ----------
    timeseries : array-like
        Series of values upon which to calculate the Change-point
    full_window_size : int, optional, default: 60
        Size of the total walking window (sum of two halfs)
    Returns
    -------
    odds : Series
        Change-point odds for each timepoint
    """
    rollin_window = pd.Series(timeseries).rolling(full_window_size,center=True)
    return rollin_window.apply(half_ttest_half)

def half_ttest_half(series):
    """
    Divides series in half and returns the t_test odds between each
    """
    halfN = len(series)//2
    t, p = ttest_ind(series[:halfN],series[halfN:])
    return odds(p)

def odds(p):
    return (1-p)/p
