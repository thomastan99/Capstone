# Capstone Project

In this project, we are helping the Asian Institute of Digital Finance (AIDF) Credit Research Initiative (CRI) work on their daily forecasting system. 
This forecasting system aims to generate default probabilities for each listed public firm in major markets.

**Installation**
1. Clone the GitHub repository to your directory of choice and navigate to the repository.
    - `git clone https://github.com/thomastan99/Capstone.git`
    - `cd capstone`
2. Install _virtualenv_ and create a virtual environment.
   - `pip install virtualenv`
   - `virtualenv env`
3. Activate the virtual environment.
   - `source env/bin/activate`
4. Install the required packages.
   - `pip install -r requirements.txt`


**Set up BigQuery:**
1. Create a Google API Console project and enable BigQuery by referencing [this link](https://support.google.com/analytics/answer/3416092?hl=en#zippy=%2Cin-this-article).
2. Create a Google Cloud platform service account and grant that service account owner privileges.
3. Download the JSON file of the service account, rename it to `token.json`, and place the file in the root directory
4. Grant billing for the project by adding a payment method.

**Data Exploration**
we have done data exploration to better understand and visualize our data under data_exploration/analysis.ipynb

**Data Imputation**

Under the folder data_preprocessing, we clean up the data for each individual datasets 
1) For CRI data, run the file CRI_data.ipynb 
    - cri_data will be created in gbq under the dataset capstone
2) For Compustat data, run the file Compustat_data.ipynb
    - compustat_data will be created in gbq under the dataset capstone
3) For yFinance data, run the file yFinance_data.ipynb
    - yfinance_cleaned will be created in gbq under the dataset capstone

**Data Merging**

Under the folder data_preprocessing, we merge the 3 datasets in the file data_merging.ipynb. The merged datasets are reflected as tables under the capstone dataset in GBQ. These tables can be used in the models later on. The 3 tables are named as such:
1) cri_data
2) cri_compustat_data
3) cri_compustat_yfinance_data

**Lightgbm**

We have tried different combinations of dataset for lightgbm model and compare their AUC and PRAUC score 
1) cri data (lightgbm_cri.ipynb)
2) cri + compustat data (lightgbm_cri_compustat.ipynb)
3) cri + compustat + yfinance data (lightgbm_yfinance.ipynb)
4) industry relative ratio (extension from model 3)
- Model 1 yields AUC score of 0.893 and PRAUC score of 0.12
- ***Model 2 yields the best AUC score of 0.971 and PRAUC score of 0.33***
- Model 3 yields AUC score of 0.951 and PRAUC score of 0.11
- Model 4 yields the best AUC score of 0.936 and PRAUC score of 0.06

The final probabilities predicted using model 2 for each time horizon (1month, 3 months, 6 months, 12 months, 24 months, 36 months and 60 months) can be retrieved from gbq, dataset = capstone, table = final_lgbm_output. This is done in the folder nelson-siegel/nelson_siegel.ipynb

**Pycox Discrete**

We used the DeepHit model under this package and evaluated the performance based on AUC. 
AUC score obtained was 0.676, indicating that the model performance is only slightly better than random chance. This can be found in file deephit_single.ipynb.

**Scikit-survival**

We used the Cox Proportional-Hazards (CoxPH) model under this package and evaluated the performance based on C-Index.
C-Index obtained was 0.5, indicating that the model performance was no better than random chance. This can be found in file sksurv.ipynb.

**Lifelines**

We used the Cox Proportional-Hazards (CoxPH) model under this package and evaluated the performance based on AUC, PRAUC and C-Index.
The model yields AUC score of 0.936, PRAUC score of 0.0539 and C-Index of 0.93. This can be found in file lifeline.ipynb.

**Nelson-siegel**  

Uses nelson-siegel-svensson package to interpolate predicted probabilities of default for a company on a specific date. 
1) Ensure that token.json is in the same directory to allow connection to GBQ table.
2) Specify CompNo, year and month for which to plot curve and get a numpy array of the predicted probabilities for this combination
3) Run plot_nelson_siegel with this numpy array as input
