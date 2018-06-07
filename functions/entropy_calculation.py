import numpy as np
from functions.generate_pdf import generate_pdf

def empirical_entropy(arr, range, dt):
    """
    Calculates entropy for empirical distribution of given values.

    Parameters
    ----------
    arr : vector of floats
        Value of each observation

    range : integer
	The lower and upper range of interval of observation

    dt : float
	Precision of analisis (delta x)

    Returns
    -------
    entropy : float
    """

    density = generate_pdf(arr, range, dt)[0]
    density = density[density != 0]

    ent = - (density * np.log(density)).sum()*dt
    return ent


def theoretical_entropy(var=None, mu=None, distribution='norm', lamb=None):
    """
    Calculates theoretical entropy (gaussian)

    Parameters
    ----------

    var : float
        variance of distribution
	ignored if exponential distribution

    mu : float
	mean of distribution
	ignored if normal distribution

    norm : string
	normal probability density function

    exp : string
	exponential probability density function

    """
    if distribution=='norm':
        return 1/2*np.log(2*np.pi*np.e*var)
    elif distribution == 'exp':
        return np.log(2*np.pi)
    else:
        raise NotImplementedError
