import requests as rq
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np
from pathlib import Path

from matplotlib.container import BarContainer


def download_file():
    filename = 'coffe_ratings.csv'
    if not os.path.exists(filename):
        url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-07-07/coffee_ratings.csv'
        response = rq.get(url)
        if response.status_code == 200:
            with open('coffe_ratings.csv', 'wb') as f:
                f.write(response.content)
                print('File successfully downloaded')
        else:
            print('Error downloading file')
    return filename

# download_file()
# df = pd.read_table('coffe_ratings.csv', sep=',')

"""
Checking is file downloaded, 
if not - checking url for errors 
downloading file 
"""

PLOTS_DIR = Path('plots')
PLOTS_DIR.mkdir(exist_ok=True)

def save_plot(name:str):
    path = PLOTS_DIR / f'{name}.png'
    plt.savefig(path, dpi=300, bbox_inches='tight')

"""
Function save_plot:
saving plots to folder in png
"""


def top_10_export_countries(df):
    df_clean = df.copy(deep=True)

    def clean_weight(weight_str):
        if pd.isna(weight_str):
            return 0
        weight_str = str(weight_str).lower()
        numbers = re.findall(r'\d+', weight_str)
        if not numbers:
            return 0
        weight = float(numbers[0])

        if 'lbs' in weight_str and 'kg' not in weight_str:
            weight = weight * 0.45

        return weight

    df_clean['bag_weight_kg'] = df_clean['bag_weight'].apply(clean_weight)
    df_clean['total_weight'] = df_clean['number_of_bags'] * df_clean['bag_weight_kg']
    export_by_country = df_clean.groupby('country_of_origin')['total_weight'].sum()

    return export_by_country.sort_values(ascending=False).head(10)


"""
Function top_10_export_countries
creating copy of dataframe , cleaning , converting lbs to kg 
counting all weight and bags quantity
sums up total weight by country
creating top 10 
"""

# top_10_export_result = top_10_export_countries(df)
# print(top_10_export_result)


def top_10_export_countries_plot(df, top_n=10, color_palette='viridis'):
    result = top_10_export_countries(df)
    tons = result.head(top_n) / 1000

    colors = plt.colormaps[color_palette](np.linspace(0.3,0.95, len(tons)))
    fig, ax = plt.subplots(figsize=(12,7))
    ax.barh(range(len(tons)), tons.values, color=colors, edgecolor='white', linewidth=2)

    ax.set_yticks(range(len(tons)))
    ax.set_yticklabels(tons.index, fontsize = 11)
    ax.invert_yaxis()
    ax.set_xlim(0, max(tons.values) * 1.12)


    for i, value in enumerate(tons.values):
        ax.text(value + 300, i , f"{value:,.1f}t", va='center', fontsize=11 , fontweight='bold')

    ax.set_xlabel('Export(tonnes)', fontsize=12 , fontweight='bold' )
    ax.set_title(f'Top{top_n} export by country ', fontsize=12, fontweight='bold' , pad=20)
    ax.grid(axis='x', alpha=0.5 , linestyle='-', linewidth=0.7)
    ax.set_axisbelow(True)

    save_plot('top_10_export_countries_plot')
    plt.tight_layout()
    plt.show()


"""
Function top_10_export_countries_plot
building gradient graphics by data from previous function
"""

# top_10_export_countries_plot(df)


