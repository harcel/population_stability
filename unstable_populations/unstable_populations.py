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


def upi(pop1, pop2, weight=True, bin_data=False, verbose=False):
    """
    Docstring focusing on UPI only
    """

    return _indicator(
        pop1, pop2, weight=weight, plus1=True, bin_data=bin_data, verbose=verbose
    )


################################################


def psi(pop1, pop2, bin_data=False, verbose=False):
    """
    Docstring focusing on psi only
    """

    return _indicator(
        pop1, pop2, weight=False, plus1=False, bin_data=bin_data, verbose=verbose
    )


################################################


def _indicator(pop1, pop2, weight=True, plus1=True, bin_data=False, verbose=False):
    """
    Versatile code to calculate any measure we
    enable: psi, upi, weihgted or not, etc.

    For definitions, see docstring of upi/psi.
    """

    a, b = _prepare_data(pop1, pop2, bin_data=bin_data, verbose=verbose)

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


def _prepare_data(pop1, pop2, bin_data=False, verbose=False):
    """
    Check the contents of pop1 and pop2 and decide
    what to do. Return two np.arrays with the binned
    data that _indicator() is going to use.

    We want to allow:
    np.array, dict, list, pd.DataFrame, pd.Series,
    But same for both!

    If dict/df/Series, check if all indices/keys exist
    in both populations, otherwise add empty category


    If bin_data is not False, _bin_data() is used.
    If False, check consistency.

    """

    # Check on file types, consistency of pop1/pop2 etc
    # Convert to numpy array

    # Type consistency check
    tp1 = type(pop1)
    if not (type(pop2) is tp1):
        raise TypeError("Both populations must be supplied in same type!")

    if bin_data:
        if tp1 in (np.ndarray, list):
            a, b = _bin_data(pop1, pop2, bins=bin_data, verbose=verbose)
        else:
            raise TypeError("Data to be binned should be an np.ndarray or list!")
    else:
        if len(pop1) != len(pop2):
            raise ValueError(
                "Populations need to be of same size, unless _bin_data != False"
            )

        # Adapt data type when necessary
        if tp1 is np.ndarray:
            a = pop1
            b = pop2

        elif tp1 is list:
            a = np.array(pop1)
            b = np.array(pop2)
            if verbose:
                print("Constructing arrays from population lists.")
                print(
                    "Assuming that the order of the elements in the lists is the same."
                )

        elif tp1 is dict:
            categories1 = set(pop1.keys())
            categories2 = set(pop2.keys())

            categories = list(categories1.union(categories2))
            a = np.array(
                [pop1[k] if k in pop1 else 0.0 for k in categories], np.float64
            )
            b = np.array(
                [pop2[k] if k in pop2 else 0.0 for k in categories], np.float64
            )
            if verbose:
                print(
                    f"Found the following categories in the populations: {categories}"
                )
                print(f"Values in population 1: {a}")
                print(f"Values in population 2: {b}")

        elif tp1 is pd.Series:
            # Merge the two populations in a DF and extract the two arrays
            df = pd.DataFrame(pop1, columns=["pop1"])
            df = df.merge(
                pd.DataFrame(pop2, columns=["pop2"]),
                how="outer",
                left_index=True,
                right_index=True,
            ).fillna(0)
            a = df.pop1.values
            b = df.pop2.values
            if verbose:
                print("The two populations in one DataFrame:\n", df)

        elif tp1 is pd.DataFrame:
            if pop1.shape[1] > 1:
                raise ValueError(
                    "Unclear which column of the DataFrame of pop1 to use!"
                )
            df = pop1.rename(columns={pop1.columns[0]: "pop1"})
            df = df.merge(
                pop2.rename(columns={pop2.columns[0]: "pop2"}),
                how="outer",
                left_index=True,
                right_index=True,
            ).fillna(0)
            a = df.pop1.values
            b = df.pop2.values
            if verbose:
                print("The two populations in one DataFrame:\n", df)

    return a, b


################################################


def _bin_data(aa, bb, bins=10, verbose=False):
    """
    If unbinned data has come in, do something smart
    with it here.

    Uses numpy.histogram for binning.

    bins can be:
    - int: number of bins
    - list or array: bin boundaries, from min to max, half open on right,
        like numpy, when bins=[1, 2, 3, 4], the bin edges will be [1,2), [2,3)
        and [3,4]. Note that min and max of data can fall out of this!
    - str: name of binning method recognized by np.histogram_bin_edges
    - True: binning will be determined by np.hist

    The bins will be the same for both populations.
    """

    data = np.array(list(aa) + list(bb))

    # First determine bin edges on all data if necessary, then bin.
    _, bin_edges = np.histogram(data, bins)

    bin_a, _ = np.histogram(aa, bin_edges)
    bin_b, _ = np.histogram(bb, bin_edges)

    if verbose:
        print(f"Bin edges that will be used: {np.round(bin_edges, decimals=2)}")
        print("Bin values for population1:", bin_a)
        print("Bin values for population2:", bin_b)

    return bin_a, bin_b


# For now:

if __name__ == "__main__":
    flat = np.array([10, 10, 10, 10])
    empty = np.array([1, 1, 1, 1])
    noise = np.array([9, 11, 9, 11])
    noise_big = np.array([99, 101, 99, 101])

    print(upi(flat, empty))
    print(upi(flat, noise))
    print(upi(flat, noise_big))
    print(psi(flat, empty))
    print(psi(flat, noise))
    print(psi(flat, noise_big))

    # Lists as entry
    print("------")
    flat = [10, 10, 10, 10]
    empty = [1, 1, 1, 1]
    noise = [9, 11, 9, 11]
    noise_big = [99, 101, 99, 101]

    print(upi(flat, empty))
    print(upi(flat, noise))
    print(upi(flat, noise_big))
    print(psi(flat, empty))
    print(psi(flat, noise))
    print(psi(flat, noise_big))

    # Dict as entry
    print("------")
    flat = {"0": 10, "1": 10, "2": 10, "3": 10}
    noise = {"0": 11, "1": 9, "2": 11, "3": 9}
    diff = {"0": 10, "1": 10, "2": 10, "4": 10}

    print(upi(flat, noise))
    print(upi(flat, diff))
    print(psi(flat, noise))
    # print(psi(flat, diff))  # Should give inf, and issues along the way!

    # Series as entry
    flat = pd.Series(flat)
    noise = pd.Series(noise)
    diff = pd.Series(diff)

    print(upi(flat, noise))
    print(upi(flat, diff))
    print(psi(flat, noise))
    # print(psi(flat, diff))  # Should give inf, and issues along the way!

    # DataFrames as entry
    print("------")
    flat = pd.DataFrame(flat)
    noise = pd.DataFrame(noise)
    diff = pd.DataFrame(diff)

    print(upi(flat, noise))
    print(upi(flat, diff))
    print(psi(flat, noise))

    # Arrays to be binned as entry
    print("--------")
    flat_rd = np.random.uniform(0, 10, size=100)
    large_flat_rd = np.random.uniform(0, 10, size=1000)
    gauss_rd = np.random.normal(5, 1, size=100)

    print(upi(flat_rd, large_flat_rd, bin_data=5, verbose=True))

    # For tests later: upi(flat, noise) > upi(flat, noise_big) ; upi(flat, empty) = 0 ; also psi
    # upi(lat, noise-big) < psi(flat, noise_big)
    # Check for same value, independent of data type of pops

    # Check for things that should throw an error:
    # lists of unequal length, array of unequal length, DataFrame with more than one column
