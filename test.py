from tmdbv3api import TMDb,Movie

tmdb = TMDb()
tmdb.api_key = 'fb86432acfe5114ca73b86d4cbe66ef2'
tmdb.language = 'en'
tmdb.debug = True
movie = Movie()
m = movie.details(343611)
link = f'https://image.tmdb.org/t/p/original/{m.poster_path}'
print(link)