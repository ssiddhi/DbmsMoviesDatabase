/* Dump the data from the tables */
\o movies.txt
SELECT * FROM movies;
\o casts.txt
SELECT * FROM casts;
\o wrote.txt
SELECT * FROM wrote;
\o starred_in.txt
SELECT * FROM starred_in;
\o directed.txt
SELECT * FROM directed;
\o produced.txt
SELECT * FROM produced;
\o reviews.txt
SELECT * FROM reviews;
\o released.txt
SELECT * FROM released;
\o finances.txt
SELECT * FROM finances;

/* Dump the data from the questions */
\o q1.txt 
\qecho List 10 movies released between the years 2000 and 2010 with the longest duration.
\qecho select name,year, runtime from movies where year>2000 and year<2010 ORDER BY runtime DESC  limit 10;
select name,year, runtime from movies where year>2000 and year<2010 ORDER BY runtime DESC  limit 10;

\o q2.txt
\qecho Which is the highest budget movie released between 1986 to 2000?
\qecho select m.movie_id, m.name, m.year, f.budget from finances f natural join movies m where m.year between '1999' and '2012' and f.budget is not null order by f.budget desc limit 1;
select m.movie_id, m.name, m.year, f.budget from finances f natural join movies m where m.year between '1999' and '2012' and f.budget is not null order by f.budget desc limit 1;

\o q3.txt
\qecho List all the directors that have directed ‘Action’ movies.
\qecho SELECT first, last, title, name, genre FROM movies natural join directed natural join casts WHERE genre = 'Action';
SELECT first, last, title, name, genre FROM movies natural join directed natural join casts WHERE genre = 'Action';

\o q4.txt
\qecho List all the ‘Comedy’ movies released between 1986 and 2016?
\qecho select name,genre,year from movies where year>1986 and year<2016 and genre='Comedy';
select name,genre,year from movies where year>1986 and year<2016 and genre='Comedy';

\o q5.txt
\qecho Out of all the highest rated movies, which movie has the highest budget?
\qecho select m.movie_id, m.name, m.year, f.budget, r.score from reviews R natural join finances f natural join movies m where f.budget is not null and r.score is not null order by r.score desc, f.budget desc limit 1;
select m.movie_id, m.name, m.year, f.budget, r.score from reviews R natural join finances f natural join movies m where f.budget is not null and r.score is not null order by r.score desc, f.budget desc limit 1;

\o q6.txt
\qecho List the top 5 stars with highest movie rating between the years 2000 and 2016?
\qecho select distinct C.member_id, C.first, C.last, MAX(r.score) from casts C natural join starred_in S natural join reviews R natural join movies m where m.year between '2000' and '2016' and r.score is not null GROUP BY C.member_id order by MAX(r.score) desc limit 5;
select distinct C.member_id, C.first, C.last, MAX(r.score) from casts C natural join starred_in S natural join reviews R natural join movies m where m.year between '2000' and '2016' and r.score is not null GROUP BY C.member_id order by MAX(r.score) desc limit 5;

\o q7.txt
\qecho Which is the most popular star (give your answer in terms of the greatest number of movies starred in)?
\qecho SELECT  C.member_id, C.first, C.last, COUNT(S.movie_id) FROM casts C natural join starred_in S GROUP BY C.member_id ORDER BY COUNT(S.movie_id) DESC LIMIT 5;
SELECT  C.member_id, C.first, C.last, COUNT(S.movie_id) FROM casts C natural join starred_in S GROUP BY C.member_id ORDER BY COUNT(S.movie_id) DESC LIMIT 5;

\o q8.txt
\qecho Create a view for the Walt Disney Productions and their total gross income.
\qecho CREATE VIEW prod_view AS select P.company, sum(F.gross) As gross_income FROM produced P NATURAL JOIN finances F where company='Walt Disney Productions' GROUP BY P.company;
\qecho SELECT * FROM prod_view;
CREATE VIEW prod_view AS select P.company, sum(F.gross) As gross_income FROM produced P NATURAL JOIN finances F where company='Walt Disney Productions' GROUP BY P.company;
SELECT * FROM prod_view;

\o q9.txt
\qecho How many movies share the same name?
\qecho SELECT  name FROM movies GROUP BY name HAVING COUNT(movie_id) >1;
SELECT  name FROM movies GROUP BY name HAVING COUNT(movie_id) >1;

