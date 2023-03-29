# Inference of transmission dynamics and retrospective forecast of invasive meningococcal disease.
Authors: Jaime Cascante Vega<sup>1</sup>, Marta Galanti<sup>1</sup>, Katharina Schley<sup>2</sup>, Sen Pei<sup>1</sup>, Jeffrey Shaman<sup>1,3</sup>

Affiliations:
1. Department of Environmental Health Sciences, Mailman School of Public Health, Columbia University, New York, NY, USA.
2. Pfizer Pharma GmbH, Berlin, Germany
3. Columbia Climate School, Columbia University, New York, NY, USA.


## Replicating the results in the manuscript

### Versions and package requirements


### 1.1 Download IMD CDC data from wonder app
All the data is available publicly in the [CDC Wonder App](https://wonder.cdc.gov). The CDC stores data per epi week per year, the urls to the tables for Meningococcal disease are in the script `analyses/url_cdc.py`. For downloading the data run the script below - the raw data per year will be stored in the directory `data/raw_data/xxxx`, where xxxx indicated the year.

```
python download_cdc.py
```

### 1.2 Prepare data
We work with the US level incident case count data. The next file create a monthly US level IMD case counts and saves the file in `data/raw_data/processed_data_us.csv`

```
python prepare_data.py
```

### 1.3 Time series analyses
Just looking at the time series it looks like there's a seasonality, and also there're substantial references pointing different explanation to this. We investigating the seasonal patterns using Local Wavelet Power Spectrum (LWPS). The notebook `analyses/TimeSeriesAnalyses.ipynb`...