import pandas as pd
from urllib.request import urlretrieve

name_url = 'https://datasets.imdbws.com/name.basics.tsv.gz'
urlretrieve(name_url, 'name.tsv')
name_df = pd.read_csv('name.tsv', compression='gzip', sep='\t', na_values='\\N')

name_ID = pd.read_csv(r'C:/Users/José Daniel/Documents/IMDB/Data_clean/names_ID.csv')

df = name_df[name_df['nconst'].isin(name_ID['0'])].copy()

df['primaryProfession'] = df.primaryProfession.str.split(',')
df['knownForTitles'] = df.knownForTitles.str.split(',')
                        
df = df.explode('primaryProfession', ignore_index=True).copy()
df = df.explode('knownForTitles', ignore_index=True).copy()

df.to_csv(r'C:/Users/José Daniel/Documents/IMDB/Data_clean/names.csv', index=False)
