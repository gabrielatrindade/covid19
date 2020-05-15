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


# inserting information from previous days
psql -U gtrindadi -d covid-19 -c "COPY covid_countries FROM '/home/gtrindadi/covid-19/data/covid-19-insert.csv' (FORMAT csv);"


# updating changed information
if [[ -s ~/covid-19/data/covid-19-update.csv ]]
then

    psql -U gtrindadi -d covid-19 -f script/update_data.sql

fi