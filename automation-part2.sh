#!/usr/bin/env bash

cd "$(dirname "$0")";


#psql -U gtrindadi -d covid-19 -c "COPY covid_countries FROM '/home/gtrindadi/covid-19/covid-19.csv' DELIMITER ',';"

covid_today_date=$(cut -d, -f2 covid-19-today.csv | head -n 1)
today_is=$(date +"%Y-%m-%d")

if [[  10#$covid_today_date == 10#$today_is ]]
then

    psql -U gtrindadi -d covid-19 -c "COPY covid_countries FROM '/home/gtrindadi/covid-19/covid-19-today.csv' DELIMITER ',';"

else

    echo 'There is no data from today!' $(date '+%F %T') >> logfile-error.csv

fi
