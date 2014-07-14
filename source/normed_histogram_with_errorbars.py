import matplotlib.pyplot as plt
import numpy as np

"""
here i show you a possibility how to plot normed histograms
with errorbars. Very helpful if you want to compare data sets
of different sizes.
"""

# get gaussian random numbers for the histograms

data1 = np.random.normal(2,1, 1000)
data2 = np.random.normal(4,1, 5000)


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title(r"Normed Histograms with Errorbars")

# variables for number of bins and the limits

num_bins = 30
limits = (-2, 8)

for data, color, label in zip([data1, data2], ['r', 'b'], ["data1", "data2"]):
    # calculate number of events in bin_limits (aka discard under- and overflow)
    mask = np.logical_and(data>=limits[0], data<=limits[1])
    num_events = len(data[mask])
    # calculate normalisation so that area under histo is 1
    normalisation = num_bins/(num_events*(limits[1]-limits[0]))

    # let numpy calculate the histogram entries
    histo, bin_edges = np.histogram(data, num_bins, limits)

    # calculate the middles of eachs bin, as this is where we want to plot the
    # errorbars
    bin_middles = 0.5*(bin_edges[1:] + bin_edges[:-1])

    # we take the poisson error as estimated standard deviation, taking the
    # normalisation into account
    y_err = np.sqrt(histo)*normalisation

    ax.errorbar(bin_middles, histo*normalisation, fmt=',', color=color, yerr=y_err)
    ax.hist(data, num_bins, limits, normed=True,
            histtype='step', color=color, label=label)

ax.grid()
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"normed frequency")
ax.legend(loc="best")
fig.tight_layout()
fig.savefig("../images/normed_histogram_with_errorbars.png", dpi=300)
