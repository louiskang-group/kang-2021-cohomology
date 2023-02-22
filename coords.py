from os import path
import sys
import numpy as np

from cohomology import coordinates

"""
`coords.py` reads in data, finds the number of persistent 1-cocycles, and
calculates circular coordinates for them.

Arguments
---------
infn: Path to CSV file containing neural data. File should contain one neuron
      per line with successive values corresponding to successive timepoints.

outroot: Root of output files.

n_cells: Number of cells to subsample. If n_cells <= 0, use all cells.

T_max: Maximum timepoint. If T_max <= 0, use all timepoints.

n_points: Number of timepoints to geometrically subsample.

n_trials: Number of repetitions.

n_threads: Number of simultaneous threads; use when n_trials > 1.


Outputs
-------
outroot_coords.csv: Coordinates u, v for each timepoint over trials. Data
                    columns are t, u1, v1, u2, v2, ....

outroot_gaps.csv: Numbers of persistent cocycles by the maximum gap heuristic
                  over trials.

"""

argc = len(sys.argv)
if argc < 4:
    sys.exit("Usage: script infn outroot n_cells [T_max] [n_points] [n_trials] [n_threads]")

T_max = 0
n_points = 1000
n_trials = 1
n_threads = 1

infn = sys.argv[1]
outroot = sys.argv[2]
n_cells = int(sys.argv[3])
if argc > 4:
    T_max = int(sys.argv[4])
if argc > 5:
    n_points = int(sys.argv[5])
if argc > 6:
    n_trials = int(sys.argv[6])
if argc > 7:
    n_threads = int(sys.argv[7])

coords, gaps = coordinates.get_coordinates(
    infn, n_cells, T_max, n_points, n_trials, n_threads
)
n_coords = coords.shape[1] - 1
np.savetxt(outroot+"_coords.csv", coords, fmt='%4d'+' %6.5f'*n_coords)
np.savetxt(outroot+"_gaps.csv", gaps, fmt='%d')
