# Config file for global variables in python.
# This script reads the variables in Python and makes them available through the function
import pandas as pd
from pathlib import Path
import os


# Loads the configuration file
# Loacation
current_location = Path(os.path.realpath(__file__)).parent
# Loads
try:
    df_config = pd.read_csv(os.path.join(current_location, 'config_file.csv'), index_col = 'name')
    
except FileNotFoundError:
    raise ValueError('The configuration file: "config_file.csv", was not found insise the directory: "global_config/". Please add it')


def get_property(name):

    try:
        return(df_config.loc[name,'value'])

    except KeyError:
        raise ValueError(f'Configuration variable "{name}", was not found. Please add it')
