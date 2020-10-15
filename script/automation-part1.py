#!/usr/bin/env python3

# importing libraries
import pandas as pd
from datetime import datetime, timedelta

########################################################################
## World
########################################################################

# getting the data
today = datetime.strftime(datetime.today(),'%Y-%m-%d')

url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-'
covid_countries = pd.read_excel(url+today+'.xlsx')


# preparing dataframe

# renaming columns
covid_countries = covid_countries.rename(columns={'countriesAndTerritories': 'countries',
                                                  'countryterritoryCode': 'countryCode',
                                                  'continentExp': 'continent'})

# getting important columns
covid_countries = covid_countries[['dateRep', 'day', 'month', 'year',
                                   'geoId', 'countries', 'countryCode', 'continent',
                                   'cases', 'deaths']]

# creating a datatime
covid_countries['datetime'] = pd.to_datetime(covid_countries[['year', 'month', 'day']])

# selecting and reordering columns
covid_countries = covid_countries[['dateRep', 'datetime',
                                   'geoId', 'countries', 'countryCode', 'continent',
                                   'cases', 'deaths']]

# creating a cases_at
covid_countries['cases_at'] = covid_countries['datetime'] - timedelta(days=1)

covid_countries = covid_countries[['dateRep', 'datetime', 'cases_at',
                                   'geoId', 'countries', 'countryCode', 'continent',
                                   'cases', 'deaths']]

# removing comman from countries
countries_no_comman_and_underscore = []

for country in covid_countries['countries']:
    country = country.replace(',', '')
    country = country.replace('_', ' ')
    countries_no_comman_and_underscore.append(country)

countries_no_comman_and_underscore = pd.DataFrame(countries_no_comman_and_underscore, columns=['countries'])

covid_countries = covid_countries.merge(countries_no_comman_and_underscore, left_index=True, right_index=True)

covid_countries = covid_countries.rename(columns={'countries_y': 'countries'})

covid_countries = covid_countries.drop(['countries_x'], axis=1)

covid_countries = covid_countries[['dateRep', 'datetime', 'cases_at',
                                   'geoId', 'countries', 'countryCode', 'continent',
                                   'cases', 'deaths']]

# Correcting country name
covid_countries = covid_countries.replace('Bonaire Saint Eustatius and Saba', 
                                          'Bonaire Sint Eustatius and Saba')

covid_countries = covid_countries.replace('Falkland Islands (Malvinas)',
                                          'Falkland Islands')

# Filling null values
countries_code = pd.read_csv('~/covid-19/source/countries_and_codes.csv', delimiter=',')

countries_code = countries_code.rename(columns={'ISO-3166\nalpha3': 'countryCode',
                                                'fips': 'geoId',
                                                'Country': 'country'})

countries_id_code_null = (covid_countries
                              [covid_countries[['geoId', 'countryCode']].isnull().any(1)]
                              .countries.unique())

countries_id_code_null = pd.DataFrame(countries_id_code_null, columns=['country'])

codes_ids_to_update = countries_code.merge(countries_id_code_null)

codes_ids_to_update = codes_ids_to_update.set_index('country')

covid_countries_set_index_country = covid_countries.set_index('countries')
covid_countries_set_index_country.update(codes_ids_to_update)

covid_countries = covid_countries_set_index_country.reset_index()

# reordering registrations on datetime (from down to up)
covid_countries_reorder = (covid_countries.groupby('countries')
                               .apply(lambda x: x.sort_values('datetime', ascending=True))
                               .reset_index(drop=True))

# creating a cumsum columns
covid_countries_reorder[['cases_cumsum', 'deaths_cumsum']] = (covid_countries_reorder
                                                                  .groupby('countries')
                                                                  .cumsum())

# adding case_ordinalDay
covid_countries_reorder = (covid_countries_reorder
                               .drop(covid_countries_reorder
                                     [(covid_countries_reorder.cases_cumsum == 0)].index))

covid_countries_reorder['case_ordinalDay'] = (covid_countries_reorder
                                                  .groupby('countries')['cases_at']
                                                  .diff()
                                                  .dt.days.fillna(0).astype(int))

covid_countries_reorder[['case_ordinalDay']] = (covid_countries_reorder
                                                  .groupby('countries')['case_ordinalDay']
                                                  .cumsum()+1)

covid_countries = covid_countries_reorder[['dateRep', 'datetime', 'cases_at', 'case_ordinalDay',
                                           'geoId', 'countries', 'countryCode', 'continent',
                                           'cases', 'deaths', 'cases_cumsum', 'deaths_cumsum']]

# comparing old and new dataset to get update information
columns_name = ['dateRep', 'datetime', 'cases_at', 'case_ordinalDay', 'geoId',
                'countries', 'countryCode', 'continent', 'cases', 
                'deaths', 'cases_cumsum', 'deaths_cumsum']

