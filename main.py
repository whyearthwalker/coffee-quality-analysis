import pandas as pd
from utils import (
    download_file, top_10_export_countries, top_10_export_countries_plot, correlation_heatmap, color_influence,
    spearman_correlation, coffee_country_influence, altitude_influence,
)

download_file()
"""
Function download_file:
Checking is file downloaded,
if not - checking url for errors
downloading file
"""
df = pd.read_table('coffe_ratings.csv', sep=',')


top_10_export_countries(df)

"""
Function top_10_export_countries
creating copy of dataframe , cleaning , converting lbs to kg
counting all weight and bags quantity
sums up total weight by country
creating top 10
"""

top_10_export_countries_plot(df)

"""
Function top_10_export_countries_plot
building gradient graphics by data from previous function
"""

correlation_heatmap(df)

"""
Function correlation_heatmap
Excluding 3 columns
Selects attributes witch >= 0.65
Building heatmap correlation by Pearson method
"""

color_influence(df)

"""
Function color_influence:
visualizes the effect of coffee bean color on the
average total cup points for different coffee species
using a bar plot.
"""

spearman_correlation(df)

"""
Function spearman_correlation:
creating copy, changing type of column,
making correlation by spearman method
printing result
"""

coffee_country_influence(df)

"""
Function coffee_country_influence:
Clearing not available values,
grouping 2 columns, counting mean value,
sorting values, building horizontal bar plot
"""

altitude_influence(df)

"""
Function altitude_influence:
Creating copy, clearing not available values,
clearing not correct values,
building kde plot,
creating vertical lines from 80 to 85, total cup points,
creating horizontal lines from 500 to 2000, altitude mean meters,
installing borders
"""



