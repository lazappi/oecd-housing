# OECD housing

This repository contains some basic analysis of housing price, affordability and taxation statistics from the OECD.
You can see the final report at https://lazappi.github.io/oecd-housing/.

## Directory structure

- `data/` - Data files
  - `00-raw/` - Raw data files
  - `01-tidied/` - Tidied versions of the individual data files
  - `02-combined.tsv` - The final combined and summarised data file used for analysis
- `docs/` - The rendered HTML report available at https://lazappi.github.io/oecd-housing/
- `output/` - Output files from analysis stages
- `scripts/` - Python files used to perform the analysis
  - `00-download-country-codes.py` - Download country code information from Wikipedia
  - `01-tidy-country-codes.py` - Tidy the country codes data
  - `01-tidy-house-prices.py` - Tidy the house prices data
  - `01-tidy-property-tax.py` - Tidy the property tax data
  - `02-combine-datasets.py` - Combine the datasets into a single file for analysis
  - `03-plot-barplot.py` - Plot bar plots showing values for a variable and their change over time
  - `03-plot-scatterplot.py` - Plot the relationship between two variables and their changes over time
- `_quarto.yml` - Quarto config file
- `environment.yml` - Conda environment file
- `index.qmd` - Quarto file used to write the final report
- `LICENSE` - MIT license
- `README.md` - This README
- `run-analysis.sh` - Shell script to run the analysis steps in order

## Sources

The housing and taxation statistics were downloaded from the OECD stats explorer https://stats.oecd.org/>.

Country code information was download from the Wikipedia ISO Country Codes page https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes.

All data from these sources is covered by their respective licences.
