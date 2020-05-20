import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import csv

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

file = open("books.csv")
if file is None:
    print("Could not open file! Please check file location!")

reader = csv.reader(file)

for isbn, title, author, year in reader:
    db.execute("INSERT INTO books (author, title, year, isbn) VALUES (:author, :title, :year, :isbn)", {"author":author, "title":title, "year":year, "isbn":isbn})
    print(f"Book added: {author} - {title} - {year} ISBN: {isbn}")

db.commit()
file.close()
