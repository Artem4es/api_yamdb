import sqlite3
import pandas

conn = sqlite3.connect('db.sqlite3', check_same_thread=False)


# df = pandas.read_csv("static/data/category.csv")
# df.to_sql("reviews_category", conn, if_exists='append', index=False)

# df = pandas.read_csv("static/data/comments.csv")
# df.to_sql("reviews_comment", conn, if_exists='append', index=False)

# df = pandas.read_csv("static/data/genre.csv")
# df.to_sql("reviews_genre", conn, if_exists='append', index=False)

# df = pandas.read_csv("static/data/genre_title.csv")
# df.to_sql("reviews_titlegenre", conn, if_exists='append', index=False)

df = pandas.read_csv("static/data/review.csv")
df.to_sql("reviews_review", conn, if_exists='append', index=False)

# df = pandas.read_csv("static/data/titles.csv")
# df.to_sql("reviews_title", conn, if_exists='append', index=False)

# df = pandas.read_csv("static/data/users.csv")
# df.to_sql("reviews_user", conn, if_exists='append', index=False)
