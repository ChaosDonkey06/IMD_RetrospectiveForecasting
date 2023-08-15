import pandas as pd
import numpy as np

def degenerate_em_weights(dist_cond_likelihood, init_weights=None, obs_weights=None, models_name=None, tol_stop = 1e-13):
    """ Degenerate expectation maximization weights.
        Compute weights to create a posterior distribution averaging over given set of quantiles.

    Args:
        dist_cond_likelihood (_type_): P_k(wi | hi), k in [1, num_models], i in [1, num_quantiles] [K, Q]
        init_weights         (_type_): Naive weights.
        tol_stop             (_type_): _description_. Defaults to 1e-13.
    """

    # Return number of observations and number of models.
    num_obs, num_model = dist_cond_likelihood.shape

    if obs_weights:
        obs_weights = np.array(obs_weights)
        obs_weights = obs_weights / np.sum(obs_weights)
    else:
        # Initialize all weights equally
        obs_weights = np.ones(num_obs) * 1/num_obs

    if init_weights:
        weights = init_weights
    else:
        # Initialize all weights equally
        weights = np.ones((num_obs, num_model)) * 1 / num_model

    lkhds     = weights * dist_cond_likelihood # Likelihoods   | [num_obs, num_models]
    marg_dist = np.sum(lkhds, axis=-1)         # Marginal dist | [num_obs]

    # Average log likelihood across observation space.
    log_lklhd     = np.average(np.log(marg_dist), weights=obs_weights)
    old_log_lklhd = -1000

    while log_lklhd > old_log_lklhd and (log_lklhd-old_log_lklhd >= tol_stop) or ((log_lklhd - old_log_lklhd) / -log_lklhd >= tol_stop):

        old_log_lklhd  = log_lklhd # Save new log-likelihood value.
        weights        = np.divide(lkhds, np.expand_dims(marg_dist, -1))
        weights        = np.average(weights, weights=obs_weights, axis=0) # Recompute weights | [num_models]

        # Recompute likelihoods
        lkhds          = weights * dist_cond_likelihood                     # Likelihoods    | [num_obs, num_models]
        marg_dist      = np.sum(lkhds, axis=-1)                             # Marginal dist  | [num_obs]
        log_lklhd      = np.average(np.log(marg_dist), weights=obs_weights) # Log-likelihood | Scalar

    w_df           = pd.DataFrame(columns=["weigth", "model_name"])
    w_df["weigth"] = weights
    if models_name:
        w_df["model_name"] = models_name
    else:
        w_df["model_name"] = [f"model_{str(i)}" for i in range(len(w_df))]

    return w_df.set_index("model_name")