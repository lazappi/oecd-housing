#!/usr/bin/env python

"""
Plot Real Price Index

Usage:
    03-plot-RPI.py --out-file=<path> [options] <file>

Options:
    -h --help            Show this screen.
    --out-file=<path>    Path to output file.
"""


def plot_rpi(combined):
    """
    Plot Real Price Index

    :param combined: DataFrame containing combined dataset

    :return: matplotlib axes object
    """

    import seaborn as sns
    import matplotlib.pyplot as plt

    # Set seaborn style
    sns.set_style("whitegrid")
    sns.set_context("talk")

    # Filter to most recent year and sort by RealPriceIndex
    plot_data = combined[combined["Year"] == 2020]
    plot_data = plot_data.sort_values(by="RealPriceIndex", ascending=False)

    # Set colours to highlight countries of interest
    colours = [
        "#E89611"
        if country in ["NZL", "SWE", "CAN", "JPN"]
        else "#1C4EAA"
        if country == "OECD"
        else "#374043"
        for country in plot_data["Code3"]
    ]

    # Plot bar chart
    ax = sns.barplot(x="RealPriceIndex", y="Country", data=plot_data, palette=colours)
    fig = ax.get_figure()

    # Add title and labels
    ax.set_title("2020 Real Price Index", loc="left")
    ax.set(xlabel=None, ylabel=None, yticklabels=[])
    # Add source
    fig.text(
        x=0.05,
        y=0.01,
        s="Source: OECD, https://stats.oecd.org/",
        fontsize=10,
        color="grey",
    )

    # Label bars
    padding = 0.01 * max(plot_data["RealPriceIndex"])
    for idx, country in enumerate(plot_data["Country"]):
        ax.text(
            x=0 + padding,
            y=idx + 0.5 / 2,
            s=country,
            color="white",
            fontsize=12,
        )

    # Show plot
    plt.tight_layout()
    fig.set_size_inches(8, 10)

    return ax


def main():
    """The main script function"""
    from docopt import docopt
    from pandas import read_csv

    args = docopt(__doc__)

    file = args["<file>"]
    out_file = args["--out-file"]

    print(f"Reading data from '{file}'...")
    input = read_csv(file, sep="\t")
    print(input)
    print("Plotting RPI...")
    plot = plot_rpi(input)
    output = plot.get_figure()
    print(output)
    print(f"Writing output to '{out_file}'...")
    output.savefig(out_file)
    print("Done!")


if __name__ == "__main__":
    main()