\o q10.txt
\qecho Which studio received the highest total revenue in the 1990s?
\qecho SELECT P.company, SUM(F.gross) AS Revenue FROM movies AS M NATURAL JOIN finances AS F NATURAL JOIN produced P WHERE M.year between '1990' and '1999' and F.gross is not null GROUP BY P.company ORDER BY revenue DESC limit 1;
SELECT P.company, SUM(F.gross) AS Revenue FROM movies AS M NATURAL JOIN finances AS F NATURAL JOIN produced P WHERE M.year between '1990' and '1999' and F.gross is not null GROUP BY P.company ORDER BY revenue DESC limit 1;

\o q11.txt
\qecho Which directors have directed in more than 2 movies?
\qecho SELECT  C.member_id, C.first, C.last FROM casts C natural join directed D1 inner join directed D2 on D1.member_id = D2.member_id where D1.movie_id != D2.movie_id GROUP BY C.member_id;
SELECT  C.member_id, C.first, C.last FROM casts C natural join directed D1 inner join directed D2 on D1.member_id = D2.member_id where D1.movie_id != D2.movie_id GROUP BY C.member_id;

\o q12.txt
\qecho List actors that have starred in more than one movie under a company.
\qecho SELECT C.member_id, C.first, C.last, P.company, COUNT(S.movie_id) AS num_movies FROM Casts C NATURAL JOIN starred_in S NATURAL JOIN produced P GROUP BY C.member_id, P.company HAVING COUNT(S.movie_id) > 1;
SELECT C.member_id, C.first, C.last, P.company, COUNT(S.movie_id) AS num_movies FROM Casts C NATURAL JOIN starred_in S NATURAL JOIN produced P GROUP BY C.member_id, P.company HAVING COUNT(S.movie_id) > 1;

\o q13.txt
\qecho Which movie generated the highest revenue in the year 2015?
\qecho select m.movie_id, m.name, m.year, f.gross as revenue from finances f natural join movies m where m.year = '2015' and f.gross is not null order by f.gross  desc limit 1;
select m.movie_id, m.name, m.year, f.gross as revenue from finances f natural join movies m where m.year = '2015' and f.gross is not null order by f.gross  desc limit 1;

\o q14.txt
\qecho Find the actors who have not worked in any movie between 1999 and 2012(including the start year and end year)?
\qecho select distinct member_id, first, last  from starred_in natural join casts where member_id not in ( select C.member_id from casts C natural join starred_in  natural join movies m where m.year between '1999' and '2012') ;
select distinct member_id, first, last  from starred_in natural join casts where member_id not in ( select C.member_id from casts C natural join starred_in  natural join movies m where m.year between '1999' and '2012') ;

\o q15.txt
\qecho Find the movies released before January 1st, 2000?
\qecho select M.name,M.year,R.date from movies M join released R on M.movie_id=R.movie_id where R.date<'2000-01-01';
select M.name,M.year,R.date from movies M join released R on M.movie_id=R.movie_id where R.date<'2000-01-01';

\o q16.txt
\qecho How many numbers of movies got released between the years 1985 and 2000 which has the same writer and director?
\qecho SELECT COUNT(movie_id) FROM wrote NATURAL JOIN directed NATURAL JOIN movies WHERE year BETWEEN '1985' AND '2000';
SELECT COUNT(movie_id) FROM wrote NATURAL JOIN directed NATURAL JOIN movies WHERE year BETWEEN '1985' AND '2000';

\o q17.txt
\qecho Compute the average runtime and count the number of movies for each genre.
\qecho SELECT genre,AVG(runtime), COUNT(name) FROM movies GROUP BY genre;
SELECT genre,AVG(runtime), COUNT(name) FROM movies GROUP BY genre;

\o q18.txt
\qecho What is the average budget for each year?
\qecho SELECT M.year, AVG(F.budget) FROM movies AS M NATURAL JOIN finances AS F GROUP BY M.year ORDER BY M.year ASC;
SELECT M.year, AVG(F.budget) FROM movies AS M NATURAL JOIN finances AS F GROUP BY M.year ORDER BY M.year ASC;

\o q19.txt
\qecho Find the years in which at least five ‘G’ rated movies were released?
\qecho SELECT year,count(*) FROM movies WHERE rating = 'G' group by year having count (rating = 'G') >= 5;
SELECT year,count(*) FROM movies WHERE rating = 'G' group by year having count (rating = 'G') >= 5;

\o q20.txt
\qecho How many movies that have score greater than 7 also have at least 10,000 user votes?
\qecho SELECT COUNT(*) FROM Reviews AS R WHERE R.score>7 AND votes>=10000;
SELECT COUNT(*) FROM Reviews AS R WHERE R.score>7 AND votes>=10000;


