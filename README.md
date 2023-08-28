# Inference of transmission dynamics and retrospective forecast of invasive meningococcal disease.
Authors: Jaime Cascante Vega<sup>1</sup>, Marta Galanti<sup>1</sup>, Katharina Schley<sup>2</sup>, Sen Pei<sup>1</sup>, Jeffrey Shaman<sup>1,3</sup>

Affiliations:
1. Department of Environmental Health Sciences, Mailman School of Public Health, Columbia University, New York, NY, USA.
2. Pfizer Pharma GmbH, Berlin, Germany
3. Columbia Climate School, Columbia University, New York, NY, USA.


## Replicating the results in the manuscript

### Versions and package requirements


### Download IMD CDC data from wonder app
All the data is available publicly in the [CDC Wonder App](https://wonder.cdc.gov). The CDC stores data per epi week per year, the urls to the tables for Meningococcal disease are in the script `analyses/url_cdc.py`. For downloading the data run the script below - the raw data per year will be stored in the directory `data/raw_data/xxxx`, where xxxx indicated the year.

```
python download_cdc.py
```

### Prepare data
We work with the US level incident case count data. The next file create a monthly US level IMD case counts and saves the file in `data/raw_data/processed_data_us.csv`.

```
python prepare_data.py
```

### Time series analysis
Looking at the time series it looks like there's a seasonality and also there're substantial references pointing different explanation to this. We investigated the seasonal patterns with Local Wavelet Power Spectrum (LWPS). The notebook `analyses/TimeSeriesAnalyses.ipynb` use this methods on the detrended IMD time series to produce a Fourier decomposition in time.

### ARIMA and SARIMA
We build ARIMA and SARIMA models to forecast previous IMD incidence. The code can be found in the notebook `analyses/arima.ipynb` and `analyses/sarima.ipynb`.

### Dynamical models
We used 3 different versions of a same underlying mechanistic transmission model. Each model represent one hypothesis of a different seasonality, as indicated in the main manuscript. After the first round of reviews we included birth and death dynamics. Each model code, as well as data assimilation with an EAKF and point parameter estimates with an IF-EAKF can be found in: `analyses/BD_Model1.ipynb`, `analyses/BD_Model2.ipynb` and `analyses/BD_Model3.ipynb`.

### Evaluate models accuracy
We use the scores indicated in the main text. The python functions to score the models are in the file `analyses/utils/utils_eval.py`. The notebook `analyses/EvalModels.ipynb` compile .csv files of each model performance.

### Multi-Model Ensemble (MME)
We used the expectation maximization algorithm with different settings (main text) to train a MME, as well as a equally weighted (across models) ensemble. Code can be found in `analyses/CreateMME_BD.ipynb`.

### Evaluate MME accuracy
The python functions to score the models are in the file `analyses/utils/utils_eval.py`. The notebook `analyses/EvalEnsembles_BD.ipynb` compile .csv files of each MME performance.
