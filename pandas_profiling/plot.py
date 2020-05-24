"""Plot functions for the profiling report."""

from typing import Union, Tuple
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from pkg_resources import resource_filename

from pandas_profiling.config import config
from pandas_profiling.base import Variable
register_matplotlib_converters()
matplotlib.style.use(resource_filename(__name__, "pandas_profiling.mplstyle"))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def _plot_histogram(
    series: pd.Series,
    series_description: dict,
    bins: Union[int, np.ndarray],
    figsize: tuple = (6, 4),
):
    """Plot an histogram from the data and return the AxesSubplot object.

    Args:
        series: The data to plot
        figsize: The size of the figure (width, height) in inches, default (6,4)
        bins: number of bins (int for equal size, ndarray for variable size)

    Returns:
        The histogram plot.


    """
    if (series_description["type"] == Variable.TYPE_CAT):
        if bins != 20:
            if series.index[0] == '0':
                series = series[1:11]
            elif len(series.index)>10:
                series = series[:10]
            plot = series.plot(
                kind="barh",
                figsize=figsize,
                color="#337ab7"
            )
        else:
            plot = series.plot(
                kind="hist",
                figsize=figsize,
                facecolor="#337ab7",
                bins=bins,
            )
    else:
        plot = series.plot(
            kind="hist",
            figsize=figsize,
            facecolor="#337ab7",
            bins=bins,
        )
    return plot


def histogram(
    series: pd.Series, series_description: dict, bins: Union[int, np.ndarray]
) -> str:
    """Plot an histogram of the data.

    Args:
      series_description:
      series: The data to plot.
      bins: number of bins (int for equal size, ndarray for variable size)

    Returns:
      The resulting histogram encoded as a string.

    """
    plot = _plot_histogram(series, series_description, bins)
    plot.xaxis.set_tick_params(rotation=45)
    plot.figure.tight_layout()
    plt.show()
    
def correlation_matrix(data: pd.DataFrame, vmin: int = -1,img: str = '') -> str:
    """Plot image of a matrix correlation.

    Args:
      data: The matrix correlation to plot.
      vmin: Minimum value of value range.

    Returns:
      The resulting correlation matrix encoded as a string.
    """
    fig_cor, axes_cor = plt.subplots(1, 1)
    labels = data.columns
    matrix_image = axes_cor.imshow(
        data,
        vmin=vmin,
        vmax=1,
        interpolation="nearest",
        cmap=config["plot"]["correlation"]["cmap"].get(str),
    )
    plt.colorbar(matrix_image)
    axes_cor.set_xticks(np.arange(0, data.shape[0], float(data.shape[0]) / len(labels)))
    axes_cor.set_yticks(np.arange(0, data.shape[1], float(data.shape[1]) / len(labels)))
    axes_cor.set_xticklabels(labels, rotation=90)
    axes_cor.set_yticklabels(labels)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(img)
    plt.close()
