import requests
import psycopg2
import csv
from sqlalchemy.exc import IntegrityError

base_tmdb_url = 'https://api.themoviedb.org/3/'
base_omdb_url = 'http://www.omdbapi.com/'
tmdb_key = '85dd8aebef9b0ceff51463d49eaa2093'
omdb_api_key = 'c5a65469'

conn = psycopg2.connect(
    host="localhost",
    database="movies",
    user="docker",
    password="docker")

def get_rating(movie_data):
    ratings = movie_data['Ratings']
    final_ratings = {
        'imdb': None,
        'rt': None,
    }
    for rating in ratings:
        if rating['Source'] == 'Internet Movie Database':
            final_ratings['imdb'] = rating['Value'][:-3]
        if rating['Source'] == 'Rotten Tomatoes':
            final_ratings['rt'] = rating['Value'][:-1]

    return final_ratings

def get_tmdb_movie_details(tmdb_id):
    details_url = f'{base_tmdb_url}movie/{tmdb_id}?api_key={tmdb_key}'
    details_result = requests.get(details_url).json()
    return details_result

def get_omdb_data(imdb_id):
    omdb_url = f'{base_omdb_url}?i={imdb_id}&apikey={omdb_api_key}'
    omdb_details = requests.get(omdb_url).json()
    return omdb_details

def get_movie_data(imdb_id):
    find_url = f'{base_tmdb_url}find/{imdb_id}?api_key={tmdb_key}&external_source=imdb_id'
    find_result = requests.get(find_url).json()
    if len(find_result['movie_results']) == 0:
        print(f'failed to find {imdb_id}')
        return None
    movie = find_result['movie_results'][0]
    tmdb_id = movie['id']

    details_result = get_tmdb_movie_details(tmdb_id)

    omdb_details = get_omdb_data

    release_date = details_result['release_date'].split('-')
    release_year = release_date[0]
    release_month = release_date[1]

    final_ratings = get_rating(omdb_details)

    movie_details = {
        'title': details_result['title'],
        'release_year': release_year,
        'release_month': release_month,
        'imdb_id': imdb_id,
        'tmdb_id': tmdb_id,
        'runtime': details_result['runtime'],
        'rating': omdb_details['Rated'],
        'budget': details_result['budget'],
        'imdb_rating': final_ratings['imdb'],
        'rt_rating': final_ratings['rt'],
        }

    return movie_details

