import sqlite3
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

conn = sqlite3.connect("recommend.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS ratings (
    user_id INTEGER,
    movie_id INTEGER,
    rating FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS item_vectors (
    movie_id INTEGER PRIMARY KEY,
    vector TEXT
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS user_vectors (
    user_id INTEGER PRIMARY KEY,
    vector TEXT
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    date TEXT,
    genres INTEGER,
    rating FLOAT
)
""")

conn.commit()
conn.close()

import pandas as pd
conn = sqlite3.connect("recommend.db")
c = conn.cursor()

# write ratings to db
df = pd.read_csv("../../ml-100k/u.data", sep="\t", names=["user_id", "movie_id", "rating", "timestamp"])
df.to_sql("ratings", conn, if_exists="append", index=False)

# calculate average ratings for each movie
avg_ratings = df.groupby('movie_id')['rating'].mean().to_dict()

# write movies to db
with open("../../ml-100k/u.item", encoding="ISO-8859-1") as f:
    for line in f:
        parts = line.strip().split("|")

        movie_id = int(parts[0])
        title = parts[1]
        release_date = parts[2]

        # genres from index 5 to 23
        genre_flags = parts[5:24]
        genre_binary = ''.join(genre_flags)
        genre_int = int(genre_binary, 2)

        # get average rating for this movie
        avg_rating = round(avg_ratings.get(movie_id, 0.0),1)

        c.execute("""
            INSERT OR REPLACE INTO movies (id, title, date, genres, rating)
            VALUES (?, ?, ?, ?, ?)
        """, (movie_id, title, release_date, genre_int, avg_rating))

conn.commit()
conn.close()