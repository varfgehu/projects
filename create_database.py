import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#Create database for users

#db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL)")
#db.commit()


#db.execute("CREATE TABLE users ( id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL )")
#db.commit()

#db.execute("CREATE TABLE reviews ( id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, book_id INTEGER NOT NULL, text VARCHAR NOT NULL, rating INTEGER NOT NULL, books_id INTEGER REFERENCES books )")
#db.commit()

#db.execute("ALTER TABLE reviews ADD COLUMN rating INTEGER NOT NULL")
#db.commit()

#db.execute("DROP DATABASE books")
#db.commit()

#db.execute("DROP DATABASE users")
#db.commit()

#db.execute("DROP DATABASE reviews")
#db.commit()
