## Overview

These Python libraries were created by Louis Kang, Boyan Xu, and Dmitriy Morozov for persistent cohomology analysis of neuroscience data. Our results for simulated recordings of the hippocampal spatial representation system are published in Kang L, Xu B, Morozov D. Evaluating state space discovery by persistent cohomology in the spatial representation system. *Front Comput Neurosci* 15, 616748 (2021). [doi:10.3389/fncom.2021.616748](https://doi.org/10.3389/fncom.2021.616748).

> This GitHub repository contains code used for the manuscript. See our corresponding [Google Drive respository](https://drive.google.com/drive/folders/1TF9FIyp5DXVFqlpFIC_PlJckuJgUu9mK?usp=sharing) for data files used for the manuscript.

## Installing dependencies

These libraries use [Ripser](https://ripser.scikit-tda.org/en/latest/) version 0.6.0 and its dependencies, Matplotlib, and tdqm. They can be installed with Anaconda, for example, with
```
conda install -c conda-forge ripser==0.6.0 matplotlib tqdm
```

## Sample scripts

### `diagram.py`

`diagram.py` reads in CSV data at location `infn` and outputs the persistence diagram at location `outroot.png`. Details about additional arguments are provided in the script.

```
python diagram.py infn outroot n_cells [T_max] [n_points] [max_dim]
```

### `coords.py`

`coords.py` reads in CSV data at location `infn`, finds the number of persistent 1-cocycles, and calculates circular coordinates for them. These coordinates are saved at location `outroot_coords.csv`. The number of persistent 1-cocycles as identified by the largest-gap heuristic is saved at location `outroot_gaps.csv`. Details about additional arguments are provided in the script.

```
python coords.py infn outroot n_cells [T_max] [n_points] [n_trials] [n_threads]
```

### `sweep-cells.py`

`sweep-cells.py` reads in CSV data at location `infn`, calculates the number of persistent 1-cocycles for different numbers of subsampled cells, and outputs the success rates of detecting a desired topology. The success rates are saved at location `outroot_success.csv`. The numbers of subsampled cells as specified in the command line arguments are saved at location `outroot_n.csv`. Details about additional arguments are provided in the script.

```
python infn outroot target [T_max] [n_points] [n_trials] [n_threads] -n n_cells1 [-n n_cells2 ...]
```

## Included code

`dreimac`, used for circular coordinate computation, is taken from [DREiMac](https://github.com/ctralie/DREiMac/).
