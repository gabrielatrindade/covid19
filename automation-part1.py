#!/usr/bin/env python3

# importing libraries
import pandas as pd
from datetime import datetime, timedelta

# getting the data
today = datetime.strftime(datetime.today(),'%Y-%m-%d')

url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
covid_countries = pd.read_csv(url)

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

# dataframe to csv
covid_countries.to_csv(r'/home/gtrindadi/covid-19/covid-19.csv', index=False, header=False)

# getting the today data
covid_today = covid_countries[covid_countries.datetime == today]
covid_today.to_csv(r'/home/gtrindadi/covid-19/covid-19-today.csv', index=False, header=False)
