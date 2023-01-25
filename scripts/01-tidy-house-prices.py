#!/usr/bin/env python

"""
Tidy house prices table

Usage:
    01-tidy-house-prices.py --out-file=<path> [options] <file>

Options:
    -h --help            Show this screen.
    --out-file=<path>    Path to output file.
"""


def tidy_house_prices(house_prices):
    """
    Tidy house prices DataFrame

    :param: DataFrame containing house prices data

    :return: Tidied house prices DataFrame
    """

    print("Tidying house prices...")
    # Select columns
    house_prices = house_prices.drop(
        [
            "Country",
            "Indicator",
            "Time",
            "Unit Code",
            "Unit",
            "PowerCode Code",
            "PowerCode",
            "Reference Period Code",
            "Reference Period",
            "Flag Codes",
            "Flags",
        ],
        axis=1,
    )
    # Pivot wider to make values into separate columns
    house_prices = house_prices.pivot(
        index=["COU", "TIME"], columns="IND", values="Value"
    )
    house_prices = house_prices.reset_index()
    # Rename columns
    house_prices = house_prices.rename(
        columns={
            "COU": "Code3",
            "TIME": "Year",
            "HPI_YDH_AVG": "PriceIncomeRatio",
            "RHP": "RealPriceIndex",
        }
    )
    # Filter to only annual data
    house_prices = house_prices[~house_prices["Year"].str.contains("Q")]

    return house_prices


def main():
    """The main script function"""
    from docopt import docopt
    from pandas import read_csv

    args = docopt(__doc__)

    file = args["<file>"]
    out_file = args["--out-file"]

    print(f"Reading input from '{file}'...")
    input = read_csv(file)
    print(input)
    output = tidy_house_prices(input)
    print(output)
    print(f"Writing output to '{out_file}'...")
    output.to_csv(out_file, sep="\t", index=False)
    print("Done!")


if __name__ == "__main__":
    main()
