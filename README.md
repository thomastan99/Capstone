# Capstone Project

In this project, we are helping the Asian Institute of Digital Finance (AIDF) Credit Research Initiative (CRI) work on their daily forecasting system. 
This forecasting system aims to generate default probabilities for each listed public firm in major markets.

**Set up BigQuery:**
1. Create a Google API Console project and enable BigQuery by referencing [this link](https://support.google.com/analytics/answer/3416092?hl=en#zippy=%2Cin-this-article).
2. Create a Google Cloud platform service account and grant that service account owner privileges.
3. Download the JSON file of the service account, rename it to `token.json`, and place the file in the root directory
4. Grant billing for the project by adding a payment method.

**Data Exploration**
we have done data exploration to better understand visualize our data under data_exploration/analysis.ipynb

**Data Imputation**
Under the folder data_preprocessing, we clean up the data for each individual datasets 
1. For CRI data, run the file CRI_data.ipynb 
2. For Compustat data, run the file Compustat_data.ipynb
3. For yFinance data, run the file yFinance_data.ipynb

**Data Merging**
Under the folder data_preprocessing,
We merge the 3 datasets in the file data_merging.ipynb

**Lightgbm**
We have tried different combinations of dataset for lightgbm model and compare their AUC and PRAUC score 
1) cri data (lightgbm_cri.ipynb)
2) cri + compustat data (lightgbm_cri_compustat.ipynb)
3) cri + compustat + yfinance data (lightgbm_yfinance.ipynb)
Model 2 yields the best AUC score of 0.971 and PRAUC score of 0.3268

**Pycox Discrete**

**Scikit-survival**
We used the Cox Proportional-Hazards (CoxPH) model under this package and evaluated the performance based on C-Index.
C-Index obtained was 0.5, indicating that the model performance was no better than random chance.

**Lifelines**
We used the Cox Proportional-Hazards (CoxPH) model under this package and evaluated the performance based on AUC, PRAUC and C-Index.
The model yields AUC score of 0.936, PRAUC score of 0.0539 and C-Index of 0.93.

**DeepSurv**