# Capstone

**Set up BigQuery:**

1. Create a Google API Console project and enable BigQuery by referencing [this link](https://support.google.com/analytics/answer/3416092?hl=en#zippy=%2Cin-this-article).
2. Create a Google Cloud platform service account and grant that service account owner privileges.
3. Download the JSON file of the service account, rename it to `bigquery_key.json`, and place the file in the **_key_** folder.
4. Grant billing for the project by adding a payment method.

**Data_Imputation**

Under the folder data_preprocessing
1. For CRI data, run the file CRI_data.ipynb 
2. For Compustat data, run the file Compustat_data.ipynb