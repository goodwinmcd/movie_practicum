
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="movies",
    user="docker",
    password="docker")


sql = """SELECT movie_id, genre_id FROM movie_genre"""

cursor = conn.cursor()
cursor.execute(sql)
rows = cursor.fetchall()

update_sql = """
    UPDATE movie SET genre_id = %s WHERE id = %s
"""

for row in rows:
    update_values = (row[1], row[0],)
    cursor.execute(update_sql, update_values)
    conn.commit()
cursor.close()