#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 18:23:17 2021

@author: martin
"""

import ast
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

def process_data(data):
    """
    Process data argument to prepare the data for analysis and modelling
    
    data: Pandas DataFrame
        Tidy data from CSV file of guitar info from Thomann website
    
    """
    # extract dictionaries of info from further_info_table column
    for i, row in data.iterrows():
        further_info = ast.literal_eval(row["further_info_table"])
        for info in further_info:
            for k, v in further_info.items():
                data.loc[i, k] = v
    
    # format price column
    fix_price = lambda price: int(price[1:].replace(',', ''))
    data['price'] = data['price'].apply(fix_price)
    
    # remove leading and trailing whitespace from string columns
    # make string column lower case as well
    string_cols = data.select_dtypes(include=['object']).columns
    for col in string_cols:
        data[col] = data[col].str.strip().str.lower()
        
    # define columns if guitar is a signature model or if there is a soundboard
    data['signature_model'] = np.where(data['Artist'].isna(), 0, 1)
    data['has_soundboard'] = np.where(data['Soundboard'].isna(), 0, 1)
    
    # change scale and frets columns to integers
    data['Scale'] = data['Scale'].str.replace(' mm', '').astype(float)
    data['Frets'] = data['Frets'].astype(float)
    
    # fill num_reviews with 0 if NaN
    data['num_reviews'].fillna(0, inplace=True)
    
    # months guitar has been available
    data['months_available'] = _get_months_available(data['sales_info'])
    
    # make dummy columns
    dummy_cols = ['Colour', 'Body', 'Top', 'Neck', 'Fretboard', 'Pickups',
                  'Tremolo', 'Incl. Case']
    for col in dummy_cols:
        data = pd.concat([data,#.drop(col, axis=1),
                          pd.get_dummies(data[col], dummy_na=True,
                                         prefix=col)], axis=1)
    
    # drop columns which are of no use
    data.drop(columns=['further_info_table', 'Active Pickups', 'Model',
                       'Style', 'Shape', 'Pickup System', 'Incl. Bag',
                       'Artist', 'Soundboard', 'sales_info'], inplace=True)
    
    # TODO: process_info_list
    data.drop(columns=['info_list'], inplace=True)
    
    return data

def _get_months_available(info_col):
    months = []
    for data in info_col:
        d = ast.literal_eval(data)
        if 'available since' in d.keys():
            date = d['available since']
            since = datetime.strptime(date, "%B %Y")
            now = datetime.now()  
            diff = (now - since).days / 30
            months.append(diff)
        else:
            months.append(np.nan)
    return months
    

def question_one(data):
    """
    Q1. How does the price affect the sales rank?
    The best rank is 1.
    
    """
    # select price and sales rank columns
    sub = data[['price', 'rank_overall', 'rank_in_group']]
    # non-linear correlation check using Spearman
    plt.subplot(131)
    sns.heatmap(sub.corr(method='spearman'), annot=True)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.subplot(132)
    sns.scatterplot(x='price', y='rank_overall', data=sub)
    # scatterplot of rank_overall shows 3 distinct groups when these products
    # compete with other categories, but for their own group, the
    # distribution is more homogeneous
    plt.subplot(133)
    sns.scatterplot(x='price', y='rank_in_group', data=sub)
    # observation: price is moderately correlated with rank
    
def question_two(data):
    """
    Q2. How does the choice of wood for different parts affect the sales rank?

    """
    pass

def question_three(data):
    """
    Q3. 
    
    """
    pass

try:
    print('Reading processed dataframe')
    df = pd.read_csv('lp_prices_processed.csv')
except:
    raw_df = pd.read_csv('lp_prices.csv')
    df = process_data(raw_df)
    df.to_csv('lp_prices_processed.csv', index=False)
