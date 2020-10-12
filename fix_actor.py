import psycopg2
import requests

conn = psycopg2.connect(
    host="localhost",
    database="movies",
    user="docker",
    password="docker")

base_tmdb_url = 'https://api.themoviedb.org/3/'
base_omdb_url = 'http://www.omdbapi.com/'
tmdb_key = '85dd8aebef9b0ceff51463d49eaa2093'
omdb_api_key = 'c5a65469'


def get_movie_list():
    sql = """SELECT id, tmdb_id, movie_title FROM movie"""
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_actor_list(tmdb_id):
    credits_url = f'{base_tmdb_url}movie/{tmdb_id}/credits?api_key={tmdb_key}'
    credits_result = requests.get(credits_url).json()
    counter = 0
    actors = []
    while counter != 5 and counter < len(credits_result['cast']):
        tmdb_actor = credits_result['cast'][counter]
        actor = {
            'tmdb_id': tmdb_actor['id'],
            'name': tmdb_actor['name'],
            'rating': None,
        }
        actors.append(actor)
        counter += 1

    return actors

def get_actor_from_tmdb_id(tmdb_id):
    get_actor_id_sql = """SELECT id, tmdb_id FROM actor WHERE tmdb_id=%s"""
    get_actor_id_values = (tmdb_id,)
    cursor = conn.cursor()
    cursor.execute(get_actor_id_sql, get_actor_id_values)
    actor_data = cursor.fetchone()
    if actor_data == None:
        return None
    actor_id = actor_data[0]
    cursor.close()
    return actor_id

def movie_actor_exists(movie_id, actor_id):
    check_movie_actor_sql = """
        SELECT movie_id, actor_id FROM movie_actor
        WHERE movie_id = %s AND actor_id = %s"""

    cursor = conn.cursor()

    check_movie_actor_values = (movie_id, actor_id)
    cursor.execute(check_movie_actor_sql, check_movie_actor_values)
    result = cursor.fetchone()
    cursor.close()
    return result

def insert_link_table(movie_id, actor_id):
    sql = """INSERT INTO movie_actor(movie_id, actor_id)
        VALUES(%s, %s)"""
    cursor = conn.cursor()
    sql_values = (movie_id, actor_id,)
    cursor.execute(sql, sql_values)
    conn.commit()
    cursor.close()



all_movies = get_movie_list()
for movie in all_movies:
    actors = get_actor_list(movie[1])
    for actor in actors:
        actor_id = get_actor_from_tmdb_id(actor['tmdb_id'])
        if actor_id == None:
            continue
        results = movie_actor_exists(movie[0], actor_id)
        if results == None:
            insert_link_table(movie[0], actor_id)