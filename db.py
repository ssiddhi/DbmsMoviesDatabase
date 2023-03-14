import psycopg2
from sqlalchemy import create_engine
import os

## DON'T FORGET TO SOURCE THE ENVIRONMENT VARIABLES!!! ##
def create_connection():
  """This is copied from the lecture and allows us to make
     changes to the SQL database via python commands."""
  connection = psycopg2.connect(
      host=os.environ['CLASS_DB_HOST'],
      database=os.environ['CLASS_DB_USERNAME'],
      user=os.environ['CLASS_DB_USERNAME'],
      password=os.environ['CLASS_DB_PASSWORD']
  )
  connection.autocommit = True
  return connection
def execute_general_command(db_conn, cmd):
  """receives a connection and a string that contains a SQL command
     for the db, then executes the command.
     e.g. "SELECT first, last FROM agent LIMIT 20;"
     Careful! This allows us to modify add or drop tables etc."""
  cur = db_conn.cursor()
  try:
    cur.execute(cmd)
    print(cur.fetchall())
  except:
    print("error: bad command: " + cmd)

def clean_up(db_conn):
  """This is needed in order to start from scratch each time
     we run the script. Every time a new table is created by
     the script we need to add a drop command here. """
  cur = db_conn.cursor()
  try:
    create_stmt = "DROP VIEW prod_view;"
    cur.execute(create_stmt)
  except:
    print("failed to drop view")
  tables = ['directed', 'wrote', 'starred_in', 'casts','reviews','released','finances','produced','movies']
  for table in tables:
    try:
      create_stmt = "DROP TABLE " + table +";"
      cur.execute(create_stmt)
    except:
      print("failed to drop " + table)

def create_movie_table(db_conn):
  """create the movie table."""
  cur = db_conn.cursor()
  create_stmt = "CREATE TABLE movies (" \
                "  movie_id  INT PRIMARY KEY," \
                "  name varchar(264)," \
                "  year numeric(4,0)," \
                "  genre varchar(264)," \
                "  rating  varchar(264)," \
                "  country varchar(264)," \
                "  runtime INT);"
  print(create_stmt)
  cur.execute(create_stmt)

def create_cast_table(db_conn):
  """create the casts table."""
  cur = db_conn.cursor()
  create_stmt = "CREATE TABLE casts (" \
                "  member_id  INT PRIMARY KEY," \
                "  first varchar(264)," \
                "  last varchar(264)," \
                "  title  varchar(264));"
  print(create_stmt)
  cur.execute(create_stmt)

def create_finances_table(db_conn):
  """create the finances table."""
  cur = db_conn.cursor()
  create_stmt = "CREATE TABLE finances (" \
                "  movie_id  INT PRIMARY KEY," \
                "  budget BIGINT," \
                "  gross BIGINT," \
		"  FOREIGN KEY(movie_id)  REFERENCES movies(movie_id));"
  print(create_stmt)
  cur.execute(create_stmt)

def create_reviews_table(db_conn):
  """create the reviews table."""
  cur = db_conn.cursor()
  create_stmt = "CREATE TABLE reviews (" \
                "  movie_id  INT PRIMARY KEY," \
                "  score numeric(2,1)," \
                "  votes INT," \
                "  FOREIGN KEY(movie_id)  REFERENCES movies(movie_id));"
  print(create_stmt)
  cur.execute(create_stmt)

def create_released_table(db_conn):
  """create the released table."""
  cur = db_conn.cursor()
  create_stmt = "CREATE TABLE released (" \
                "  movie_id  INT PRIMARY KEY," \
                "  country  varchar(264)," \
                "  date DATE NOT NULL," \
                "  FOREIGN KEY(movie_id)  REFERENCES movies(movie_id));"
  print(create_stmt)
  cur.execute(create_stmt)

def create_produced_table(db_conn):
  """create the produced table."""
  cur = db_conn.cursor()
  create_stmt = "CREATE TABLE produced (" \
                "  company  varchar(264)," \
                "  movie_id  INT," \
                "  FOREIGN KEY(movie_id)  REFERENCES movies(movie_id)," \
                "  PRIMARY KEY(company, movie_id) );"
  print(create_stmt)
  cur.execute(create_stmt)

def create_relational_tables(db_conn):
  """create the "directed" relational table."""
  cur = db_conn.cursor()
  tables = ["directed", "wrote", "starred_in"]
  for table in tables:
    create_stmt = "CREATE TABLE " + table + " (" \
                  "  movie_id  INT," \
                  "  member_id INT," \
                  "  FOREIGN KEY(movie_id)  REFERENCES movies(movie_id), " \
                  "  FOREIGN KEY(member_id)  REFERENCES casts(member_id), " \
                  "  PRIMARY KEY(movie_id, member_id) );"
    print(create_stmt)
    cur.execute(create_stmt)


def insert_df_rows_to_table(df, table_name):
  """This is copied from the lecture and allows us to add rows
     via python command to  any table that has been created"""
  engine = create_engine(
      f"postgresql://{os.environ['CLASS_DB_USERNAME']}:"
      f"{os.environ['CLASS_DB_PASSWORD']}@"
      f"{os.environ['CLASS_DB_HOST']}:"
      f"5432/{os.environ['CLASS_DB_USERNAME']}"
  )
  df.to_sql(table_name, engine, if_exists="append", index=False)


def query_movie(db_conn):
  """an example query. Just write the sql text and don't forget the semicolen"""
  cur = db_conn.cursor()
  cur.execute("SELECT * FROM movies WHERE rating = 'Not Rated';")
  print(cur.fetchall())

def query_cast(db_conn):
  """an example query. Just write the sql text and don't forget the semicolen"""
  cur = db_conn.cursor()
  cur.execute("SELECT * FROM casts;")
  print(cur.fetchall())

def query_finances(db_conn):
  """an example query. Just write the sql text and don't forget the semicolen"""
  cur = db_conn.cursor()
  cur.execute("SELECT * FROM finances;")
  print(cur.fetchall())

def query_reviews(db_conn):
  """an example query. Just write the sql text and don't forget the semicolen"""
  cur = db_conn.cursor()
  cur.execute("SELECT * FROM reviews;")
  print(cur.fetchall())

def query_released(db_conn):
  """an example query. Just write the sql text and don't forget the semicolen"""
  cur = db_conn.cursor()
  cur.execute("SELECT * FROM released;")
  print(cur.fetchall())

def setup_db():
  """set up the connection, clean up, etc. This will be run automatically when
     running the file directly but it can also be called manually by any file
     or module that imports this file."""

  conn = create_connection()
  clean_up(conn)
  create_movie_table(conn)

  create_cast_table(conn)
  create_finances_table(conn)
  create_reviews_table(conn)
  create_released_table(conn)
  create_produced_table(conn)
  create_relational_tables(conn)

  return conn

if __name__ == "__main__":
  setup_db()
