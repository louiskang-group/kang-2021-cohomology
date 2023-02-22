from os import path
import sys
import numpy as np
import matplotlib.pyplot as plt

from cohomology import persistence
from ripser import ripser
from persim import plot_diagrams

"""
`diagram.py` reads in data and outputs a persistence diagram.

Arguments
---------
infn: Path to CSV file containing neural data. File should contain one neuron
      per line with successive values corresponding to successive timepoints.

outroot: Root of output files.

n_cells: Number of cells to subsample. If n_cells <= 0, use all cells.

T_max: Maximum timepoint. If T_max <= 0, use all timepoints.

n_points: Number of timepoints to geometrically subsample.

max_dim: Maximum cohomology dimension to compute.


Outputs
-------
outroot.png: Persistence diagram.

"""

n_cells = 0
T_max = 0
n_points = 1000
max_dim = 1

argc = len(sys.argv)
if argc > 7 or argc < 4:
    sys.exit("Usage: script infn outroot n_cells [T_max] [n_points] [max_dim]")
    
infn = sys.argv[1]
outroot = sys.argv[2]
n_cells = int(sys.argv[3])
if argc > 4:
    T_max = int(sys.argv[4])
if argc > 5:
    n_points = int(sys.argv[5])
if argc > 6:
    max_dim = int(sys.argv[6])

X = persistence.read(infn, n_cells, T_max)

dgm = persistence.compute_diagrams(X, max_dim=max_dim, n_points=n_points)
_, gap = persistence.find_max_gap(dgm[1])

plot_diagrams(dgm, show=False)
plt.suptitle(f"Max gap: {gap}")
plt.savefig(outroot)
