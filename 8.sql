SELECT name
FROM stars
	INNER JOIN people ON people.id = stars.person_id
	INNER JOIN movies ON stars.movie_id = movies.id
WHERE movies.title = "Toy Story"