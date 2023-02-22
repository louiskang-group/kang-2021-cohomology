from os import path
import getopt
import sys
import numpy as np

from cohomology import success

"""
`sweep-cells.py` reads in data, calculates the number of persistent 1-cocycles
for different numbers of subsampled cells, and outputs the success rates of
detecting an expected topology.

Arguments
---------
infn: Path to CSV file containing neural data. File should contain one neuron
      per line with successive values corresponding to successive timepoints.

outroot: Root of output files.

target: Expected number of 1-cocycles.

T_max: Maximum timepoint. If T_max <= 0, use all timepoints.

n_points: Number of timepoints to geometrically subsample.

n_trials: Number of repetitions for calculation of success rate.

n_threads: Number of simultaneous threads.

-n n_cells: Number of cells to subsample. If n_cells <= 0, use all cells.
            Multiple values can be given, each preceded by the flag '-n'.

Outputs
-------
outroot_success.csv: Success rates over numbers of subsampled cells.

outroot_n.csv: Numbers of subsampled cells as specified in the command
               line arguments.

"""

print(sys.argv[1])
optlist, args = getopt.gnu_getopt(sys.argv[1:], 'n:')

valid_args = len(args) >= 3 and len(args) <= 7
valid_optlist = len(optlist) >= 1
if not valid_args or not valid_optlist:
    sys.exit("Usage: script infn outroot target [T_max] [n_points] [n_trials] [n_threads] -n n_cells1 [-n n_cells2 ...]")


T_max = 0
n_points = 1000
n_trials = 100
n_threads = 20

infn = args[0]
outroot = args[1]
target = int(args[2])
if len(args) > 3:
    T_max = int(args[3])
if len(args) > 4:
    n_points = int(args[4])
if len(args) > 5:
    n_trials = int(args[5])
if len(args) > 6:
    n_threads = int(args[6])

arr_cells = []
for opt, arg in optlist:
    if opt in ('-n'):
        arr_cells.append(int(arg))
print("Cell numbers:", arr_cells)
np.savetxt(outroot+"_n.csv", arr_cells, fmt='%d')

results = success.sweep_cells(
        infn, arr_cells, target, T_max, n_points, n_trials, n_threads
        )
print("Success rates:", results)
np.savetxt(outroot+"_success.csv", results, fmt='%4.3f')
