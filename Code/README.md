The movies_genres_csv.py downloads and transforms the IMDB data from https://datasets.imdbws.com/ to generate two datasets.

For the "movies.csv" archive it is used the 'basics', 'ratings' and 'crew' raw data from IMDB. 
The movies are filtered from 'basics' and the columns ['tconst', 'year', 'runTimeminutes', 'isAdult', 'genres', 'originalTitle', primaryTitle'] are obtained.

From 'ratings' de columns ['averageRating', 'numVotes'] are obtained and the 'basics' and 'ratings' datasets are merged with a left-join using the unique 
identifier 'tconst' on both tables. Creating the "mr_df" dataset

The 'crew' dataset contains the columns ['tconst', 'directors' ,writers'] and it is used to find the duplicates values, according with all of the columns resulting 
from the merge of "mr_df" and 'crew' except for the 'tconst' column.

The weightedRating variable is calculated in the following way:

The 0.90 percentile from number of votes (m) and the mean of averageRating (C) are calculated. The following formula gives a rating based on how many number 
of votes the title had. The closer is the number of votes to the 0.90 percentile, the less is the difference between weightedRating and averageRating.

df["weightedRating"] = (df["numVotes"] / (df["numVotes"] + m)) * df["averageRating"] + (m / (df["numVotes"] + m)) * C

The resulting movies.csv dataset has the following columns.
One for movies with the columns :
averageRating - the average rating of the movies by number of votes
decade (int) - the decade the movies where release
isAdult (bool) - if the movies are for adults or not
numVotes (int) - number of votes the movies recieve on IMDB
originalTitle (string) - the original title of the movies
primaryTitle (string) - the more popular title / the title used by the filmmakers on promotional materials at the point of release
runtimeMinutes (int) - primary runtime of the title, in minutes 
tconst (string) - unique identifier of the movies titles
weightedRating (float) - average rating weighted by the number of votes
year (int) - the year the movies were released

And one for the genres of the movies with the columns:
tconst - Unique identifier of the movies titles
genres - The genres the movies titles are associated with

The movies_genres_csv.py also exports the 'tconst' column as a csv archive for its later use.

The principals_csv.py extracts the ['tconst','nconst','category'] variables from the 'principals' raw data of IMDB.
It is filtered to only contain records from movies titles. The resulting dataset contains the columns:
tconst (string) - unique identifier of the movies titles
nconst (string) - unique identifier of a person releated to the movie title
category (string) - the category of job that person was in

It also exports the 'nconst' column as a csv archive for its later use.

The names_csv.py extract the names.basics raw data from IMDB.

It explodes the variables 'primaryProfession' and 'knownForTitles' since the records were lists. And it is filetered to conatin only records related 
to movies titles. Generating the dataset with columns:

nconst (string) - alphanumeric unique identifier of the name/person
primaryName (string)– name by which the person is most often credited
birthYear – in YYYY format
deathYear – in YYYY format
primaryProfession (string) - the top-3 professions of the person
knownForTitles (string) – unique identifier of titles the person is known for
