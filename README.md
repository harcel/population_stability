# Population stability
A package to calculate the **Unstable Population Indicator** (see below for definition) or the **Population Stability Index**, see e.g. [this paper](https://scholarworks.wmich.edu/cgi/viewcontent.cgi?article=4249&context=dissertations) or [this paper](https://mwburke.github.io/data%20science/2018/04/29/population-stability-index.html), with a (slightly flawed, as explained in the accompanying paper) Python implementation [here](https://github.com/mwburke/population-stability-index).

## Installation instructions
Clone the repository, then
```bash
pip install -e .
```

## The Unstable Population Indicator
The UPI is explained in much more detail in an accompanying paper, but the main idea is that it is an indicator that can be used when comparing two populations, to see if they are similar. Dissimilarity can be interpreted as data drift, for example, and may indicate a difference between a population some algorithm was trained on and a new population, for which the algorithm will be used.

The UPI works for continuous, ordinal and nominal data (continuous data will be binned) and is formally defined as (LaTeX robably not rendered on Github, see your local version or the accompanying paper):

$$
\textrm{UPI} = \,
	\sum_{\textrm{bins, }i} w_i \cdot(f_{1,i} - f_{0,i}) \cdot \log \Big( \frac{f_{1,i} + 1/n_\textrm{tot} }{f_{0,i} + 1/n_\textrm{tot} } \Big)  \\
\, \\
w_i = \begin{cases} 
\frac{N_\textrm{bins} }{2} (f_{1,i} + f_{0,i} )& \textrm{\small bins weighted by fraction}\\
1 & \textrm{\small unweighted}
\end{cases}
$$
where $f_{0,i}$ and $f_{1,i}$ are the fraction of the entities in bin or category $i$ in the original and new population, respectively,  $n_\textrm{tot}$ is the number of entities in the original and new populations together and $N_\textrm{bins}$ is the number of bins or categories (over which the sum is taken). The weighting ($w_i$) can be chosen to be uniform, or based on the fraction of entities from both population in the bin/category (giving well populated bins/categories more weight in the indicator).


## Usage
The UPI and PSI can be calculated for two populations as follows
```python
from unstable_populations import upi, psi
UPI = upi(pop1, pop2)
PSI = psi(pop1, pop2)
```

There are optional keyword parameters that can let you do binning of the populations, or chose the weighting. The data can be provided in lists, numpy arrays, dictionaries, pandas Series or pandas DataFrames, see the documentation for more details.

## Misc
Developed and written by Marcel Haas, Joris Huese and Lisette Sibbald at the University of Amsterdam.
Hosted at https://github.com/harcel/population_stability/
