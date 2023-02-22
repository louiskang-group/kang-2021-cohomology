import sys
from os import path
import numpy as np

from joblib import parallel_backend, Parallel, delayed

from dreimac.circularcoords import CircularCoords
from . import persistence


def read(infn, T_max):

    if not path.isfile(infn):
        sys.exit(f"Data file {infn} does not exist")

    # Read in activities as a CSV file. File should contain one neuron per line
    # with successive values corresponding to successive timepoints.
    print("Reading data file ", infn)
    X = np.loadtxt(infn, delimiter=',').T
    print("Data shape:", X.shape)

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
    t = np.arange(T_max)[~zero_rows]

    return t, X


def get_coordinates_one(X, n_cells, T_max, n_points):
    
    # Randomly subsample n_cells neurons.
    if n_cells > 0:
        X = X[:,np.random.choice(X.shape[1], n_cells, replace=False)]

    # Compute circular coordinates.
    c = CircularCoords(X, n_points)
    dgm = c.dgms_[1]
    max_gap, gap = persistence.find_max_gap(dgm)
    print(f"Largest gap {max_gap} after {gap} points")

    # Sort cocycles by persistence lifetime.
    dgm_enum = list(enumerate(dgm))
    sorted_dgm = sorted(dgm_enum, key=lambda pt: pt[1][1]-pt[1][0],
                        reverse=True)
    pt1_idx = sorted_dgm[0][0]
    pt2_idx = sorted_dgm[1][0]

    # Select circular coordinates corresponding to the two most persistent
    # cocycles.
    coord1 = c.get_coordinates(cocycle_idx=[pt1_idx])
    coord2 = c.get_coordinates(cocycle_idx=[pt2_idx])
    coords = np.array([coord1, coord2]).T

    return coords, gap


def get_coordinates(infn, n_cells, T_max=0, n_points=0,
                    n_trials=1, n_threads=1):

    t, X = read(infn, T_max)
    
    # n_points is the number is the number of timepoints in the geometric
    # subsample. If it is out of range, use all timepoints.
    if n_points <= 0:
        n_points = X.shape[0]
    if n_points > X.shape[0]:
        n_points = X.shape[0]

    # Obtain circular coordinates for multiple trials.
    with parallel_backend('loky', n_jobs=n_threads):
        data = Parallel(verbose=0)(
            delayed(get_coordinates_one)(X, n_cells, T_max, n_points)
            for _ in range(n_trials)
        )

    # Collect coordinates u, v over trials. Data columns are
    # t, u1, v1, u2, v2, ...
    coords = []
    for trial in data:
        coords.append(trial[0])
    coords = np.hstack(coords)
    coords = np.hstack((np.reshape(t, (t.size,1)), coords))

    # Collect gaps over trials.
    gaps = []
    for trial in data:
        gaps.append(trial[1])
   
    return coords, gaps
