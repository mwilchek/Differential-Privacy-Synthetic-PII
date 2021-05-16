import pandas as pd
import numpy as np
import re
from tqdm import tqdm

df = pd.read_csv(r'Data/fake_pii_data.csv')

df['origin_id'] = df['origin_id'].astype(str)
df['destination_id'] = df['destination_id'].astype(str)
df['departure_date'] = df['departure_date'].astype(np.datetime64)
df['arrival_date'] = df['arrival_date'].astype(np.datetime64)

df['gender'].replace('unknown', 'male', inplace=True)
df['gender'].replace('mostly_male', 'male', inplace=True)
df['gender'].replace('mostly_female', 'female', inplace=True)

df['person_name'].replace('Dr\. ', '', inplace=True, regex=True)
df['person_name'].replace('Ing\. ', '', inplace=True, regex=True)
df['person_name'].replace('Lic\. ', '', inplace=True, regex=True)
df['person_name'].replace('Mtro\. ', '', inplace=True, regex=True)
df['person_name'].replace('Sr\(a\)\. ', '', inplace=True, regex=True)

df['origin_address'] = ""
df['origin_city'] = ""
df['origin_state_province'] = ""
df['origin_zip'] = ""


def formatAddress(full_address):
    chunks = re.split('\n', full_address)
    address = chunks[0]
    local = re.split(',', chunks[1])
    city = local[0]
    area = re.split(' ', local[1])
    state_province = area[1]
    zip = area[2]

    return address, city, state_province, zip


for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    address, city, state_province, zip = formatAddress(row['origin'])
    df.loc[index, 'origin_address'] = address
    df.loc[index, 'origin_city'] = city
    df.loc[index, 'origin_state_province'] = state_province
    df.loc[index, 'origin_zip'] = zip

df['destination_address'] = ""
df['destination_city'] = ""
df['destination_state_province'] = ""
df['destination_zip'] = ""

# Drop Military and PO Box addresses
df = df[df["destination"].str.contains("Box") == False]
df = df[df["destination"].str.contains("APO") == False]
df = df[df["destination"].str.contains("FPO") == False]

for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    address, city, state_province, zip = formatAddress(row['destination'])
    df.loc[index, 'destination_address'] = address
    df.loc[index, 'destination_city'] = city
    df.loc[index, 'destination_state_province'] = state_province
    df.loc[index, 'destination_zip'] = zip

df['departure_year'] = pd.DatetimeIndex(df['departure_date']).year
df['departure_year'] = df['departure_year'].astype('string')

df = df[['person_name', 'origin_id', 'departure_date', 'origin_address',
         'origin_city', 'origin_state_province', 'origin_zip', 'destination_id', 'arrival_date',
         'destination_address', 'destination_city', 'destination_state_province', 'destination_zip',
         'trip_length', 'date_of_birth', 'age_at_arrival', 'departure_year', 'place_of_birth', 'gender', 'Season',
         'AgeBin', 'TripLengthBin']]

df.to_csv('Data/fake_pii_data_clean.csv', index=False)
df.shape

# Get current distro by country/year
test = df.groupby('departure_year')['Season'].apply(lambda x: x.value_counts())
