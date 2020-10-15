CREATE TABLE covid_countries
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

COPY covid_countries FROM '/home/gtrindadi/covid-19/data/covid-19.csv' (FORMAT csv);

CREATE TABLE covid_bra
(
    cases_at DATE NOT NULL,
    state_br VARCHAR(255) NOT NULL,
    city VARCHAR(255),
    place_type VARCHAR(255) NOT NULL,
    cases INTEGER NOT NULL,
    deaths INTEGER NOT NULL,
    case_ordinal_day INTEGER NOT NULL
);

COPY covid_bra FROM '/home/gtrindadi/covid-19/data/covid-19-bra.csv' (FORMAT csv);

CREATE TABLE covid_bra_state
(
    state_br VARCHAR(255) NOT NULL,
    case_ordinal_day INTEGER NOT NULL,
    cases_at DATE NOT NULL,
    place_type VARCHAR(255) NOT NULL,
    cases INTEGER NOT NULL,
    deaths INTEGER NOT NULL,
    cases_per_day INTEGER NOT NULL,
    deaths_per_day INTEGER NOT NULL,
    state_id VARCHAR(255) NOT NULL
);

COPY covid_bra_state FROM '/home/gtrindadi/covid-19/data/covid-19-bra-states.csv' (FORMAT csv);

CREATE TABLE covid_bra_city
(
    state_br VARCHAR(255) NOT NULL,
    city VARCHAR(255),
    case_ordinal_day INTEGER NOT NULL,
    cases_at DATE NOT NULL,
    place_type VARCHAR(255) NOT NULL,
    cases INTEGER NOT NULL,
    deaths INTEGER NOT NULL,
    cases_per_day INTEGER NOT NULL,
    deaths_per_day INTEGER NOT NULL
);

COPY covid_bra_city FROM '/home/gtrindadi/covid-19/data/covid-19-bra-cities.csv' (FORMAT csv);