covid_countries_old = pd.read_csv('/home/gtrindadi/covid-19/data/covid-19.csv', names=columns_name)

covid_countries_old['dateRep'] = pd.to_datetime(covid_countries_old['dateRep'])
covid_countries_old['datetime'] = pd.to_datetime(covid_countries_old['datetime'])
covid_countries_old['cases_at'] = pd.to_datetime(covid_countries_old['cases_at'])

new_data = pd.concat([covid_countries_old, covid_countries]).drop_duplicates(keep=False)

data_insert = new_data.drop_duplicates(subset=['dateRep', 'datetime', 'case_ordinalDay', 
                                               'countries', 'continent'], 
                                       keep=False)

data_update = pd.concat([data_insert, new_data]).drop_duplicates(keep=False)

data_update = data_update.drop_duplicates(['dateRep', 'datetime', 'cases_at', 'case_ordinalDay',
                                           'geoId', 'countries', 'countryCode', 'continent'],
                                          keep='last')

# dataframe to csv
covid_countries.to_csv(r'/home/gtrindadi/covid-19/data/covid-19.csv', index=False, header=False)

# getting the today and update data
covid_today = covid_countries[covid_countries.datetime == today]
covid_today.to_csv(r'/home/gtrindadi/covid-19/data/covid-19-today.csv', index=False, header=False)

data_update.to_csv(r'/home/gtrindadi/covid-19/data/covid-19-update.csv', index=False, header=False)

data_insert = data_insert[data_insert.datetime != today]
data_insert.to_csv(r'/home/gtrindadi/covid-19/data/covid-19-insert.csv', index=False, header=False)



########################################################################
## Brazil
########################################################################
import pandas as pd
from datetime import datetime, timedelta
import requests
import io
import gzip

# getting the data
url = 'https://data.brasil.io/dataset/covid19/caso.csv.gz'
response = requests.get(url)
bytes_io = io.BytesIO(response.content)
with gzip.open(bytes_io, 'rt') as read_file:
    covid_bra = pd.read_csv(read_file)


# preparing the dataframe

# Converting date column to datetime type
covid_bra['date'] = pd.to_datetime(covid_bra['date'])

# Selecting important columns
covid_bra = covid_bra[['date', 'state', 'city', 'place_type', 
                      'confirmed', 'deaths', 'order_for_place']]

# Separating states and cities
covid_bra_states = covid_bra[covid_bra.place_type == 'state']

covid_bra_states = covid_bra_states.drop(columns='city')

#covid_bra_cities = covid_bra[covid_bra.place_type == 'city']

# Reordering the dataframes
covid_bra_states = (covid_bra_states.groupby('state')
                        .apply(lambda x: x.sort_values('date', ascending=True))
                        .reset_index(drop=True))

# Creating diff columns in covid_bra_states
covid_bra_states['cases_per_day'] = covid_bra_states.groupby('state')['confirmed'].diff()
covid_bra_states['deaths_per_day'] = covid_bra_states.groupby('state')['deaths'].diff()

first_cases = covid_bra_states.groupby('state')[['order_for_place', 'confirmed', 'deaths']].min()
first_cases = (first_cases.rename(columns={'confirmed': 'cases_per_day', 
                                           'deaths': 'deaths_per_day'})
                   .reset_index()
                   .set_index(['state','order_for_place']))

covid_bra_states_set_index = covid_bra_states.set_index(['state','order_for_place'])
covid_bra_states_set_index.update(first_cases)
covid_bra_states = covid_bra_states_set_index.reset_index()

covid_bra_states[['cases_per_day', 'deaths_per_day']] = covid_bra_states[['cases_per_day', 'deaths_per_day']].astype(int)

# Adding state_code column in covid_bra_states
covid_bra_states['state_code'] = 'BR-' +  covid_bra_states['state'].astype(str)

# Creating csv files with prepared dataset
covid_bra.to_csv(r'~/covid-19/data/covid-19-bra.csv', index=False, header=False)
covid_bra_states.to_csv(r'~/covid-19/data/covid-19-bra-states.csv', index=False, header=False)
#covid_bra_cities.to_csv(r'~/covid-19/data/covid-19-bra-cities.csv', index=False, header=False)

yesterday = datetime.strftime(datetime.today() - timedelta(1),'%Y-%m-%d')
covid_bra[covid_bra.date == yesterday].to_csv(r'~/covid-19/data/covid-19-bra-today.csv', 
                                          index=False, header=False)
(covid_bra_states[covid_bra_states.date == yesterday]
     .to_csv(r'~/covid-19/data/covid-19-bra-states-today.csv', 
             index=False, header=False))