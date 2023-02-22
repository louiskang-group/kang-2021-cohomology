import sys
from os import path
import numpy as np
from ripser import ripser

def read(infn, n_cells, T_max):

    if not path.isfile(infn):
        sys.exit(f"Data file {infn} does not exist")

    # Read in activities as a CSV file. File should contain one neuron per line
    # with successive values corresponding to successive timepoints.
    print("Reading data file ", infn)
    X = np.loadtxt(infn, delimiter=',').T
    print("Data shape:", X.shape)

    # Randomly subsample n_cells neurons.
    if n_cells > 0:
        X = X[:,np.random.choice(X.shape[1], n_cells, replace = False)]

    # T_max sets the number of timepoints to be used. If not set, use all
    # timepoints.
    if T_max > 0:
        X = X[:T_max]
    else:
        T_max = X.shape[0]

    # Normalize each neuron.
    X /= X.mean(axis=0)

    # Remove timepoints at which all neurons have activity less than epsilon.
    epsilon = 1e-3
    zero_rows = np.all(X < epsilon, axis=1)
    X = X[~zero_rows, :]
    print("Subsampled shape:", X.shape)
    
    return X


def compute_diagrams(X, max_dim=2, coeff=3, n_points=500):

    # max_dim is the maximum cocycle dimension, coeff is the prime number p of
    # Z/pZ used to compute cohomology, n_points is the number of timepoints in
    # the geometric subsample.
    return ripser(X, maxdim=max_dim, coeff=coeff, n_perm=n_points)['dgms']


def find_max_gap(dgm):

    # Sort cocycles by persistence lifetime.
    if len(dgm) == 0:
        return (0, -1)
    points_persistence = [p[1] - p[0] for p in dgm]
    points_persistence.sort(reverse=True)
    if len(points_persistence) == 1:
        return (points_persistence[0], 0)

    gaps = [points_persistence[i] - points_persistence[i+1]
            for i in range(len(points_persistence) - 1)]
    max_gap_info = max((g, i+1) for i, g in enumerate(gaps))

    # max_gap_info[0] contains the length of the gap and max_gap_info[1] is the
    # number of persistent cocycles.
    return max_gap_info
