CREATE TABLE IF NOT EXISTS movie (
   id serial PRIMARY KEY,
   movie_title varchar(100) NOT NULL,
   release_year int NOT NULL,
   release_month int NOT NULL,
   imdb_id varchar(20) UNIQUE NOT NULL,
   tmdb_id INT NOT NULL,
   runtime int NOT NULL,
   rating varchar(20),
   budget decimal,
   imdb_rating decimal,
   rt_rating decimal,
   genre_id varchar(200),
   FOREIGN KEY (genre_id) REFERENCES genre(id)
);

CREATE TABLE IF NOT EXISTS actor (
   id serial PRIMARY KEY,
   tmdb_id int UNIQUE NOT NULL,
   actor_name varchar(150),
   actor_performance decimal NOT NULL
);

CREATE TABLE IF NOT EXISTS genre (
    id serial PRIMARY KEY,
    genre varchar(200)
);

CREATE TABLE IF NOT EXISTS movie_actor (
  movie_id INT NOT NULL,
  actor_id INT NOT NULL,
  PRIMARY KEY (movie_id, actor_id),
  FOREIGN KEY (movie_id)
      REFERENCES movie (id),
  FOREIGN KEY (actor_id)
      REFERENCES actor (id)
);

CREATE TABLE IF NOT EXISTS movie_genre (
  movie_id INT NOT NULL,
  genre_id INT NOT NULL,
  PRIMARY KEY (movie_id, genre_id),
  FOREIGN KEY (movie_id)
      REFERENCES movie (id),
  FOREIGN KEY (genre_id)
      REFERENCES genre (id)
);