# Differential Privacy Synthetic PII

Differential Privacy Synthetic PII is a set of Python algorithms that enable generation of differential privacy, fully 
synthetic personally identifiable information (PII) data and then impute additional insights based on real data. The 
algorithms enable generation of data which can be distributed easily without revealing private information. A core piece
behind our differential privacy data is the introduction of randomness behind the imputation of certain features while 
not impacting the overall dataset's valid inferences. By introducing randomness to the data generation, differential 
privacy can create deniability behind identifiable features of individuals. 

## Dependencies
- Python (>= 3.8.5)
- NumPy (1.17.0)
- SciPy
- Dython
- MLxtend
- Faker
- Pandas
- gender_guesser
- re
- tqdm
- datetime
- random
- matplotlib

## Setup
A. Create a bulk data request CSV file with the following format (keep column names the same):

| Country | Year | Records |
| ------- | ---- | ------- |
| RUSSIA | 2016 | 457 |
| MEXICO | 2020 | 1102 |
| CHINA | 2018 | 632 |

B. Update line 9 if needed in the script **fake_pii_generator.py** to point to the file made in step A. Then execute 
script.

C.  Clean the differential privacy synthetic PII with the **fake_data_clean.py** script. This script primarily removes 
any person titles (Dr., Ing., Lic., etc.), cleans gender categories, and removes any records with P.O. Box or military 
addresses.

## Impute Insights (Optional)
Due to the introduction of randomness behind many of the PII features, there is a chance the dataset may not have much 
valid inferences. Therefore, adjusting some of the features such as Age or other dates, can create custom context and
insights.  The script **age_update.py** is an example of imputed insights that was adjusted on a real distribution 
dataset by the U.S. Immigration Customs Enforcement Agency (ICE) made available to the public 
[here](https://www.dhs.gov/immigration-statistics/refugees-asylees).    