from matplotlib.dates import date2num, num2date
from matplotlib.colors import ListedColormap
from matplotlib import dates as mdates
from matplotlib.patches import Patch
from matplotlib import pyplot as plt
from matplotlib import ticker

from urllib.request import urlopen
from unidecode import unidecode

import pandas as pd
import numpy as np
import itertools
import re
import os

import pymmwr as pm
import urllib

import sys

sys.path.insert(0, '../')

from global_config import config
from itertools import chain

results_dir   = config.get_property('results_dir')
data_dir      = config.get_property('data_dir')

plt.rc('font', size=15)

def extract_meningococcal_disease_keys(keys):
    k_r = [ [k] * bool(re.search(r'\bMeningococcal\b', k)) for k in keys ]
    return list(itertools.chain(*k_r))

def values2int(string_input):
    if type(string_input)==str and string_input!="NC" and string_input!="NP" and string_input!="U" and string_input!="N":
        return np.double(string_input.replace(",", ""))
    elif string_input=="NC" or string_input=="NP" or string_input=="U" or string_input=="N":
        return np.nan
    return string_input

year_totals_weekly = {2006: 'Meningococcal diseases, invasive, all serogroups current week',
                    2007: "Meningococcal diseases, invasive �, all serogroups current week",
                    2008: "Meningococcal diseases, invasive �, all serogroups current week",
                    2009: "Meningococcal diseases, invasive �, all serogroups current week",
                    2010: "Meningococcal diseases, invasive �, All groups current week",
                    2011: 'Meningococcal diseases, invasive �, All groups current week',
                    2012: "Meningococcal diseases, invasive �, All groups current week",
                    2013: 'Meningococcal diseases, invasive �, All groups current week',
                    2014: "Meningococcal diseases, invasive �, All groups current week",
                    2015: "Meningococcal diseases, invasive�, All groups current week",
                    2016: "Meningococcal disease, invasive�, All groups current week",
                    2017: "Meningococcal disease(Neisseria meningitidis)�, All serogroups current week",
                    2018: "Meningococcal disease, all serogroups current week"}

keys_rename = {'Meningococcal disease; All serogroups current week': "total",
                    'Meningococcal disease, All serogroups; Current week': "total",
                    'Meningococcal disease; Serogroups ACWY current week': "incidence_ACWY",
                    'Meningococcal disease; Serogroups ACWY cummulative YTD for 2019�': "cum_ACWY_2018�",
                    'Meningococcal disease; Serogroups ACWY cummulative YTD for 2019�': "cum_ACWY_2019�",
                    'Meningococcal disease; Serogroup B current week': "incidence_B",
                    'Meningococcal disease; Serogroups B cummulative YTD for 2019�': "cum_B_2018�",
                    'Meningococcal disease; Serogroups B cummulative YTD for 2019�': "cum_B_2019�",
                    "Reporting Area": "reporting_area"}

regions_rename = {'NEW ENGLAND'   : "New England",
                'MID. ATLANTIC' : "Middle Atlantic",
                'E.N. CENTRAL'  : "East North Central",
                'W.N. CENTRAL'  : "West North Central",
                'S. ATLANTIC'   : "South Atlantic",
                'E.S. CENTRAL'  : "East South Central",
                'W.S. CENTRAL'  : "West South Central",
                'MOUNTAIN'      : "Mountain",
                'PACIFIC'       : "Pacific"}

years_df = []
for year in year_totals_weekly.keys():
    year_df   = pd.read_csv(os.path.join(data_dir, "raw_data", str(year), 'data_meningococcus.csv'), sep=",").drop(columns=["Unnamed: 0"])
    year_df   = year_df.rename(columns={year_totals_weekly[year]: "total"})[["year", "mmwr_week", "Reporting Area", "total"]]
    years_df.append(year_df)
years_df         = pd.concat(years_df)
years_df["date"] = years_df.apply(lambda x: pm.epiweek_to_date(pm.Epiweek(x.year, x.mmwr_week)), axis=1)
years_df         = years_df.rename(columns={"Reporting Area": "reporting_area"})

year     = 2019
year1_df = pd.read_csv(os.path.join(data_dir, "raw_data", str(year), 'data_meningococcus1.csv'), sep=",")#.drop(columns=["Unnamed: 0"])
year2_df = pd.read_csv(os.path.join(data_dir, "raw_data", str(year), 'data_meningococcus2.csv')).drop(columns=["Unnamed: 0"])
year_df  = pd.concat([year1_df, year2_df])
usa_df   = year_df.set_index(["year", "mmwr_week", "Reporting Area"])
usa_df   = usa_df[extract_meningococcal_disease_keys(list(usa_df.keys()))]
usa_df   = usa_df.applymap(values2int)

keys_use = ["total"]
usa_df   = usa_df.reset_index().rename(columns=keys_rename).set_index(["year", "mmwr_week", "reporting_area"])
usa_df         = usa_df.copy()[keys_use].reset_index()
usa_df["date"] = usa_df.apply(lambda x: pm.epiweek_to_date(pm.Epiweek(x.year, x.mmwr_week)), axis=1)

