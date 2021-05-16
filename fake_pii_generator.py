import datetime
import random
import os
import pandas as pd
import gender_guesser.detector as gg
from tqdm import tqdm
from faker import Faker

file = r'Data\bulk_data_request.csv'
output_name = 'fake_pii_data.csv'

# ----------------------------------------- Core Functions -------------------------------------------------------------
fake_mexico = Faker('es_MX')
fake_US = Faker('en_US')


def season_of_date(date):
    year = str(date.year)
    seasons = {'Spring': pd.date_range(start='21/03/' + year, end='20/06/' + year),
               'Summer': pd.date_range(start='21/06/' + year, end='22/09/' + year),
               'Autumn': pd.date_range(start='23/09/' + year, end='20/12/' + year)}
    if date in seasons['Spring']:
        return 'Spring'
    if date in seasons['Summer']:
        return 'Summer'
    if date in seasons['Autumn']:
        return 'Autumn'
    else:
        return 'Winter'


def get_fake_pii_data(file, output_name):
    data_request = pd.read_csv(file)

    try:
        # Read benchmark data if it exists
        df = pd.read_csv('\\Data\\' + output_name)
    except FileNotFoundError:
        columns = ['person_name', 'origin_id', 'departure_date', 'origin', 'destination_id', 'arrival_date',
                   'destination', 'trip_length', 'date_of_birth', 'age_at_arrival', 'place_of_birth', 'gender']
        df = pd.DataFrame(columns=columns)

    for index, row in data_request.iterrows():
        pob = row['Country']
        year = int(row['Year'])
        num_records = int(row['Records'])

        for trip in tqdm(range(0, num_records)):
            # Identity ID
            person_name = fake_mexico.name()

            # Trip Origin ID
            trip_origin_id = random.randint(1000000000, 9999999999)

            # Trip Departure Date
            start_date = datetime.date(year=year, month=1, day=1)
            end_date = datetime.date(year=year, month=12, day=30)
            departure_date = fake_mexico.date_between(start_date=start_date, end_date=end_date)

            # Trip Origin Location
            origin = fake_mexico.address()

            # Trip Destination ID
            trip_destination_id = random.randint(1000000000, 9999999999)

            # Trip Arrival Date
            days = random.randrange(10, 51, 1)
            arrival_date = departure_date + datetime.timedelta(days)

            # Trip Destination Location
            destination = fake_US.address()

            # Calculate number of days from Departure to Arrival
            tripLength = arrival_date - departure_date
            tripLength = tripLength.days

            # Fake Birth date of Person
            dob = fake_US.date_of_birth(tzinfo=None, minimum_age=8, maximum_age=80)

            # Calculate age when arrival occurred
            age_at_arrival = arrival_date - dob
            age_at_arrival = age_at_arrival / datetime.timedelta(days=365)
            age_at_arrival = int(age_at_arrival)

            # Place of Birth
            placeOfBirth = pob

            # Get Gender
            d = gg.Detector()
            full_name = person_name.split()
            first_name = full_name[0]
            gender = d.get_gender(first_name)

            new_trip = {'person_name': person_name,
                        'origin_id': trip_origin_id,
                        'departure_date': departure_date,
                        'origin': origin,
                        'destination_id': trip_destination_id,
                        'arrival_date': arrival_date,
                        'destination': destination,
                        'trip_length': tripLength,
                        'date_of_birth': dob,
                        'age_at_arrival': age_at_arrival,
                        'place_of_birth': placeOfBirth,
                        'gender': gender}

            df = df.append(new_trip, ignore_index=True)

        # Get Season of Travel
        try:
            df['arrival_date'] = pd.to_datetime(df['arrival_date'])
            df['Season'] = df['arrival_date'].map(season_of_date)
        except Exception:
            df['Season'] = df['arrival_date'].map(season_of_date)

        # Create Age Bins
        df['AgeBin'] = pd.cut(df['age_at_arrival'], [0, 10, 20, 40, 60, 85],
                              labels=['0-9', '10-19', '20-39', '40-59', '60+'])

        # Create TimeToEncounter Bins
        df['TripLengthBin'] = pd.cut(df['trip_length'], [0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 1000],
                                     labels=['0-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40',
                                             '40-45', '45-50', '50+'])

        output = 'Data/' + output_name

        df.to_csv(output, index=False)
        print("")
        print("Benchmark file made for " + pob + " " + str(year))


# ----------------------------------------- Execute Fake Data Generation -----------------------------------------------
get_fake_pii_data(file, output_name)
print("Data has been made here: " + str(os.getcwd() + '\\Data\\' + output_name))
