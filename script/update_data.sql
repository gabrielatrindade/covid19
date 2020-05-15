CREATE TEMP TABLE tmp_x
(
    date_rep VARCHAR(255),
    rep_at DATE NOT NULL,
    cases_at DATE NOT NULL,
    case_ordinal_day INTEGER NOT NULL,
    geo_id VARCHAR(255), --NOT NULL,
    countries VARCHAR(255) NOT NULL,
    country_code VARCHAR(255), --NOT NULL,
    continent VARCHAR(255) NOT NULL,
    cases INTEGER NOT NULL,
    deaths INTEGER NOT NULL,
    cases_cumsum INTEGER NOT NULL,
    deaths_cumsum INTEGER NOT NULL
);

COPY tmp_x FROM '/home/gtrindadi/covid-19/data/covid-19-update.csv' (FORMAT csv);

UPDATE covid_countries
SET 
	date_rep = tmp_x.date_rep,
	rep_at = tmp_x.rep_at,
	cases_at = tmp_x.cases_at,
	cases = tmp_x.cases,
	deaths = tmp_x.deaths,
	cases_cumsum = tmp_x.cases_cumsum,
	deaths_cumsum = tmp_x.deaths_cumsum
    
FROM tmp_x
WHERE
	covid_countries.cases_at = tmp_x.cases_at
	AND covid_countries.case_ordinal_day = tmp_x.case_ordinal_day
	AND covid_countries.geo_id = tmp_x.geo_id
	AND covid_countries.countries = tmp_x.countries
	AND covid_countries.country_code = tmp_x.country_code
	AND covid_countries.continent = tmp_x.continent
;
	
DROP TABLE tmp_x;