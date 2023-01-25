#!/usr/bin/env bash

./scripts/00-download-country-codes.py --out-file data/00-raw/country-codes.tsv
./scripts/01-tidy-country-codes.py --out-file data/01-tidied/country-codes.tsv data/00-raw/country-codes.tsv
./scripts/01-tidy-house-prices.py --out-file data/01-tidied/house-prices.tsv data/00-raw/house-prices.csv