import pandas as pd
from urllib.request import urlretrieve

basics_url = 'https://datasets.imdbws.com/title.basics.tsv.gz'
urlretrieve(basics_url, 'basics.tsv')
basics_df = pd.read_csv('basics.tsv', compression='gzip', sep='\t', na_values='\\N')

mb_df = basics_df[basics_df.titleType == 'movie'].copy()
mb_df.drop('endYear', axis=1, inplace=True)


mb_df['genres'] = mb_df.genres.fillna('unknown')
mb_df['startYear'] = mb_df.startYear.astype('Int64')
mb_df['runtimeMinutes'] = mb_df.runtimeMinutes.astype('float')
mb_df.drop('titleType',axis=1,inplace=True)
mb_df['runtimeMinutes'] = mb_df.runtimeMinutes.astype('Int64')
mb_df['isAdult'] = mb_df.isAdult.astype('bool')

mb_df.rename(columns={'startYear':'year'},inplace=True)

mb_df.reset_index(inplace=True, drop=True)

################################

ratings_url = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
urlretrieve(ratings_url, 'ratings.tsv')
ratings_df = pd.read_csv('ratings.tsv', compression='gzip', sep='\t')

mr_df = mb_df.merge(ratings_df, on='tconst', how='left').copy()

mr_df['decade'] = mr_df['year'].case_when([
    (mr_df.year < 1900, 1800),
    (mr_df.year < 1910, 1900),
    (mr_df.year < 1920, 1910),
    (mr_df.year < 1930, 1920),
    (mr_df.year < 1940, 1930),
    (mr_df.year < 1950, 1940),
    (mr_df.year < 1960, 1950),
    (mr_df.year < 1970, 1960),
    (mr_df.year < 1980, 1970),
    (mr_df.year < 1990, 1980),
    (mr_df.year < 2000, 1990),
    (mr_df.year < 2010, 2000),
    (mr_df.year < 2020, 2010),
    (mr_df.year < 2030, 2020)
])

mr_df['decade'] = mr_df.decade.astype('int')

###############################

crew_url = 'https://datasets.imdbws.com/title.crew.tsv.gz'
urlretrieve(crew_url, 'crew.tsv')
crew_df = pd.read_csv('crew.tsv', compression='gzip', sep='\t', na_values='\\N')

df = mr_df.merge(crew_df, how='left', on='tconst').copy()
df.drop_duplicates(subset=[c for c in df.columns if c != 'tconst'], inplace=True)

C = df["averageRating"].mean()
m = df["numVotes"].quantile(0.90)
df["weightedRating"] = (
    (df["numVotes"] / (df["numVotes"] + m)) * df["averageRating"]
    + (m / (df["numVotes"] + m)) * C
)

df1 = df.copy()
df1['genres'] = df1.genres.str.split(',')
df1 = df1.explode(column=['genres']).copy()
Genres = df1[['tconst','genres']].copy()

df.drop('genres',axis=1,inplace=True)

df.to_csv(r'path/movies.csv', index=False)
Genres.to_csv(r'path/genres.csv', index=False)

titles_ID = df['tconst']

titles_ID.to_csv(r'path/titles_ID.csv', index=False)
