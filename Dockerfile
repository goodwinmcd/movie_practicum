FROM postgres
ENV POSTGRES_DB movies
ENV POSTGRES_USER docker
ENV POSTGRES_PASSWORD docker
COPY create_tables.sql /docker-entrypoint-initdb.d/
COPY postgres/* /docker-entrypoint-initdb.d/