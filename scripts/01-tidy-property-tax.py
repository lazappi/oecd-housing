#!/usr/bin/env python

"""
Tidy property tax table

Usage:
    01-tidy-property-tax.py --out-file=<path> [options] <file>

Options:
    -h --help            Show this screen.
    --out-file=<path>    Path to output file.
"""


def tidy_property_tax(property_tax):
    """
    Tidy property tax DataFrame

    :param: DataFrame containing property tax data

    :return: Tidied property tax DataFrame
    """

    print("Tidying property tax...")
    # Select columns
    property_tax = property_tax.drop(
        [
            "INDICATOR",
            "SUBJECT",
            "FREQUENCY",
            "Flag Codes",
        ],
        axis=1,
    )
    # Pivot wider to make values into separate columns
    property_tax = property_tax.pivot(
        index=["LOCATION", "TIME"], columns="MEASURE", values="Value"
    )
    property_tax = property_tax.reset_index()
    # Rename columns
    property_tax = property_tax.rename(
        columns={
            "LOCATION": "Code3",
            "TIME": "Year",
            "PC_GDP": "PctGDP",
            "PC_TOT_TAX": "PctTotalTax",
        }
    )
    # Filter to years from 2000 onwards
    property_tax = property_tax[property_tax["Year"].astype(int) >= 2000]

    return property_tax


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
    output = tidy_property_tax(input)
    print(output)
    print(f"Writing output to '{out_file}'...")
    output.to_csv(out_file, sep="\t", index=False)
    print("Done!")


if __name__ == "__main__":
    main()
