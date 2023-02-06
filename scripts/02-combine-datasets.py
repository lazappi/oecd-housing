#!/usr/bin/env python

"""
Combine datasets

Usage:
    02-combine-datasets.py --country-codes=<path> --house-prices=<path> --property-tax=<path> --out-file=<path> [options]

Options:
    -h --help                 Show this screen.
    --country-codes=<path>    Path to TSV file containing country codes.
    --house-prices=<path>     Path to TSV file containing house prices data.
    --property-tax=<path>     Path to TSV file containing property tax data.
    --out-file=<path>         Path to output file.
"""


def combine_datasets(country_codes, house_prices, property_tax):
    """
    Combine country codes, house prices and property tax data into a single DataFrame

    :param country_codes: DataFrame containing country codes
    :param house_prices: DataFrame containing house prices data
    :param property_tax: DataFrame containing property tax data

    :return: DataFrame containing combined data
    """

    from pandas import concat, Series

    print("Merging house prices and property tax...")
    # Rename the OAVG country code to OECD for consistency
    property_tax["Code3"].replace("OAVG", "OECD", inplace=True)
    # Get intersection of country codes and filter to those
    property_codes = set(property_tax["Code3"].unique())
    house_prices_codes = set(house_prices["Code3"].unique())
    shared_codes = property_codes.intersection(house_prices_codes)
    property_tax = property_tax[property_tax["Code3"].isin(shared_codes)]
    house_prices = house_prices[house_prices["Code3"].isin(shared_codes)]
    # Merge house prices and property tax using Code3 and Year
    # Use inner join to only keep rows present in both datasets
    combined = house_prices.merge(property_tax, on=["Code3", "Year"], how="inner")

    print("Adding country names...")
    # Select three letter code and country names
    country_codes = country_codes[["Code3", "Country"]]
    # Add row for OECD average
    oecd_code = Series({"Code3": "OECD", "Country": "OECD Average"})
    country_codes = concat([country_codes, oecd_code.to_frame().T], ignore_index=True)
    # Add country names to combined dataset
    combined = combined.merge(country_codes, on="Code3", how="left")
    # Move country name column
    combined.insert(1, "Country", combined.pop("Country"))

    print("Adding country labels...")
    combined["CountryLabel"] = combined["Country"]
    # Replace country names with labels
    combined["CountryLabel"] = combined["CountryLabel"].replace(
        {
            "United Kingdom of Great Britain and Northern Ireland (the)": "United Kingdom",
            "Korea (the Republic of)": "Republic of Korea",
            "United States of America (the)": "United States",
            "Netherlands (the)": "Netherlands",
        }
    )
    combined["CountryLabel"] = combined["CountryLabel"] + " (" + combined["Code3"] + ")"
    combined.insert(2, "CountryLabel", combined.pop("CountryLabel"))

    # Remove countries with incomplete years
    print("Removing countries with incomplete years...")
    # Filter years after 2020
    combined = combined[combined["Year"] <= 2020]
    # Remove entries with missing values
    combined = combined.dropna()
    # Get list of countries with complete years
    complete_countries = (
        combined.groupby("Code3")
        .filter(lambda x: min(x["Year"]) == 2000 and max(x["Year"]) == 2020)["Code3"]
        .unique()
    )
    combined = combined[combined["Code3"].isin(complete_countries)]

    return combined


def main():
    """The main script function"""
    from docopt import docopt
    from pandas import read_csv

    args = docopt(__doc__)

    country_codes_file = args["--country-codes"]
    house_prices_file = args["--house-prices"]
    property_tax_file = args["--property-tax"]
    out_file = args["--out-file"]

    print(f"Reading country codes from '{country_codes_file}'...")
    country_codes = read_csv(country_codes_file, sep="\t")
    print(country_codes)
    print(f"Reading house prices from '{house_prices_file}'...")
    house_prices = read_csv(house_prices_file, sep="\t")
    print(house_prices)
    print(f"Reading property tax from '{property_tax_file}'...")
    property_tax = read_csv(property_tax_file, sep="\t")
    print(property_tax)
    print("Combining datasets...")
    output = combine_datasets(country_codes, house_prices, property_tax)
    print(output)
    print(f"Writing output to '{out_file}'...")
    output.to_csv(out_file, sep="\t", index=False)
    print("Done!")


if __name__ == "__main__":
    main()
