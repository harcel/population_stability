# Unstable Populations
#
# Blablabla
#
# Date, authors, contact etc.
#
################################################

import numpy as np
import pandas as pd

################################################


def upi(pop1, pop2, weight=True, bin_data=False):
    """
    Docstring focusing on UPI only
    """

    return _indicator(pop1, pop2, weight=weight, plus1=True, bin_data=bin_data)


################################################


def psi(pop1, pop2, bin_data=True):
    """
    Docstring focusing on psi only
    """

    return _indicator(pop1, pop2, weight=False, plus1=False, bin_data=bin_data)


################################################


def _indicator(pop1, pop2, weight=True, plus1=True, bin_data=False):
    """
    Versatile code to calculate any measure we
    enable: psi, upi, weihgted or not, blabla

    """

    a, b = _prepare_data(pop1, pop2, bin_data=bin_data)

    atot = a.sum()
    btot = b.sum()

    # Make fractions
    fa = a / atot
    fb = b / btot

    if plus1:
        fal = (a + 1) / atot
        fbl = (b + 1) / btot
    else:
        fal = fa
        fbl = fb

    if weight:
        w = (fa + fb) * len(a) / 2
    else:
        w = 1.0

    return np.sum((fa - fb) * np.log(fal / fbl) * w)


################################################


def _prepare_data(pop1, pop2, bin_data=False):
    """
    Check the contents of pop1 and pop2 and decide
    what to do. Return two np.arrays with the binned
    data that _indicator() is going to use.

    We want to allow:
    np.array, dict, list, pd.DataFrame, pd.Series

    If dict/df/Series, check if all indices/keys exist
    in both populations, otherwise add empty category


    If bin_data is True, do a binning. If False, check consistency

    """

    # Check on file types, consistency of pop1/pop2 etc
    # Convert to numpy array

    if bin_data:
        a, b = _bin_data(pop1, pop2)

    # For now:
    a = pop1
    b = pop2

    return a, b


################################################


def _bin_data(aa, bb):
    """
    If unbinned data has come in, do something smart
    with it here.
    """

    # Use numpy for binning.
    # Perhaps make method dependent on data properties

    # Placeholder
    bin_a = aa
    bin_b = bb

    return bin_a, bin_b


# For now:

if __name__ == "__main__":
    flat = np.array([10, 10, 10, 10])
    empty = np.array([1, 1, 1, 1])
    noise = np.array([9, 11, 9, 11])

    print(upi(flat, empty))
    print(upi(flat, noise))
