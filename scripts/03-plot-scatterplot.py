#!/usr/bin/env python

"""
Plot a scatter plot showing the relationship between two variables by country (for both current values and changes)

Usage:
    03-plot-scatterplot.py --out-file=<path> --x-var=<str> --x-label=<str> --y-var=<str> --y-label=<str> [options] <file>

Options:
    -h --help            Show this screen.
    --out-file=<path>    Path to output file.
    --x-var=<str>        Name of the variable to plot on the x-axis.
    --x-label=<str>      Label for the variable on the x-axis.
    --y-var=<str>        Name of the variable to plot on the y-axis.
    --y-label=<str>      Label for the variable on the y-axis.
"""


def plot_scatter(combined, x_var, x_label, y_var, y_label):
    """
    Plot scatter plot

    :param combined: DataFrame containing combined dataset
    :param x_var: Name of the variable to plot on the x-axis
    :param x_label: Label for the variable on the x-axis
    :param y_var: Name of the variable to plot on the x-axis
    :param y_label: Label for the variable on the x-axis

    :return: matplotlib figure object
    """

    import matplotlib.pyplot as plt
    import seaborn as sns

    # Set seaborn style
    sns.set_style("whitegrid")
    sns.set_context("talk")

    fig, axs = plt.subplots(ncols=2)

    fig.tight_layout(pad=0)

    plt.subplots_adjust(wspace=0.2)

    combined["Code3"] = combined["Code3"].astype("category")
    colours = get_colours(combined)
    plot_current(combined, x_var, x_label, y_var, y_label, colours, ax=axs[0])
    plot_change(combined, x_var, x_label, y_var, y_label, colours, ax=axs[1])

    # Add source
    fig.text(
        x=0.03,
        y=-0.02,
        s="Source: OECD, https://stats.oecd.org/",
        fontsize=10,
        color="grey",
    )

    fig.set_size_inches(16, 8)

    return fig


def plot_current(combined, x_var, x_label, y_var, y_label, colours, ax=None):
    """
    Plot scatter plot of current values

    :param combined: DataFrame containing combined dataset
    :param x_var: Name of the variable to plot on the x-axis
    :param x_label: Label for the variable on the x-axis
    :param y_var: Name of the variable to plot on the x-axis
    :param y_label: Label for the variable on the x-axis
    :param colours: List of colours for each country
    :param ax: matplotlib axes object to use

    :return: matplotlib axes object
    """

    import seaborn as sns

    # Filter to most recent year
    plot_data = combined[combined["Year"] == max(combined["Year"])]

    # Plot scatter plot
    sns.regplot(
        x=x_var,
        y=y_var,
        scatter_kws={"color": colours},
        line_kws={"color": "#7ea8be"},
        data=plot_data,
        ax=ax,
        seed=1,
    )
    label_points(plot_data[x_var], plot_data[y_var], plot_data["Code3"], colours, ax=ax)

    # Add title and labels
    ax.set_title(f"Comparison of current values", loc="left")
    ax.set(xlabel=f"2020 {x_label}", ylabel=f"2020 {y_label}")

    return ax


def plot_change(combined, x_var, x_label, y_var, y_label, colours, ax=None):
    """
    Plot change in Real Price Index

    :param combined: DataFrame containing combined dataset
    :param x_var: Name of the variable to plot on the x-axis
    :param x_label: Label for the variable on the x-axis
    :param y_var: Name of the variable to plot on the x-axis
    :param y_label: Label for the variable on the x-axis
    :param colours: List of colours for each country
    :param ax: matplotlib axes object to use

    :return: matplotlib axes object
    """

    import seaborn as sns
    import pandas as pd

    # Calculate changes by country
    plot_data = combined.groupby("Code3", sort=False).apply(
        lambda x: pd.Series(
            data=[
                x["Code3"].iloc[0],
                x["CountryLabel"].iloc[0],
                x[x_var][x["Year"] == min(x["Year"])].iloc[0],
                x[x_var][x["Year"] == max(x["Year"])].iloc[0],
                x[y_var][x["Year"] == min(x["Year"])].iloc[0],
                x[y_var][x["Year"] == max(x["Year"])].iloc[0],
            ],
            index=["Code3", "CountryLabel", "xFirst", "xLast", "yFirst", "yLast"],
        )
    )
    plot_data["xChange"] = plot_data["xLast"] - plot_data["xFirst"]
    plot_data["yChange"] = plot_data["yLast"] - plot_data["yFirst"]

    # Plot scatter plot
    sns.regplot(
        x="xChange",
        y="yChange",
        scatter_kws={"color": colours},
        line_kws={"color": "#7ea8be"},
        data=plot_data,
        ax=ax,
        seed=1,
    )
    label_points(
        plot_data["xChange"], plot_data["yChange"], plot_data["Code3"], colours, ax=ax
    )

    # Add title and labels
    ax.set_title(f"Comparison of changes", loc="left")
    ax.set(
        xlabel=f"Change in {x_label} since 2000",
        ylabel=f"Change in {y_label} since 2000",
    )

    return ax


def get_colours(plot_data):
    """
    Get country colours

    :param plot_data: DataFrame containing the data to plot

    :return: List of colours for each country
    """

    # Set colours to highlight countries of interest
    colours = [
        "#E89611"
        if country in ["NZL", "SWE", "CAN", "JPN"]
        else "#1C4EAA"
        if country == "OECD"
        else "#374043"
        for country in plot_data["Code3"].cat.categories
    ]

    return colours


def label_points(x, y, labels, colours, ax):

    from adjustText import adjust_text
    from numpy.random import seed

    seed(1)

    texts = []
    for point in range(len(x)):
        texts.append(
            ax.text(
                x.iloc[point],
                y.iloc[point],
                labels.iloc[point],
                color=colours[point],
                fontsize=12,
            )
        )

    # Automatically adjust text positions
    adjust_text(texts, expand_points=(1.2, 1.2), ax=ax)

    return ax


def main():
    """The main script function"""
    from docopt import docopt
    from pandas import read_csv

    args = docopt(__doc__)

    file = args["<file>"]
    out_file = args["--out-file"]
    x_var = args["--x-var"]
    x_label = args["--x-label"]
    y_var = args["--y-var"]
    y_label = args["--y-label"]

    print(f"Reading data from '{file}'...")
    input = read_csv(file, sep="\t")
    print(input)
    print(f"Plotting scatter plot of {x_var} ({x_label}) vs {y_var} ({y_label})...")
    output = plot_scatter(input, x_var, x_label, y_var, y_label)
    print(output)
    print(f"Writing output to '{out_file}'...")
    output.savefig(out_file, bbox_inches="tight")
    print("Done!")


if __name__ == "__main__":
    main()
