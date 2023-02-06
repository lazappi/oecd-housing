#!/usr/bin/env python

"""
Plot a bar plot showing the current value of a variable by country and the change over time

Usage:
    03-plot-barplot.py --out-file=<path> --var=<str> --label=<str> [options] <file>

Options:
    -h --help            Show this screen.
    --out-file=<path>    Path to output file.
    --var=<str>          Name of the variable to plot.
    --label=<str>        Label for the variable.
"""


def plot_barplot(combined, var, label):
    """
    Plot Real Price Index

    :param combined: DataFrame containing combined dataset
    :param var: Name of the variable to plot
    :param label: Label for the variable

    :return: matplotlib axes object
    """

    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    # Set seaborn style
    sns.set_style("whitegrid")
    sns.set_context("talk")

    fig, axs = plt.subplots(ncols=2)

    fig.tight_layout(pad=0)

    plt.subplots_adjust(wspace=0.1)

    order_data = combined[combined["Year"] == max(combined["Year"])]
    order_data = order_data.sort_values(by=var, ascending=False)
    combined["Code3"] = pd.Categorical(
        combined["Code3"], categories=order_data["Code3"]
    )
    combined["Country"] = pd.Categorical(
        combined["Country"], categories=order_data["Country"]
    )
    combined.sort_values(by=["Code3", "Year"], inplace=True)

    colours = get_colours(combined)
    plot_current(combined, var, label, colours, ax=axs[0])
    plot_change(combined, var, label, colours, ax=axs[1])

    # Add source
    fig.text(
        x=0.08,
        y=0.01,
        s="Source: OECD, https://stats.oecd.org/",
        fontsize=10,
        color="grey",
    )

    fig.set_size_inches(16, 10)

    return fig


def plot_current(combined, var, label, colours, ax=None):
    """
    Plot curent Real Price Index

    :param combined: DataFrame containing combined dataset
    :param var: Name of the variable to plot
    :param label: Label for the variable
    :param colours: List of colours for each country
    :param ax: matplotlib axes object to use

    :return: matplotlib axes object
    """

    import seaborn as sns
    import matplotlib.pyplot as plt

    # Filter to most recent year and sort
    plot_data = combined[combined["Year"] == max(combined["Year"])]

    # Plot bar chart
    sns.barplot(x=var, y="Country", data=plot_data, palette=colours, ax=ax)

    plt.axvline(x=0, color="black")

    # Add title and labels
    ax.set_title(f"2020 {label}", loc="left")
    ax.set(xlabel=None, ylabel=None, yticklabels=[])

    # Label bars
    ax = label_bars(
        ax,
        labels=plot_data["Country"].cat.categories,
        values=list(plot_data[var]),
    )

    return ax


def plot_change(combined, var, label, colours, ax=None):
    """
    Plot change in Real Price Index

    :param combined: DataFrame containing combined dataset
    :param var: Name of the variable to plot
    :param label: Label for the variable
    :param colours: List of colours for each country
    :param ax: matplotlib axes object to use

    :return: matplotlib axes object
    """

    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt

    # Filter to most recent year and sort by RealPriceIndex
    plot_data = combined.groupby("Code3", sort=False).apply(
        lambda x: pd.Series(
            data=[
                x["Code3"].iloc[0],
                x["Country"].iloc[0],
                x[var][x["Year"] == min(x["Year"])].iloc[0],
                x[var][x["Year"] == max(x["Year"])].iloc[0],
            ],
            index=["Code3", "Country", "First", "Last"],
        )
    )
    plot_data["Change"] = plot_data["Last"] - plot_data["First"]
    plot_data["Country"] = pd.Categorical(
        plot_data["Country"], categories=combined["Country"].cat.categories
    )

    # Plot bar chart
    ax = sns.barplot(x="Change", y="Country", data=plot_data, palette=colours, ax=ax)

    plt.axvline(x=0, color="black")

    # Add title and labels
    ax.set_title(f"Change in {label} since 2000", loc="left")
    ax.set(xlabel=None, ylabel=None, yticklabels=[])

    # Label bars
    limits = label_bars(
        ax, labels=plot_data["Country"].cat.categories, values=plot_data["Change"]
    )
    ax.set_xlim(limits[0], limits[1])

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


def label_bars(ax, labels, values):
    """
    Label bars on a bar chart

    :param ax: matplotlib axes object to use
    :param labels: Labels for each bar
    :param values: Values for each bar

    :return: Limits to use for the bar axis
    """

    from numpy import sign

    padding = 0.01 * max(values)
    limits = [min(values), max(values) + padding]
    if min(values) < 0:
        limits[0] = min(values) - padding

    for idx, label in enumerate(labels):
        value = values[idx]
        if value < 0:
            width = abs(min(values))
            align = "right"
        else:
            width = max(values)
            align = "left"

        label_width = len(label) * 0.013
        if label_width > (abs(value) / width):
            x_pos = value
            colour = "#374043"

            x_width = x_pos + sign(value) * (2 * label_width * width + padding)
            if x_width > limits[1]:
                limits[1] = x_width
            elif x_width < limits[0]:
                limits[0] = x_width

        else:
            x_pos = 0
            colour = "white"

        ax.text(
            x=x_pos + sign(value) * padding,
            y=idx + 0.15,
            s=label,
            color=colour,
            fontsize=12,
            horizontalalignment=align,
        )

    return limits


def main():
    """The main script function"""
    from docopt import docopt
    from pandas import read_csv

    args = docopt(__doc__)

    file = args["<file>"]
    out_file = args["--out-file"]
    var = args["--var"]
    label = args["--label"]

    print(f"Reading data from '{file}'...")
    input = read_csv(file, sep="\t")
    print(input)
    print(f"Plotting bar plot of {var} ({label})...")
    output = plot_barplot(input, var, label)
    print(output)
    print(f"Writing output to '{out_file}'...")
    output.savefig(out_file, bbox_inches="tight")
    print("Done!")


if __name__ == "__main__":
    main()
