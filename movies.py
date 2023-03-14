#!/usr/bin/python3

import pandas as pd
import db
import re
import datetime


def wrangle_movies(df):
  """clean up the data as needed for the movie table.
     Specifically, we need to change "Not Rated" values to
     be the same as "Unrated" and to add a unique movie_id key."""

  df['rating'] = df['rating'].apply(not_rated_to_unrated)
  df['movie_id'] = get_ids(df)
  return pd.DataFrame(data=df[['movie_id','name', 'year', 'genre', 'rating', 'country','runtime']])

def wrangle_cast(df):
  """clean up the data as needed for the cast table."""
  ## get the raw values for the director, writer, and star fields and add all of them as values for 'name'
  ## store the values in a temporary dataframe
  people_df = pd.DataFrame(data=pd.melt(df, id_vars=['name'],value_vars=['director','writer','star']))
  ## Some names have a title of 'Jr.' or 'Sr.' as a suffix. Here we separate them from the full name
  cast_df = pd.DataFrame(data=people_df['value'].str.extract(r'^(?P<full_name>.*?)(?P<title>[JS]r\.)?$', expand=True))
  ## split the full name into first and last. Some full names have more than two names (e.g. middle names)
  ## which will be stored in the first name field.
  ## some names are only one word, they will be stored as the last name and the first name will be null (empty)
  cast_df['first'] = cast_df['full_name'].apply(get_first_name)
  cast_df['last'] = cast_df['full_name'].apply(get_last_name)
  ## store the original name for now to make it easier to build the relational DBs
  ## remove this later, once done with the relational tables (directed/wrote/starred_in)
  cast_df['original_name'] = people_df['value']
  ## get rid of duplicates and of columns that are not needed
  cast_df = cast_df.drop(columns=['full_name'])
  cast_df = cast_df.drop_duplicates(['first','last','title'])
  ## create a unique member_id for each person
  cast_df['member_id'] = get_ids(cast_df)
  return cast_df[['member_id','first','last','title','original_name']]

def wrangle_relational(cast_df, df, job):
  """create the specified relational dataframe"""
  relational_df = pd.DataFrame(data=pd.merge(cast_df,df,left_on='original_name', right_on=job))
  print(job)
  return relational_df[['movie_id','member_id']]

def wrangle_reviews(df):
  """create the reviews dataframe, no wrangling is needed."""
  reviews_df = pd.DataFrame(data=df[['score','votes']])
  reviews_df['movie_id'] = get_ids(df)
  return reviews_df[['movie_id','score','votes']]

def wrangle_finances(df):
  """create the finances dataframe, no wrangling is needed."""
  finances_df = pd.DataFrame(data=df[['budget','gross']])
  finances_df['movie_id'] = get_ids(df)
  return finances_df[['movie_id','budget','gross']]

def wrangle_released(df):
  """create the released dataframe. split the original data into date and country"""
  released_df = pd.DataFrame(data=df[['released']])
  released_df['date'] = df['released'].apply(get_release_date)
  released_df['country'] = df['released'].apply(get_release_country)
  released_df['movie_id'] = get_ids(df)
  return released_df[['movie_id', 'date', 'country']]

def wrangle_produced(df):
  """create the produced dataframe, no wrangling is needed."""
  return pd.DataFrame(data=df[['company','movie_id']])

def get_ids(df):
  """use this to make sure the IDs are coordinated"""
  return range(1,len(df) + 1)

def not_rated_to_unrated(rating):
  """ combine the values "Not Rated" and "Unrated" into a single value since
      they are essentially the same"""
  if pd.isnull(rating):
    return rating
  return re.sub("Not Rated","Unrated",rating)

def get_release_country(release):
  """the country is wrapped by parentheses"""
  if pd.isnull(release):
    return release
  return re.sub(".*\((.*)\)",r'\1',release)

def get_release_date(text):
  """turn the string with the release date into a datetime object"""
  raw_date =  text.split('(',1)[0]
  ## try to get the exact date
  date_obj =  pd.to_datetime(raw_date, format = "%B %d, %Y ", errors = 'coerce')
  if(pd.isnull(date_obj)):
    ## try with just month and year
    date_obj =  pd.to_datetime(raw_date, format = "%B %Y ", errors = 'coerce')
  if(pd.isnull(date_obj)):
    ## try with just year. raise error if it fails
    date_obj =  pd.to_datetime(raw_date[0:4], format = "%Y", errors = 'raise')
  return date_obj

def get_first_name(full_name):
  """split the full name into space separated words and then
     join all but the last together with a single space in
     between each word."""
  if pd.isnull(full_name):
    return full_name
  return " ".join(full_name.split()[0:-1])


def get_last_name(full_name):
  """get the last space separated word"""
  if pd.isnull(full_name):
    return full_name
  return full_name.split()[-1]

def execute_general_commands(conn):
  """get a string from a user and execute it as a SQL command on the DB"""
  cmd = input("Please enter a valid SQL command or 'exit' to finish: ")
  while(not cmd.lower() == "exit"):
    db.execute_general_command(conn, cmd)
    cmd = input("Please enter a valid SQL command or 'exit' to finish: ")
  print("Thank you, goodbye.")

def runme():
  """this is the main function that does all the work."""
  ## read the csv file
  df = pd.read_csv("movies.csv", header=0)

  ## prepare the dataframes needed for each table
  movies_df = wrangle_movies(df)
  print(movies_df)
  released_df = wrangle_released(df)
  print(released_df)
  cast_df = wrangle_cast(df)
  print(cast_df)
  reviews_df = wrangle_reviews(df)
  print(reviews_df)
  finances_df = wrangle_finances(df)
  print(finances_df)
  produced_df = wrangle_produced(df)
  print(produced_df)
  directed_df = wrangle_relational(cast_df, df, "director")
  print(directed_df)
  wrote_df = wrangle_relational(cast_df, df, "writer")
  print(wrote_df)
  starred_df = wrangle_relational(cast_df, df, "star")
  print(starred_df)

  ##clean up the casts DF. Now that we have the relational DFs we don't need
  ## the original name anymore
  cast_df = cast_df.drop(columns=['original_name'])
  print(cast_df)

  ## setup the database and retreive the connection object
  conn = db.setup_db()
  ## input the data from the dataframes into the relevant tables in the database
  db.insert_df_rows_to_table(movies_df[['movie_id','name', 'year', 'genre', 'rating', 'country','runtime']], 'movies')
  db.insert_df_rows_to_table(cast_df[['member_id','first', 'last', 'title']], 'casts')
  db.insert_df_rows_to_table(finances_df[['movie_id','budget', 'gross']], 'finances')
  db.insert_df_rows_to_table(reviews_df[['movie_id','score', 'votes']], 'reviews')
  db.insert_df_rows_to_table(released_df[['movie_id','country', 'date']], 'released')
  db.insert_df_rows_to_table(produced_df[['company', 'movie_id']], 'produced')
  db.insert_df_rows_to_table(directed_df[['movie_id','member_id']], 'directed')
  db.insert_df_rows_to_table(wrote_df[['movie_id','member_id']], 'wrote')
  db.insert_df_rows_to_table(starred_df[['movie_id','member_id']], 'starred_in')

  #The queries for all 20 questions can be input and dumped automatically in the database by importing project_dump.sql in the database

  ## allow user to run SQL commands manually
  execute_general_commands(conn)

if __name__ == "__main__":
  runme()

