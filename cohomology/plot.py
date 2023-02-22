import numpy as np
from matplotlib import pyplot as plt


# Plot success rates over a 2D parameter sweep.
def plot_success(data, outfn='', xticks='', yticks='', xlabel='', ylabel=''):

    plt.matshow(np.flipud(data))
    plt.colorbar()

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.gca().xaxis.tick_bottom()
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.yticks(np.arange(data.shape[0]), yticks[::-1], fontsize=6)
    plt.xticks(np.arange(data.shape[1]), xticks, fontsize=6)

    if outfn:
        plt.savefig(outfn, dpi=600)
    else:
        plt.show()
