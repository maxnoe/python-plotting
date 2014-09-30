import matplotlib.pyplot as plt
import numpy as np

if plt.rcParams["text.usetex"] is False:
    plt.rcParams["text.usetex"] = True
    print("\nWARNING: text.usetex is now set to True\n")

if plt.rcParams["text.latex.unicode"] is False:
    plt.rcParams["text.latex.unicode"] = True
    print("\nWARNING: text.latex.unicode is now set to True\n")

if "siunitx" not in plt.rcParams["text.latex.preamble"]:
    plt.rcParams["text.latex.preamble"].append(r"\usepackage{siunitx}")



def siunitx_ticklabels(ax=None, locale="DE", xaxis=True, yaxis=True):
    """
    This function uses siunitx to create the ticklabels
    Main reason is for adjusting the decimal marker properly.
    The function takes 4 arguments:

        ax=None     the matplotlib axes to operate on
                    if set to None (Standard) this will be the current axes
        locale="DE" The locale parameter for siunitx, one of
                    "UK", "US", "DE", "FR" oder "ZA"
        xaxis=True  Boolean, if True the labels for the xaxis are set
        yaxis=True  Boolean, if True the labels for the yaxis are set

    """

    if ax is None:
        ax = plt.gca()

    if xaxis is True:
        xticks = ax.get_xticks()
        xlabels = [r"$\num[locale={}]{{{}}}$".format(locale, tick) for tick in xticks]
        ax.set_xticklabels(xlabels)

    if yaxis is True:
        yticks = ax.get_yticks()
        ylabels = [r"$\num[locale={}]{{{}}}$".format(locale, tick) for tick in yticks]
        ax.set_yticklabels(ylabels)

if __name__ == "__main__":
    fig, ax = plt.subplots(1,1)
    x = np.linspace(-2, 2, 1000)
    ax.plot(x, 0.5*x**3, 'r-')

    siunitx_ticklabels(ax)

    ax.set_title(r"ticklabels with \texttt{siunitx} to get \num[locale=DE]{2.1}")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    fig.tight_layout()
    fig.savefig("../images/siunitx_ticks.png", dpi=200)
