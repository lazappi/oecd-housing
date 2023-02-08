#!/usr/bin/env bash

# ==== 00. GET DATASETS ==== #
echo "Downloading country codes..."
./scripts/00-download-country-codes.py --out-file data/00-raw/country-codes.tsv

# ==== 01. TIDY DATASETS ==== #
echo "Tidying country codes..."
./scripts/01-tidy-country-codes.py --out-file data/01-tidied/country-codes.tsv data/00-raw/country-codes.tsv
echo "Tidying house prices..."
./scripts/01-tidy-house-prices.py --out-file data/01-tidied/house-prices.tsv data/00-raw/house-prices.csv
echo "Tidying property tax..."
./scripts/01-tidy-property-tax.py --out-file data/01-tidied/property-tax.tsv data/00-raw/property-tax.csv

# ==== 02. COMBINE DATASETS ==== #
echo "Combining datasets..."
./scripts/02-combine-datasets.py \
    --country-codes data/01-tidied/country-codes.tsv \
    --house-prices data/01-tidied/house-prices.tsv \
    --property-tax data/01-tidied/property-tax.tsv \
    --out-file data/02-combined.tsv

# ==== 03. PLOT VARIABLES ==== #
echo "Plotting Real Price Index..."
./scripts/03-plot-barplot.py \
    --out-file output/03-RPI-barplot.png \
    --var RealPriceIndex \
    --label "Real Price Index" \
    data/02-combined.tsv
echo "Plotting Price to Income Ratio..."
./scripts/03-plot-barplot.py \
    --out-file output/03-PriceRatio-barplot.png \
    --var PriceIncomeRatio \
    --label "Price to Income Ratio" \
    data/02-combined.tsv
echo "Plotting Percent GDP..."
./scripts/03-plot-barplot.py \
    --out-file output/03-PctGDP-barplot.png \
    --var PctGDP \
    --label "Housing Tax Percentage of GDP" \
    data/02-combined.tsv
echo "Plotting Percent Total Tax..."
./scripts/03-plot-barplot.py \
    --out-file output/03-PctTotalTax-barplot.png \
    --var PctTotalTax \
    --label "Housing Tax Percentage of Total Tax" \
    data/02-combined.tsv
echo "Plotting Real Price Index vs Price to Income Ratio..."
./scripts/03-plot-scatterplot.py \
    --out-file output/03-RPI-PriceRatio-scatterplot.png \
    --x-var RealPriceIndex \
    --x-label "Real Price Index" \
    --y-var PriceIncomeRatio \
    --y-label "Price to Income Ratio" \
    data/02-combined.tsv
echo "Plotting Percent Total Tax vs Percent GDP..."
./scripts/03-plot-scatterplot.py \
    --out-file output/03-PctTotalTax-PctGDP-scatterplot.png \
    --x-var PctTotalTax \
    --x-label "Housing Tax Percentage of Total Tax" \
    --y-var PctGDP \
    --y-label "Housing Tax Percentage of GDP" \
    data/02-combined.tsv
echo "Percent GDP vs Real Price Index..."
./scripts/03-plot-scatterplot.py \
    --out-file output/03-PctGDP-RPI-scatterplot.png \
    --x-var PctGDP \
    --x-label "Housing Tax Percentage of GDP" \
    --y-var RealPriceIndex \
    --y-label "Real Price Index" \
    data/02-combined.tsv
echo "Percent Total Tax vs Real Price Index..."
./scripts/03-plot-scatterplot.py \
    --out-file output/03-PctTotalTax-RPI-scatterplot.png \
    --x-var PctTotalTax \
    --x-label "Housing Tax Percentage of Total Tax" \
    --y-var RealPriceIndex \
    --y-label "Real Price Index" \
    data/02-combined.tsv
echo "Percent GDP vs Price Income Ratio..."
./scripts/03-plot-scatterplot.py \
    --out-file output/03-PctGDP-PriceRatio-scatterplot.png \
    --x-var PctGDP \
    --x-label "Housing Tax Percentage of GDP" \
    --y-var PriceIncomeRatio \
    --y-label "Price to Income Ratio" \
    data/02-combined.tsv
echo "Pct Total Tax vs Price Income Ratio..."
./scripts/03-plot-scatterplot.py \
    --out-file output/03-PctTotalTax-PriceRatio-scatterplot.png \
    --x-var PctTotalTax \
    --x-label "Housing Tax Percentage of Total Tax" \
    --y-var PriceIncomeRatio \
    --y-label "Price to Income Ratio" \
    data/02-combined.tsv

# ==== 90. RENDER REPORT ==== #
echo "Rendering HTML report..."
quarto render

echo "Done!"
