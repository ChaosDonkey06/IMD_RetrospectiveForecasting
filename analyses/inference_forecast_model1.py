from matplotlib.dates import date2num, num2date
from matplotlib.colors import ListedColormap
from matplotlib import dates as mdates
from matplotlib.patches import Patch
from matplotlib import pyplot as plt
from matplotlib import ticker


import pandas as pd
import numpy as np
import itertools
import os

import pymmwr as pm

import sys

sys.path.insert(0, '../')

from scipy.stats import truncnorm
from global_config import config

results_dir   = config.get_property('results_dir')
data_dir      = config.get_property('data_dir')

def flat_list(list_of_lists):
    return list(itertools.chain(*list_of_lists))

data_df = pd.read_csv(os.path.join(data_dir, 'processed_data_us.csv'), index_col=0)

def binomial_transition(var, rate, dt=1, num_ensembles=300):
    kb        = np.maximum(1.0 - np.exp(-rate*dt), 0)
    num_ind   = np.random.binomial(list(var), kb )
    if num_ind.shape[-1]!=num_ensembles:
        print("Error transitioning stochastic model")
    return np.squeeze(num_ind)

def imd_model(x, betas, theta, N, dt=1):
    """[summary]

    Args:
        x ([type]):           Dimension of [num_state_variables, num_ensembles]
        betas ([type]):       Dimension of [num_state_variables, num_ensembles]
        pop_pyramid ([type]): Dimension of [num_state_variables, num_ensembles]

    Returns:
        [type]: [description]
    """

    # Infection duration.
    gamma   = 1/15

    # Carriage duration.
    alpha1   = 1/150
    alpha2   = 1/10

    S       = x[0, :] # Susceptible  [1, num_ensembles]
    C       = x[1, :] # Carriers     [1, num_ensembles]
    I       = x[2, :] # Infected     [1, num_ensembles]

    # Force of Infection
    foi =  betas * (C + I) / N

    ############ TRANSITIONS ############
    s2c   =  binomial_transition(S, dt * foi)                # susceptible to colonized with vaccine preventable strain
    c2i   =  binomial_transition(C, dt * alpha2 * theta)     # colonized to infected with vaccine preventable strain
    c2s   =  binomial_transition(C, dt * alpha1 * (1-theta)) # colonized to susceptible due to decolonization
    i2s   =  binomial_transition(I, dt * gamma)              # infected to susceptible due to infection clearance

    S     = S  - s2c  + c2s + i2s
    C     = C  + s2c  - c2i - c2s
    I     = I  + c2i   - i2s
    inc   = c2i

    return np.array([S , C , I , inc])

#######-#######-#######-#######

num_ensembles = 300
population    = 200e6
theta         = 1e-2
beta          = 0.85

num_variables = 4
num_steps     = 365

S0     = np.ones(( num_ensembles)) * population
C0     = np.random.uniform(1e-6, 0.05 / 100, ( num_ensembles))*S0
I0     = np.random.uniform(1e-6, 0.01 / 100, ( num_ensembles))*S0
S0     = S0 - C0 - I0
inc    = np.zeros(( num_ensembles))
x0     = np.array([S0, C0, I0, inc]) # array with initial conditions [num_state_variables, num_age_groups]

x                  = x0

thetas       = theta * np.ones((num_ensembles))
betas        = beta  * np.ones((num_ensembles))

x_all        = np.full((num_variables, num_ensembles, num_steps), np.nan)
x_all[:,:,0] = x0


for t in range(1, num_steps):
    #print(t)
    x_all[:, :, t] = imd_model(x_all[:, :, t-1], betas, theta, N=population)

keys_variables = ["date", "ens_id", "S", "C", "I", "inc"]

result_df           = pd.DataFrame(columns=keys_variables)
result_df["date"]   = flat_list([range(num_steps)] * num_ensembles)
result_df["ens_id"] = flat_list([[idx_ens]*num_steps for idx_ens in range(num_ensembles)])
result_df["S"]      = x_all[0, :, :].flatten()
result_df["C"]      = x_all[1, :, :].flatten()
result_df["I"]      = x_all[2, :, :].flatten()
result_df["inc"]    = x_all[3, :, :].flatten()

mean_df             = result_df.groupby("date").mean().reset_index()

#######-#######-#######-#######

def compute_oev(obs_vec, var_obs=0.2):
    return 1 + (var_obs*obs_vec)**2


def checkbound_params(dict_params_range, params_ens):
    params_update = []
    for idx_p, p in enumerate(dict_params_range.keys()):
        loww = dict_params_range[p][0]
        upp  = dict_params_range[p][1]

        p_ens = params_ens[idx_p, :].copy()

        idx_wrong      = np.where(np.logical_or(p_ens <loww, p_ens > upp))[0]

        idx_wrong_loww = np.where(p_ens < loww)[0]
        idx_wrong_upp  = np.where(p_ens > upp)[0]

        idx_good  = np.where(np.logical_or(p_ens >=loww, p_ens <= upp))[0]

        p_ens[idx_wrong] = np.median(p_ens[idx_good])

        np.put(p_ens, idx_wrong_loww, loww * (1+0.2*np.random.rand( idx_wrong_loww.shape[0])) )
        np.put(p_ens, idx_wrong_upp, upp * (1-0.2*np.random.rand( idx_wrong_upp.shape[0])) )

        params_update.append(p_ens)

    return np.array(params_update)

def checkbound_state_vars(x_state_ens, pop):
    loww = 0
    upp  = pop
    x_state_ens = np.clip(x_state_ens, loww, upp)
    return x_state_ens

# range of parameters
βmin = 0.006
βmax = 0.01

θmin = 0.5e-6
θmax = 1.2e-6

