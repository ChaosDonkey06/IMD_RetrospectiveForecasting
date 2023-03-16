# Inference of transmission dynamics and retrospective forecast of invasive meningococcal disease.
Authors: Jaime Cascante Vega<sup>1</sup>, Marta Galanti<sup>1</sup>, Katharina Schley<sup>2</sup>, Sen Pei<sup>1</sup>, Jeffrey Shaman<sup>1,3</sup>

Affiliations:
1. Department of Environmental Health Sciences, Mailman School of Public Health, Columbia University, New York, NY, USA.
2. Pfizer Pharma GmbH, Berlin, Germany
3. Columbia Climate School, Columbia University, New York, NY, USA.

## Replicating the paper:

### 1.1 Download IMD CDC data from wonder app
All the data is available publicly in the [CDC Wonder App](https://wonder.cdc.gov). The urls are stored to the data per year are in url_cdc.py, you need to run the code in download_cdc.py to download all the data under the specified directory.

```
python download_cdc.py
```

### 1.2 Prepare data
We work with the US level data, so the next file create a monthly US level IMD case counts.
```
python prepare_data.py
```
