--
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2 (Debian 11.2-1.pgdg90+1)
-- Dumped by pg_dump version 11.2 (Debian 11.2-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE movies;
--
-- Name: movies; Type: DATABASE; Schema: -; Owner: docker
--

CREATE DATABASE movies WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE movies OWNER TO docker;

\connect movies

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: actor; Type: TABLE; Schema: public; Owner: docker
--

CREATE TABLE public.actor (
    id integer NOT NULL,
    actor_performance numeric NOT NULL,
    tmdb_id integer NOT NULL,
    actor_name character varying(150)
);


ALTER TABLE public.actor OWNER TO docker;

--
-- Name: actor_id_seq; Type: SEQUENCE; Schema: public; Owner: docker
--

CREATE SEQUENCE public.actor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actor_id_seq OWNER TO docker;

--
-- Name: actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: docker
--

ALTER SEQUENCE public.actor_id_seq OWNED BY public.actor.id;


--
-- Name: genre; Type: TABLE; Schema: public; Owner: docker
--

CREATE TABLE public.genre (
    id integer NOT NULL,
    genre character varying(200)
);


ALTER TABLE public.genre OWNER TO docker;

--
-- Name: genre_id_seq; Type: SEQUENCE; Schema: public; Owner: docker
--

CREATE SEQUENCE public.genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.genre_id_seq OWNER TO docker;

--
-- Name: genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: docker
--

ALTER SEQUENCE public.genre_id_seq OWNED BY public.genre.id;


--
-- Name: movie; Type: TABLE; Schema: public; Owner: docker
--

CREATE TABLE public.movie (
    id integer NOT NULL,
    movie_title character varying(100) NOT NULL,
    release_year integer NOT NULL,
    release_month integer NOT NULL,
    imdb_id character varying(20) NOT NULL,
    tmdb_id integer NOT NULL,
    runtime integer NOT NULL,
    rating character varying(20),
    budget numeric,
    imdb_rating numeric,
    rt_rating numeric,
    genre_id integer
);


ALTER TABLE public.movie OWNER TO docker;

--
-- Name: movie_actor; Type: TABLE; Schema: public; Owner: docker
--

CREATE TABLE public.movie_actor (
    movie_id integer NOT NULL,
    actor_id integer NOT NULL
);


ALTER TABLE public.movie_actor OWNER TO docker;

--
-- Name: movie_id_seq; Type: SEQUENCE; Schema: public; Owner: docker
--

CREATE SEQUENCE public.movie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movie_id_seq OWNER TO docker;

--
-- Name: movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: docker
--

ALTER SEQUENCE public.movie_id_seq OWNED BY public.movie.id;


--
-- Name: actor id; Type: DEFAULT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.actor ALTER COLUMN id SET DEFAULT nextval('public.actor_id_seq'::regclass);


--
-- Name: genre id; Type: DEFAULT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.genre ALTER COLUMN id SET DEFAULT nextval('public.genre_id_seq'::regclass);


--
-- Name: movie id; Type: DEFAULT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.movie ALTER COLUMN id SET DEFAULT nextval('public.movie_id_seq'::regclass);


--
-- Data for Name: actor; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.actor (id, actor_performance, tmdb_id, actor_name) FROM stdin;
\.
COPY public.actor (id, actor_performance, tmdb_id, actor_name) FROM '$$PATH$$/2900.dat';

--
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.genre (id, genre) FROM stdin;
\.
COPY public.genre (id, genre) FROM '$$PATH$$/2902.dat';

--
-- Data for Name: movie; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.movie (id, movie_title, release_year, release_month, imdb_id, tmdb_id, runtime, rating, budget, imdb_rating, rt_rating, genre_id) FROM stdin;
\.
COPY public.movie (id, movie_title, release_year, release_month, imdb_id, tmdb_id, runtime, rating, budget, imdb_rating, rt_rating, genre_id) FROM '$$PATH$$/2898.dat';

--
-- Data for Name: movie_actor; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.movie_actor (movie_id, actor_id) FROM stdin;
\.
COPY public.movie_actor (movie_id, actor_id) FROM '$$PATH$$/2903.dat';

--
-- Name: actor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.actor_id_seq', 11647, true);


--
-- Name: genre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.genre_id_seq', 580, true);


--
-- Name: movie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.movie_id_seq', 5343, true);


--
-- Name: actor actor_pkey; Type: CONSTRAINT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_pkey PRIMARY KEY (id);


--
-- Name: actor actor_tmdb_id_key; Type: CONSTRAINT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_tmdb_id_key UNIQUE (tmdb_id);


--
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (id);


--
-- Name: movie_actor movie_actor_pkey; Type: CONSTRAINT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.movie_actor
    ADD CONSTRAINT movie_actor_pkey PRIMARY KEY (movie_id, actor_id);


--
-- Name: movie movie_imdb_id_key; Type: CONSTRAINT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_imdb_id_key UNIQUE (imdb_id);


--
-- Name: movie movie_pkey; Type: CONSTRAINT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (id);


--
-- Name: movie genre_fk; Type: FK CONSTRAINT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT genre_fk FOREIGN KEY (genre_id) REFERENCES public.genre(id);


--
-- Name: movie_actor movie_actor_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.movie_actor
    ADD CONSTRAINT movie_actor_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actor(id);


--
-- Name: movie_actor movie_actor_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: docker
--

ALTER TABLE ONLY public.movie_actor
    ADD CONSTRAINT movie_actor_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movie(id);


--
-- PostgreSQL database dump complete
--