def correlation_heatmap(df,threshold=0.65):
    exclude_columns = ['sweetness', 'uniformity', 'clean_cup']

    df_nums = (df.select_dtypes(include='number').drop(columns=exclude_columns, errors='ignore'))

    full_corr = df_nums.corr(method='pearson')

    strong_columns = full_corr.columns[(abs(full_corr) >= threshold).any(axis=0)]
    selected_corr = full_corr.loc[strong_columns, strong_columns]  # исправление

    plt.figure(figsize=(12, 7))
    sns.heatmap(
        selected_corr,
        annot=True,
        fmt='.2f',
        vmin=-1,
        vmax=1,
        cmap='coolwarm'
    )
    plt.title(f'Correlation Heatmap (Pearson)',fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_plot('correlation_heatmap')
    plt.show()


"""
Function correlation_heatmap
Excluding 3 columns
Selects attributes witch >= 0.65
Building heatmap correlation by Pearson method
"""

# correlation_heatmap(df)

def color_influence(df):
    pivot_table = df.pivot_table(
        index='species',
        columns='color',
        values='total_cup_points',
        aggfunc='mean'
    )

    colors = {
        'Blue-Green': '#7FFFD4',
        'Bluish-Green': '#2EB9AE',
        'Green': '#008000'
    }


    pivot_table.plot(kind='bar',
                     figsize=(10,7.3),
                     color=[colors[col] for col in pivot_table.columns],
                     )
    ax = plt.gca()
    for cont in ax.containers:
        if isinstance(cont, BarContainer):
            ax.bar_label(cont,
                         fmt='%.2f',
                         padding=5,
                         fontweight='bold',)


    plt.title('Color Influence', fontsize=14 , fontweight='bold')
    plt.xlabel('Species', fontsize=11 , fontweight='bold' )
    plt.ylabel('Average total Cup Points', fontsize=12 , fontweight='bold')
    plt.legend(title='Color of coffee')
    plt.xticks(rotation=45)
    plt.grid(True)
    save_plot('color_influence')
    plt.show()

"""
Function color_influence:
visualizes the effect of coffee bean color on the
average total cup points for different coffee species
using a bar plot.
"""

# color_influence(df)


def spearman_correlation(df):
    df_corr = df[["country_of_origin","total_cup_points"]].copy(deep=True)
    df_corr["country_catt"] = df_corr["country_of_origin"].astype("category").cat.codes
    spearman_corr = df_corr[['country_catt',"total_cup_points"]].corr("spearman")
    print(spearman_corr)
    return spearman_corr

"""
Function spearman_correlation:
creating copy, changing type of column,
making correlation by spearman method
printing result
"""

# spearman_correlation(df)

def coffee_country_influence(df):

    data = df[['country_of_origin','total_cup_points']].dropna()
    country_mean = (data.groupby('country_of_origin')['total_cup_points'].mean().sort_values(ascending=False))

    plt.figure(figsize=(12,7))
    ax = country_mean.sort_values().plot(kind='barh')
    ax.set_facecolor('lightsteelblue')
    plt.title('Coffee Country Influence', fontsize=14 , fontweight='bold')
    plt.xlabel('Average Total Cup Points', fontsize=10 , fontweight='bold' )
    plt.ylabel('Country of Origin', fontsize=10 , fontweight='bold')
    plt.yticks(fontsize=8)
    plt.grid(axis='x',alpha=1 ,linestyle='--', color='k')
    plt.subplots_adjust(left=0.35)
    plt.xlim(76,86)
    plt.tight_layout()
    save_plot('coffee_country_influence')
    plt.show()

"""
Function coffee_country_influence:
Clearing not available values,
grouping 2 columns, counting mean value,
sorting values, building horizontal bar plot 
"""

# coffee_country_influence(df)


def altitude_influence(df):
    clear_data = df[['total_cup_points','altitude_mean_meters']].copy(deep=True)
    clear_data.dropna(inplace=True)
    clear_data = clear_data[(clear_data['altitude_mean_meters'] >=0) & (clear_data['altitude_mean_meters'] < 5000)]
    clear_data = clear_data[(clear_data['total_cup_points'] >=0) & (clear_data['total_cup_points'] < 100)]

    plt.figure(figsize=(12,7))
    sns.kdeplot(data=clear_data,x='altitude_mean_meters',y='total_cup_points',
                fill=True,cmap='coolwarm',levels=20,thresh=0.05)

    plt.axvline(x=500, linestyle='--', color='black', linewidth=2, alpha=0.7, label='Altitude 500-2000 meters')
    plt.axvline(x=2000, linestyle='--', color='black', linewidth=2, alpha=0.7)
    plt.axhline(y=80, linestyle='--', color='green', linewidth=2, label='Points 80-85', alpha=0.7)
    plt.axhline(y=85, linestyle='--', color='green', linewidth=2, alpha=0.7)

    plt.xlim(-300,2500)
    plt.ylim(60,clear_data['total_cup_points'].max())

    plt.title('Altitude Influence', fontsize=14 , fontweight='bold')
    plt.xlabel('Altitude Mean Meters', fontsize=10 , fontweight='bold')
    plt.ylabel('Total cup points', fontsize=10 , fontweight='bold')
    plt.yticks(fontsize=8)
    plt.legend()
    plt.tight_layout()
    save_plot('altitude_influence')
    plt.show()

    return clear_data

"""
Function altitude_influence:
Creating copy, clearing not available values,
clearing not correct values,
building kde plot,
creating vertical lines from 80 to 85, total cup points,
creating horizontal lines from 500 to 2000, altitude mean meters,
installing borders
"""


# altitude_influence(df)
