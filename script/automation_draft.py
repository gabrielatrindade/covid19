#!/usr/bin/env python3

import pandas as pd

url = 'https://data.brasil.io/dataset/covid19/caso.csv.gz'
covid_bra = pd.read_csv(url)

covid_bra['state_code'] = 'BR-' +  covid_bra['state'].astype(str)

cols = covid_bra.columns.tolist()
cols = cols[:7] + cols[-1:]
covid_bra = covid_bra[cols]

covid_bra.to_csv(r'~/covid-19/covid-19-bra.csv', index=False, header=False)
