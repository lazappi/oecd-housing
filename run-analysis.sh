#!/usr/bin/env bash

# ==== 0. GET DATASETS ==== #
echo "Downloading country codes..."
./scripts/00-download-country-codes.py --out-file data/00-raw/country-codes.tsv

# ==== 1. TIDY DATASETS ==== #
echo "Tidying country codes..."
./scripts/01-tidy-country-codes.py --out-file data/01-tidied/country-codes.tsv data/00-raw/country-codes.tsv
echo "Tidying house prices..."
./scripts/01-tidy-house-prices.py --out-file data/01-tidied/house-prices.tsv data/00-raw/house-prices.csv
echo "Tidying property tax..."
./scripts/01-tidy-property-tax.py --out-file data/01-tidied/property-tax.tsv data/00-raw/property-tax.csv
