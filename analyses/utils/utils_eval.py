
import pandas as pd
import numpy as np


def meanae_df(frcst_df, obs_df):
    """  Mean absolute error

    Args:
        frcst_df: Forecast pd.DataFrame from create_df_response in create_df_response, keys \in [date, median, mean, low_q1, up_q1, low_q2, up_q2, ...]
        obs_df:   Observations pd.DataFrame

    Returns:
        scalar: Mean absolute error \sum_i^N |mean(f_i) - o_i| / N
    """
    frsct = frcst_df["mean"].values
    obs   = obs_df["total"].values

    return np.mean(np.abs(frsct - obs))


def error_df(frcst_df, obs_df):
    """  Mean error

    Args:
        frcst_df: Forecast pd.DataFrame from create_df_response in create_df_response, keys \in [date, median, mean, low_q1, up_q1, low_q2, up_q2, ...]
        obs_df:   Observations pd.DataFrame

    Returns:
        scalar: Mean error \sum_i^N (median(f_i) - o_i) / N
    """
    frsct = frcst_df["median"].values
    obs   = obs_df["total"].values
    return np.mean(frsct - obs)



def interval_score(lowerr, upper, obs, alpha):
    """ Interval Score
        Reference: Evaluating epidemic forecasts in an interval format, Johannes Bracher, Evan L. Ray, Tilmann Gneiting, Nicholas G. Reich, PLOS Comp. Biology 2021
                    https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008618

    Args:
        lowerr: np.array Lower quantile with confidence level alpha
        upper:  np.array Upper quantile with confidence level 1-alpha
        obs:    np.array with observations
        alpha:  Confidence level

    Returns:
        Scalar: Interval score
    """
    iss = (upper-lowerr) + 2/alpha * (lowerr-obs) * (obs<lowerr) + 2/alpha * (obs-upper) * (obs>upper)
    return np.mean(iss)


def wis(frcst_df, obs_df, quantiles=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 97.5], col_eval="total"):
    """ Weighted Interval Score
        Reference: Evaluating epidemic forecasts in an interval format, Johannes Bracher, Evan L. Ray, Tilmann Gneiting, Nicholas G. Reich, PLOS Comp. Biology 2021
                    https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008618

    Args:
        frcst_df: Forecast pd.DataFrame from create_df_response in create_df_response, keys \in [date, median, mean, low_q1, up_q1, low_q2, up_q2, ...]
        obs_df:   Observations pd.DataFrame

    Returns:
        Scalar: Weighted Interval score
    """

    wis_df             = pd.DataFrame(columns=["quantile", "interval_score"])
    wis_df["quantile"] = quantiles
    wis_df             = wis_df.set_index("quantile")
    for q in quantiles:
        loww                            = frcst_df[f"low_{q}"].values
        upp                             = frcst_df[f"up_{q}"].values
        value                           = obs_df[col_eval].values
        wis_df.loc[q]["interval_score"] = interval_score(loww, upp, value, q/100)
        meddian                         = frcst_df["median"]

    K   = len(quantiles)
    wis = 1 / (K + 1/2) * (1/2 * np.mean(np.abs(value - meddian)) + np.sum(np.array(quantiles)/100 * wis_df["interval_score"].values) )
    return wis

def compute_evals(frcst_df, obs_df):
    weekdict = {'1m': 1, '2m': 2, '3m': 3, '4m': 4, '5m': 5, '6m': 6}

    df_response_frct = pd.DataFrame(index=list(weekdict.keys()), columns=['mae', 'error', "wis"])

    for kw in weekdict.keys():
        w                                 = weekdict[kw]
        df_response_frct['mae'].loc[kw]   = meanae_df(frcst_df.iloc[:w], obs_df.iloc[:w])
        df_response_frct['error'].loc[kw] = error_df(frcst_df.iloc[:w], obs_df.iloc[:w])
        df_response_frct['wis'].loc[kw]   = wis(frcst_df.iloc[:w], obs_df.iloc[:w])

    df_response_frct["type"]    = 'imd_incidence'
    df_response_frct.index.name = "eval_horizon"
    return df_response_frct

