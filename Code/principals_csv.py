import pandas as pd
from urllib.request import urlretrieve

principals_url = 'https://datasets.imdbws.com/title.principals.tsv.gz'
urlretrieve(principals_url, 'principals.tsv')
principals_df = pd.read_csv('principals.tsv', compression='gzip', sep='\t', na_values='\\N', 
                           usecols=['tconst', 'nconst', 'category'])
titles_ID =  pd.read_csv(r'path/titles_ID.csv')

principals_df.set_index('tconst', inplace=True)

movies_index = set(principals_df.index).intersection(titles_ID['tconst'])
movies_index = list(movies_index)

principals = principals_df.loc[movies_index].copy()

principals.to_csv(r'path/principals.csv')
names_ID = pd.Series(principals['nconst'].unique())

names_ID.to_csv(r'path/names_ID.csv', index=False)
