import requests

base_tmdb_url = 'https://api.themoviedb.org/3/'
base_omdb_url = 'http://www.omdbapi.com/'
tmdb_api_key = '85dd8aebef9b0ceff51463d49eaa2093'
omdb_api_key = '28ab5b4c'

# search for movie and obtaim tmdb id
search_url = f'{base_tmdb_url}search/movie?api_key={tmdb_api_key}&language=en-US&query=fight%20club&page=1&include_adult=false&year=1999'
result = requests.get(search_url).json()
print(result['results'][0]['id']) # 550 is id for fight club

# get details from tmdb id
movie_details_url = f'{base_tmdb_url}movie/550?api_key={tmdb_api_key}'
result = requests.get(movie_details_url).json()
print(result)

omdb_title_search = f'{base_omdb_url}?t=fight+club&apikey={omdb_api_key}'
# omdb_title_search = f'http://www.omdbapi.com/?i=tt3896198&apikey=28ab5b4c'
result = requests.get(omdb_title_search).json()
print(result)