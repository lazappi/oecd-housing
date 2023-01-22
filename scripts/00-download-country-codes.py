#!/usr/bin/env python

"""
Download country code from Wikipedia

Usage:
    00-download-country-codes.py --out-file=<path> [options]

Options:
    -h --help            Show this screen.
    --out-file=<path>    Path to output file.
"""


def download_country_codes():
    """
    Download country codes from Wikipedia

    :return: DataFrame containing country codes
    """
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup

    url = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
    print(f"Reading '{url}'...")
    response = requests.get(url)

    print("Extracting HTML table...")
    soup = BeautifulSoup(response.text, "html.parser")
    html_table = soup.find("table", {"class": "wikitable"})

    print("Converting HTML table to DataFrame...")
    codes = pd.read_html(str(html_table))[0]
    codes.columns = codes.columns.droplevel()

    print(codes)

    return codes


def main():
    """The main script function"""
    from docopt import docopt

    args = docopt(__doc__)

    out_file = args["--out-file"]

    output = download_country_codes()
    print(output)
    print(f"Writing output to '{out_file}'...")
    output.to_csv(out_file, sep="\t", index=False)
    print("Done!")


if __name__ == "__main__":
    main()
