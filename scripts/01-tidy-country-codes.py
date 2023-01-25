#!/usr/bin/env python

"""
Tidy country codes table

Usage:
    01-tidy-country-codes.py --out-file=<path> [options] <file>

Options:
    -h --help            Show this screen.
    --out-file=<path>    Path to output file.
"""


def tidy_country_codes(codes):
    """
    Tidy country codes DataFrame

    :param: DataFrame containing country codes

    :return: Tidied country codes DataFrame
    """

    print("Tidying country codes...")
    codes = codes.iloc[:, [0, 1, 3, 4, 5, 7]]
    codes = codes.rename(
        columns={
            "Country name[5]": "Country",
            "Official state name[6]": "OfficialName",
            "Alpha-2 code[5]": "Code2",
            "Alpha-3 code[5]": "Code3",
            "Numeric code[5]": "CodeNumeric",
            "Internet ccTLD[9]": "TLD",
        }
    )
    codes = codes.sort_values(by="Country")
    # Remove footnotes
    codes = codes.apply(lambda x: x.str.replace("\s?\\[[a-z]+\\]\s?", "", regex=True))
    # Replace rogue HTML in the first Code2 value
    codes["Code2"][0] = "AF"
    # Remove annotation rows
    codes = codes[~(codes["Code2"] == codes["Code3"])]

    return codes


def main():
    """The main script function"""
    from docopt import docopt
    from pandas import read_csv

    args = docopt(__doc__)

    file = args["<file>"]
    out_file = args["--out-file"]

    print(f"Reading input from '{file}'...")
    input = read_csv(file, sep="\t")
    print(input)
    output = tidy_country_codes(input)
    print(output)
    print(f"Writing output to '{out_file}'...")
    output.to_csv(out_file, sep="\t", index=False)
    print("Done!")


if __name__ == "__main__":
    main()
