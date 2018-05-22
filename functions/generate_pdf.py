import numpy as np
import pandas as pd

def generate_pdf(data, range, step):

    """
    Generates a probability density function
    given samples and a step size.
    Too big step sizes will make the pdf imprecise,
    but too small sizes will have much noise.

    Parameters
    ----------
    data : array
		Value of each observation

    range : tuple (min, max)
        the range of support for the pdf

    step : float
		Precision of analisis (delta x)

    Returns
    -------
    density : array
        Value of the probability density along intervals

    bin_edges : arrays
        The infimum and supremum values of intervals
    """

    nbins = int((range[1] - range[0])/step) + 1
    new_range = (range[0], range[0]+nbins*step)
    density, bin_edges = np.histogram(data, nbins, new_range, density=True)

    return density, bin_edges

def calculate_cs_us(df_orig):
    df = df_orig.copy()
    df['distancia_do_ultimo_US'] = df[df.recompensado]['final_da_trial'].diff()
    US = df['distancia_do_ultimo_US'].dropna().values
    CS = df[df.recompensado]['t'].values
    return (CS, US)