def upload_movie(movie):
    sql = """
    INSERT INTO movie(
        movie_title,
        release_year,
        release_month,
        imdb_id,
        tmdb_id,
        runtime,
        rating,
        budget,
        imdb_rating,
        rt_rating)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    insert_values = (
        movie['title'],
        movie['release_year'],
        movie['release_month'],
        movie['imdb_id'],
        movie['tmdb_id'],
        movie['runtime'],
        movie['rating'],
        movie['budget'],
        movie['imdb_rating'],
        movie['rt_rating'],
        )
    cursor = conn.cursor()
    try:
        cursor.execute(sql, insert_values)
    except IntegrityError as ex:
        print(f'{imdb_id} already exist')
    except Exception as ex:
        print(f'{imdb_id} failed to upload')
    finally:
        conn.commit()
        cursor.close()

def actor_exist(actor):
    sql = """SELECT tmdb_id FROM actor WHERE tmdb_id=%s"""
    filter = (actor['tmdb_id'],)
    cursor = conn.cursor()
    cursor.execute(sql, filter)
    return_value = cursor.fetchone() is not None
    cursor.close()
    return return_value

def upload_actor(actor, movie_id):
    sql_actor = """
    INSERT INTO actor(
        actor_performance,
        tmdb_id,
        actor_name)
        VALUES(%s, %s, %s)
        RETURNING id;
    """
    sql_movie_actor = """
        INSERT INTO movie_actor(movie_id, actor_id)
        VALUES (%s, %s);
    """
    actor_insert_values = (
        actor['rating'],
        actor['tmdb_id'],
        actor['name']
        )
    cursor = conn.cursor()
    try:
        cursor.execute(sql_actor, actor_insert_values)
        actor_id = cursor.fetchone()[0]
        movie_actor_insert_values = (
            movie_id,
            actor_id
        )
        cursor.execute(sql_movie_actor, movie_actor_insert_values)
        conn.commit()
    except IntegrityError as ex:
        print(f'{actor["name"]} already exist')
    except Exception as ex:
        print(f'{actor["name"]} failed to upload')
    finally:
        cursor.close()


def get_actor_rating(actor):
    actor_credit_url = f'{base_tmdb_url}person/{actor["tmdb_id"]}/movie_credits?api_key={tmdb_key}'
    actor_credit_result = requests.get(actor_credit_url).json()
    if 'success' in actor_credit_result and not actor_credit_result['success']:
        return None
    # get most popular movies
    actor_movies = sorted(
        actor_credit_result['cast'],
        key=lambda x: x['vote_count'],
        reverse=True)
    counter = 0
    found_divider = 0
    rating_sum = 0
    while counter < 10 and counter < len(actor_movies):
        current_movie = actor_movies[counter]
        tmdb_id = current_movie['id']
        movie_details =  get_tmdb_movie_details(tmdb_id)
        imdb_id = movie_details['imdb_id']
        if imdb_id != None:
            omdb_data = get_omdb_data(imdb_id)
            if omdb_data['Response'] == 'True':
                ratings = get_rating(omdb_data)
                if ratings['imdb'] != None:
                    rating_sum += float(ratings['imdb'])
                    found_divider += 1
        counter += 1
    if found_divider > 0:
        return rating_sum / found_divider
    else:
        return None

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

def get_genres(tmdb_id):
    movie_details = get_tmdb_movie_details(tmdb_id)
    genres = movie_details['genres']
    all_genres = []
    for genre in genres:
        all_genres.append(genre['name'].lower())
    all_genres.sort()
    return all_genres

def genre_exist(genres):
    sql = """SELECT id, genre FROM genre WHERE genre=%s"""
    filter = (str(genres),)
    with conn.cursor() as cursor:
        cursor.execute(sql, filter)
        return_value = cursor.fetchone()
        return return_value

def store_new_genres(genres, movie_id):
    sql_genre = """
    INSERT INTO genre(
        genre)
        VALUES(%s)
        RETURNING id;
    """
    sql_movie_genre = """
        INSERT INTO movie_genre(movie_id, genre_id)
        VALUES (%s, %s);
    """
    genre_insert_values = (str(genres),)
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql_genre, genre_insert_values)
            genre_id = cursor.fetchone()[0]
            movie_genre_insert_values = (
                movie_id,
                genre_id
            )
            cursor.execute(sql_movie_genre, movie_genre_insert_values)
            conn.commit()
        except IntegrityError as ex:
            print(f'{genres} already exist')
        except Exception as ex:
            print(f'{genres} failed to upload')
            conn.rollback()

def insert_existing_genre(genre_id, movie_id):
    try:
        sql_movie_genre = """
            INSERT INTO movie_genre(movie_id, genre_id)
            VALUES (%s, %s);
        """
        movie_genre_insert_values = (
            movie_id,
            genre_id
        )
        with conn.cursor() as cursor:
                cursor.execute(sql_movie_genre, movie_genre_insert_values)
                conn.commit()
    except IntegrityError as ex:
        print(f'{genre_id} already exist')
    except Exception as ex:
        print(f'{genre_id} failed to upload')
        conn.rollback()


all_movies_in_db = get_movie_list()

for movie in all_movies_in_db:
    print(f'Getting genre for {movie[2]}')
    genres = get_genres(movie[1])
    genre_existing = genre_exist(genres)
    if genre_existing == None:
        store_new_genres(genres, movie[0])
    else:
        insert_existing_genre(genre_existing[0], movie[0])





# for movie in all_movies_in_db:
#     print(f'Getting movie data for {movie[2]}')
#     movie_actors = get_actor_list(movie[1])
#     for actor in movie_actors:
#         print(f'getting actor data for {actor["name"]}')
#         if actor_exist(actor):
#             print(f'{actor["name"]} exists')
#             continue
#         actor_rating = get_actor_rating(actor)
#         if actor_rating == None:
#             continue
#         actor['rating'] = actor_rating
#         upload_actor(actor, movie[0])



# count = 0
# with open('imdb_movies.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter='|')
#     for row in csv_reader:
#         imdb_id = row[1].strip()
#         movie_data = get_movie_data(imdb_id)
#         if movie_data == None:
#             continue
#         upload_movie(movie_data)
#         print(count)
#         count += 1