from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/search/title/?title_type=feature&year=2019-01-01,2019-12-31&start=1&ref_=adv_nxt'

movies = []
year = 2009
page_offset = 1

for i in range(10):
    print(f'processing year {year}')
    for j in range(10):
        print(f'processing page {j}')
        url = f'https://www.imdb.com/search/title/?title_type=feature&year={year}-01-01,{year}-12-31&start={page_offset}&ref_=adv_nxt'
        page_data = urlopen(url)
        soup = BeautifulSoup(page_data, "html.parser")
        all_movies_in_list = soup.find_all('div', class_='lister-item-image')
        for movie in all_movies_in_list:
            title = movie.a.img['alt']
            imdb_id = movie.a.img['data-tconst']
            movie = [ title, imdb_id ]
            movies.append(movie)
        page_offset += 50
    page_offset = 1
    year += 1

with open('imdb_movies.csv', 'a') as file:
    for movie in movies:
        file.write(f'{movie[0]}:: {movie[1]}\n')

print('done')

print(movies)