import pandas as pd
import numpy as np
import random
import gc
from datetime import datetime, timedelta

df = pd.read_csv(r'Data\fake_pii_data_clean.csv')

years = [2016, 2017, 2018, 2019]
new_data = pd.DataFrame(columns=df.columns)


def subtract_years(dt, years):
    try:
        dt = dt.replace(year=dt.year-years)
    except ValueError:
        dt = dt.replace(year=dt.year-years, day=dt.day-1)
    return dt


for year_data in years:
    df_year = df[(df['departure_year'] == year_data)]
    print("Number of records for " + str(year_data) + " is " + str(df_year.shape[0]))
    print("Splitting subsetted data into following Percentages...")

    # 1-25% (0 to 9 years 25%) #######################################################################################
    sub1 = df_year[(df_year.index > np.percentile(df_year.index, 1)) &
                   (df_year.index <= np.percentile(df_year.index, 25))]  # Get the first 25% records to change
    print("25% data is: " + str(sub1.shape[0]) + " records.")
    for ind_1, row_1 in sub1.iterrows():
        sub1.at[ind_1, 'age_at_arrival'] = random.randint(6, 9)
        arrival_date = sub1.loc[ind_1, 'arrival_date']
        date_time_obj = datetime.strptime(arrival_date, '%Y-%m-%d')
        sub1.at[ind_1, 'date_of_birth'] = subtract_years(date_time_obj, sub1.loc[ind_1, 'age_at_arrival'])

    # 25-48% (10 to 19 years 23%) ####################################################################################
    sub2 = df_year[(df_year.index > np.percentile(df_year.index, 25)) &
                   (df_year.index <= np.percentile(df_year.index, 48))]  # Get the next 23% records to change
    print("23% data is: " + str(sub2.shape[0]) + " records.")
    for ind_2, row_2 in sub2.iterrows():
        sub2.at[ind_2, 'age_at_arrival'] = random.randint(10, 19)
        arrival_date = sub2.loc[ind_2, 'arrival_date']
        date_time_obj = datetime.strptime(arrival_date, '%Y-%m-%d')
        sub2.at[ind_2, 'date_of_birth'] = subtract_years(date_time_obj, sub2.loc[ind_2, 'age_at_arrival'])

    # 48-83% (20 to 39 years 35%) ####################################################################################
    sub3 = df_year[(df_year.index > np.percentile(df_year.index, 48)) &
                   (df_year.index <= np.percentile(df_year.index, 83))]  # Get the next 35% records to change
    print("35% data is: " + str(sub3.shape[0]) + " records.")
    for ind_3, row_3 in sub3.iterrows():
        sub3.at[ind_3, 'age_at_arrival'] = random.randint(20, 39)
        arrival_date = sub3.loc[ind_3, 'arrival_date']
        date_time_obj = datetime.strptime(arrival_date, '%Y-%m-%d')
        sub3.at[ind_3, 'date_of_birth'] = subtract_years(date_time_obj, sub3.loc[ind_3, 'age_at_arrival'])

    # 83-96% (40 to 60 years 13%) ####################################################################################
    sub4 = df_year[(df_year.index > np.percentile(df_year.index, 83)) &
                   (df_year.index <= np.percentile(df_year.index, 96))]  # Get the next 13% records to change
    print("13% data is: " + str(sub4.shape[0]) + " records.")
    for ind_4, row_4 in sub4.iterrows():
        sub4.at[ind_4, 'age_at_arrival'] = random.randint(40, 59)
        arrival_date = sub4.loc[ind_4, 'arrival_date']
        date_time_obj = datetime.strptime(arrival_date, '%Y-%m-%d')
        sub4.at[ind_4, 'date_of_birth'] = subtract_years(date_time_obj, sub4.loc[ind_4, 'age_at_arrival'])

    # 96-100% ( 60 years and over 4%) ################################################################################
    sub5 = df_year[(df_year.index > np.percentile(df_year.index, 96)) &
                   (df_year.index <= np.percentile(df_year.index, 100))]  # Get the final 4% records to change
    print("4% data is: " + str(sub5.shape[0]) + " records.")
    for ind_5, row_5 in sub5.iterrows():
        sub5.at[ind_5, 'age_at_arrival'] = random.randint(60, 70)
        arrival_date = sub5.loc[ind_5, 'arrival_date']
        date_time_obj = datetime.strptime(arrival_date, '%Y-%m-%d')
        sub5.at[ind_5, 'date_of_birth'] = subtract_years(date_time_obj, sub5.loc[ind_5, 'age_at_arrival'])

    # Merge all the updated records to a master set
    frames = [sub1, sub2, sub3, sub4, sub5]
    updated_frame = pd.concat(frames)
    new_data = new_data.append(updated_frame, ignore_index=True)

    # Clean memory
    del sub1, sub2, sub3, sub4, sub5, updated_frame
    gc.collect()

    # Save a benchmark file if script takes too long
    print("Data updated for " + str(year_data))
    new_data.to_csv('Data/benchmark_updated_data.csv', index=False)

# Update final data with latest Bins
new_data['AgeBin'] = pd.cut(new_data['age_at_arrival'], [0, 10, 20, 40, 60, 85],
                            labels=['0-9', '10-19', '20-39', '40-59', '60+'])
new_data.to_csv('Data/fake_pii_data_clean.csv', index=False)