years_df = pd.concat([years_df, usa_df])[["year", "mmwr_week", "reporting_area", "total", "date"]].fillna(0)

############ 2020 ############
year     = 2020
year1_df = pd.read_csv(os.path.join(data_dir, "raw_data", str(year), 'data_meningococcus1.csv')).drop(columns=["Unnamed: 0"])
year2_df = pd.read_csv(os.path.join(data_dir, "raw_data", str(year), 'data_meningococcus2.csv')).drop(columns=["Unnamed: 0"])
year_df  = pd.concat([year1_df, year2_df])
usa_df   = year_df.set_index(["year", "mmwr_week", "Reporting Area"])

usa_df         = usa_df[extract_meningococcal_disease_keys(list(usa_df.keys()))]
usa_df         = usa_df.applymap(values2int)
usa_df         = usa_df.reset_index().rename(columns=keys_rename).set_index(["year", "mmwr_week", "reporting_area"])
usa_df         = usa_df.copy()[keys_use].reset_index()
usa_df["date"] = usa_df.apply(lambda x: pm.epiweek_to_date(pm.Epiweek(x.year, x.mmwr_week)), axis=1)
years_df       = pd.concat([years_df, usa_df])[["year", "mmwr_week", "reporting_area", "total", "date"]].fillna(0)
#############################

############ 2021 ############
year     = 2021
year1_df = pd.read_csv(os.path.join(data_dir, "raw_data", str(year), 'data_meningococcus1.csv')).drop(columns=["Unnamed: 0"])
year2_df = pd.read_csv(os.path.join(data_dir, "raw_data", str(year), 'data_meningococcus2.csv')).drop(columns=["Unnamed: 0"])
year_df  = pd.concat([year1_df, year2_df])
usa_df   = year_df.set_index(["year", "mmwr_week", "Reporting Area"])

usa_df         = usa_df[extract_meningococcal_disease_keys(list(usa_df.keys()))]
usa_df         = usa_df.applymap(values2int)
usa_df         = usa_df.reset_index().rename(columns=keys_rename).set_index(["year", "mmwr_week", "reporting_area"])
usa_df         = usa_df.copy()[keys_use].reset_index()
usa_df["date"] = usa_df.apply(lambda x: pm.epiweek_to_date(pm.Epiweek(x.year, x.mmwr_week)), axis=1)
years_df       = pd.concat([years_df, usa_df])[["year", "mmwr_week", "reporting_area", "total", "date"]].fillna(0)
#############################

############ 2022 ############
year     = 2022
year1_df = pd.read_csv(os.path.join(data_dir, "raw_data", str(year), 'data_meningococcus1.csv')).drop(columns=["Unnamed: 0"])
year2_df = pd.read_csv(os.path.join(data_dir, "raw_data", str(year), 'data_meningococcus2.csv')).drop(columns=["Unnamed: 0"])
year_df  = pd.concat([year1_df, year2_df])
usa_df   = year_df.set_index(["year", "mmwr_week", "Reporting Area"])

usa_df         = usa_df[extract_meningococcal_disease_keys(list(usa_df.keys()))]
usa_df         = usa_df.applymap(values2int)
usa_df         = usa_df.reset_index().rename(columns=keys_rename).set_index(["year", "mmwr_week", "reporting_area"])
usa_df         = usa_df.copy()[keys_use].reset_index()
usa_df["date"] = usa_df.apply(lambda x: pm.epiweek_to_date(pm.Epiweek(x.year, x.mmwr_week)), axis=1)
years_df       = pd.concat([years_df, usa_df])[["year", "mmwr_week", "reporting_area", "total", "date"]].fillna(0)
#############################




years_df["reporting_area"] = years_df["reporting_area"].replace(regions_rename)

rename_usa = {"UNITED STATES": "US", "United States": "US", "Total": "US"}
years_df["reporting_area"] = years_df["reporting_area"].replace(rename_usa)
years_df["total"] = years_df["total"].map(values2int)
years_df["date"]  = years_df.apply(lambda x: pm.epiweek_to_date(pm.Epiweek(x.year, x.mmwr_week)), axis=1)

years_df = years_df.groupby(["date", "year", "mmwr_week", "reporting_area"]).sum().reset_index()
data_df  = years_df.copy()
data_df  = data_df[data_df["reporting_area"] == "US"]
data_df["date"] = pd.to_datetime(data_df["date"])

# all analyses use monthly data
data_df                   = data_df.set_index("date").resample("M").sum().reset_index()[["date", "total"]]
data_df["reporting_area"] = "US"

data_df.to_csv(os.path.join(data_dir, "processed_data_us.csv"), index=False)

#old_data_df = pd.read_csv(os.path.join(data_dir, "old_imd_cases.csv"), parse_dates=["date"])
#fig, ax = plt.subplots(figsize=(10, 5))
#ax.plot(data_df.date, data_df.total, color="black", lw=2, label="New data")
#ax.plot(old_data_df.date, old_data_df.total, color="red", ls=":", lw=2, label="Old data")
#ax.legend()
#ax.set_ylabel("IMD")
#ax.set_xlabel("Date (month)")
#plt.show()
