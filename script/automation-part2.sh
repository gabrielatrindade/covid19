#!/usr/bin/env bash

cd "$(dirname "$0")";

# adding all information
#psql -U gtrindadi -d covid-19 -c "COPY covid_countries FROM '/home/gtrindadi/covid-19/data/covid-19.csv' DELIMITER ',';"


# inserting information on today
covid_today_date=$(cut -d, -f2 ~/covid-19/data/covid-19-today.csv | head -n 1)
today_is=$(date +"%Y-%m-%d")

if [[  10#$covid_today_date == 10#$today_is ]]
then

    psql -U gtrindadi -d covid-19 -c "COPY covid_countries FROM '/home/gtrindadi/covid-19/data/covid-19-today.csv' DELIMITER ',';"

else

    echo 'There is no data from today!' $(date '+%F %T') >> logfile-error.csv
    echo 'No data from today: '$today_is | mutt -s"No data from today" gabizinha_hzs@hotmail.com

fi

# inserting information on today bra
covid_bra_date=$(cut -d, -f1 ~/covid-19/data/covid-19-bra-today.csv | head -n 1)
yesterday_was=$(date +%Y-%m-%d -d "yesterday")

if [[  10#$covid_bra_date == 10#$yesterday_was ]]
then

    psql -U gtrindadi -d covid-19 -c "COPY covid_bra FROM '/home/gtrindadi/covid-19/data/covid-19-bra-today.csv' DELIMITER ',';"
    psql -U gtrindadi -d covid-19 -c "COPY covid_bra_state FROM '/home/gtrindadi/covid-19/data/covid-19-bra-states-today.csv' DELIMITER ',';"

else

    echo 'There is no data from yesterday in BRA!' $(date '+%F %T') >> logfile-error.csv
    echo 'No data from today: '$today_is | mutt -s"No data from today about BRA" gabizinha_hzs@hotmail.com

fi

# inserting information from previous days
psql -U gtrindadi -d covid-19 -c "COPY covid_countries FROM '/home/gtrindadi/covid-19/data/covid-19-insert.csv' (FORMAT csv);"


# updating changed information
if [[ -s ~/covid-19/data/covid-19-update.csv ]]
then

    psql -U gtrindadi -d covid-19 -f update_data.sql

fi