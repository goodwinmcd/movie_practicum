Explanation of all files

1. collect_data.py
- One time script that did the bulk of the work done to collect the necessary data for movies, actors, and genres.
2. create_tables.sql
- Initializes the database and tables used to store the data. Used by the DockerFile to make the db more portable across computers
3. fix_actor.py
- I made a mistake the first time I collected the data for actors. I check if the actor exists and if it does, then I continue the loop. The issue is that I needed to still put an entry in the movie_actor link table to create that link between the movie and actor. This script fixes that so I didn't have to wait the 12 hours for the actor script to run
4. fix_genres
- I originally had a link table for movies and genres. I realized there is a one to one relationship between the two tables and that I didn't need a linking table. This script fixed that issue and allowed me to delete the unnecessary table
5. imdb_movies.csv
- This file was created by imdb scrape. It has a list of movie titles with their corresponding imdb ids.
6. imdb_scrape.py
- This was used to scrape the titles and imdb ids of the 500 most popular movies of each year for the last decade. This list was then used to do api calls to collect the rest of the necessary data from TMDB.
7. model_builder.ipynb
- This is a jupyter file I used to build the models to predict imdb ratings based on the data.
8. test-scrape.py
- POC to make sure I could get needed data from omdb and tmdb