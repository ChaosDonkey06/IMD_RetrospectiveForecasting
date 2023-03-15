from urllib.request import urlopen
from unidecode import unidecode
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import time
import os

import urllib
import sys

sys.path.insert(0, "../")
from global_config import config

data_dir = config.get_property('data_dir')

def process_url(url, year, mmwr_week):
    contents = urllib.request.urlopen(url)
    lines_c  = contents.readlines(False)
    lines_s  = [l.decode(errors='replace').replace("\n", "").replace("\r", "") for l in lines_c]

    lines_t    = [l.split("\t") for l in lines_s]
    tables_idx     = np.where([len(l)>3 for l in lines_t])
    non_tables_idx = np.where([len(l)<3 for l in lines_t])

    df_lines          = pd.DataFrame(lines_t)
    df_table    = df_lines.copy().iloc[tables_idx]
    df_keys           = df_lines.copy().iloc[non_tables_idx][[0]]
    df_keys["length"] = df_keys[0].apply(lambda x: len(x.split(" ")))
    df_keys           = df_keys[df_keys.length>1]
    df_keys           = df_keys.reset_index(drop=True)
    df_keys           = df_keys.iloc[2:np.where(df_keys[0]=="tab delimited data:")[0][0]]
    idx2keys          = {idx: k for idx, k in enumerate( df_keys[0].to_list())}

    df_table["mmwr_week"] = mmwr_week
    df_table["year"]      = year
    df_table              = df_table.rename(columns=idx2keys)

    df_table = df_table[["year", "mmwr_week"]+list(idx2keys.values())]
    df_table = df_table.replace({"-": 0})
    return df_table

from url_cdc import *
df_urls = df_urls.set_index("year")

years_set1 = [1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]

for year in years_set1:

    path_to_save = os.path.join(data_dir, str(year))
    #if os.path.isdir(path_to_save):
    #    continue

    df_url_year = df_urls.loc[year]
    year1_df = []
    for mmwr_week in range(df_url_year["week_start"],df_url_year["week_end"]+1):
        mmwr_week = str(mmwr_week)
        year_df = process_url(df_url_year["base_url1"].format(mmwr_week.zfill(2)), year, mmwr_week)
        year1_df.append(year_df)
    year1_df = pd.concat(year1_df)

    path_to_save = os.path.join(data_dir, "raw_data", str(year))
    if not os.path.isdir(path_to_save):
        os.mkdir(path_to_save)
    print("Saving data for year {}".format(year))
    year1_df.to_csv(os.path.join(path_to_save, "data_meningococcus.csv"))
    time.sleep(90)

years_set2 = [2017, 2018]

for year in years_set2:
    path_to_save = os.path.join(data_dir, "raw_data", str(year))
    df_url_year  = df_urls.loc[year]
    year1_df     = []

    for mmwr_week in range(df_url_year["week_start"],df_url_year["week_end"]+1):
        mmwr_week = str(mmwr_week)
        year_df   = process_url(df_url_year["base_url1"].format(mmwr_week.zfill(2), mmwr_week.zfill(2)), year, mmwr_week)
        year1_df.append(year_df)
    year1_df = pd.concat(year1_df)

    path_to_save = os.path.join(data_dir, "raw_data", str(year))
    if not os.path.isdir(path_to_save):
        os.mkdir(path_to_save)
    print("Saving data for year {}".format(year))
    year1_df.to_csv(os.path.join(path_to_save, "data_meningococcus.csv"))
    time.sleep(90)

years_set2 = [2019, 2020, 2021, 2022]

for year in years_set2:
    path_to_save = os.path.join(data_dir, str(year))
    if os.path.isdir(path_to_save):
        continue

    df_url_year = df_urls.loc[year]
    year1_df = []
    for mmwr_week in range(df_url_year["week_start"],df_url_year["week_end"]+1):
        mmwr_week = str(mmwr_week)
        year_df = process_url(df_url_year["base_url1"].format(mmwr_week.zfill(2), mmwr_week.zfill(2)), year, mmwr_week)
        year1_df.append(year_df)
    year1_df = pd.concat(year1_df)

    path_to_save = os.path.join(data_dir, "raw_data", str(year))
    if not os.path.isdir(path_to_save):
        os.mkdir(path_to_save)
    print("Saving data for year {}".format(year))
    year1_df.to_csv(os.path.join(path_to_save, "data_meningococcus1.csv"))
    time.sleep(90)

    year1_df = []
    for mmwr_week in range(df_url_year["week_start"], df_url_year["week_end"]+1):
        mmwr_week = str(mmwr_week)
        year_df = process_url(df_url_year["base_url2"].format(mmwr_week.zfill(2), mmwr_week.zfill(2)), year, mmwr_week)
        year1_df.append(year_df)
    year1_df = pd.concat(year1_df)

    path_to_save = os.path.join(data_dir, "raw_data", str(year))
    if not os.path.isdir(path_to_save):
        os.mkdir(path_to_save)
    print("Saving data for year {}".format(year))
    year1_df.to_csv(os.path.join(path_to_save, "data_meningococcus2.csv"))
    time.sleep(90)