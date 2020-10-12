# imports
import pandas as pd
import psycopg2

# create db connection to load data
conn = psycopg2.connect(
    host="localhost",
    database="movies",
    user="docker",
    password="docker")

    # load data into dataframe
sql = """SELECT * FROM movie"""
cursor = conn.cursor()
cursor.execute(sql)
movies = cursor.fetchall()
cursor.close()

columns = ['id', 'title', 'release_year', 'release_month', 'imdb_id', 'tmdb_id', 'runtime', 'rating', 'budget', 'imdb_rating', 'rt_rating', 'genre_id']
movie_df = pd.DataFrame(movies, columns =columns)
# load actor data
sql = """
    SELECT a.id, a.actor_performance, a.tmdb_id, a.actor_name, ma.movie_id
        from actor a
    JOIN movie_actor ma
    	ON a.id = ma.actor_id
"""
cursor = conn.cursor()
cursor.execute(sql)
actors = cursor.fetchall()
cursor.close()

columns = ['actor_id', 'actor_performance', 'tmdb_id', 'actor_name', 'movie_id']
actor_df = pd.DataFrame(actors, columns=columns)

movie_df['actor_performance'] = ''
for index, row in movie_df.iterrows():
    movie_id = row['id']
    movie_actors = actor_df.loc[actor_df['movie_id'] == movie_id]
    actor_average_performance = movie_actors['actor_performance'].mean()
    row['actor_performance'] = actor_average_performance