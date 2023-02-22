from os import path
import sys
import numpy as np

from joblib import parallel_backend, Parallel, delayed
from tqdm import tqdm

from . import persistence


def read(infn):

    if not path.isfile(infn):
        sys.exit(f"Data file {infn} does not exist")

    # Read in activities as a CSV file. File should contain one neuron per line
    # with successive values corresponding to successive timepoints.
    print("Reading data file ", infn)
    X = np.loadtxt(infn, delimiter=',').T
    print("Data shape:", X.shape)

    # Normalize each neuron.
    X /= X.mean(axis=0)

    return X


def read_two(infn1, infn2):

    if not path.isfile(infn1):
        sys.exit(f"Data file {infn1} does not exist")
    if not path.isfile(infn2):
        sys.exit(f"Data file {infn2} does not exist")

    # Read in two sets of activities as CSV files. This allows construction of
    # merged datasets.
    print("Reading data file ", infn1)
    X1 = np.loadtxt(infn1, delimiter=',').T
    print("Reading data file ", infn2)
    X2 = np.loadtxt(infn2, delimiter=',').T
    if X1.shape[0] != X2.shape[0]:
        sys.exit("Two data files have unequal number of timepoints")
    print("Data shapes:", X1.shape, X2.shape)

    # Normalize each neuron.
    X1 /= X1.mean(axis = 0)
    X2 /= X2.mean(axis = 0)

    return X1, X2


def test_success_one(X1, X2, n_cells1, n_cells2, target, n_points):

    # Randomly subsample n_cells1 neurons from X1. If n_cells2 > 0, also
    # subsample n_cells2 neurons from X2 and combine the two datasets.
    X = X1[:,np.random.choice(X1.shape[1], n_cells1, replace=False)]
    if n_cells2 > 0:
        X = np.hstack(
            (X, X2[:,np.random.choice(X2.shape[1], n_cells2, replace=False)])
        )

    # Remove timepoints at which all neurons have activity less than epsilon.
    epsilon = 1e-3
    zero_rows = np.all(X < epsilon, axis=1)
    X = X[~zero_rows, :]

    # n_points is the number is the number of timepoints in the geometric
    # subsample. If it is out of range, use all timepoints.
    if n_points <= 0:
        n_points = X.shape[0]
    if n_points > X.shape[0]:
        n_points = X.shape[0]

    dgms = persistence.compute_diagrams(X, max_dim=1, n_points=n_points)
    max_gap, gap = persistence.find_max_gap(dgms[1])

    # Does the number of persistent cocycles match the target number?
    return gap == target


def test_success(X1, X2, n_cells1, n_cells2, target,
                 n_points, n_trials, n_threads):

    # Generate multiple subsampled datasets and test their successes.
    with parallel_backend('loky', n_jobs=n_threads):
        trial_results = Parallel(verbose=0)(
            delayed(test_success_one)(X1, X2, n_cells1, n_cells2, target,
                                      n_points)
            for _ in range(n_trials)
        )

    # Return the success rate.
    return sum(trial_results) / n_trials


def sweep_cells(infn, arr_cells, target,
                T_max=0, n_points=1000, n_trials=100, n_threads=20):

    X = read(infn)
    
    # T_max sets the number of timepoints to be used. If not set, use all
    # timepoints.
    if T_max > 0:
        X = X[:T_max]

    # Obtain success rates over different numbers of neurons.
    results = np.zeros(len(arr_cells))
    for i in tqdm(range(len(arr_cells))):    
        results[i] = test_success(
            X, None, arr_cells[i], 0, target, n_points, n_trials, n_threads
        )

    return results


def sweep_cells_two(infn1, infn2, arr_cells1, arr_cells2, target,
                    T_max=0, n_points=1000, n_trials=100, n_threads=20):

    X1, X2 = read_two(infn1, infn2)
    
    # T_max sets the number of timepoints to be used for both datasets. If not
    # set, use all timepoints.
    if T_max > 0:
        X1 = X1[:T_max]
        X2 = X2[:T_max]

    # Obtain success rates over different numbers of neurons.
    results = np.zeros((len(arr_cells1), len(arr_cells2)))
    for i in tqdm(range(len(arr_cells1))):    
        for j in tqdm(range(len(arr_cells2)), leave=False):    
            results[i,j] = test_success(
                X1, X2, arr_cells1[i], arr_cells2[j], target,
                n_points, n_trials, n_threads
            )

    return results


def sweep_times(infn, n_cells, target, arr_T,
                n_points=1000, n_trials=100, n_threads=20):

    X = read(infn)

    # Obtain success rates over maximum timepoints.
    results = np.zeros(len(arr_T))
    for i in tqdm(range(len(arr_T))):    
        results[i] = test_success(
            X[:arr_T[i]], None, n_cells, 0, target,
            n_points, n_trials, n_threads
        )

    return results
