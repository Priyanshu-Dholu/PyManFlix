from tmdbv3api import TMDb, Movie

# tmdb = TMDb()
# tmdb.api_key = 'fb86432acfe5114ca73b86d4cbe66ef2'
# tmdb.language = 'en'
# tmdb.debug = True
# movie = Movie()
# m = movie.details(343611)
# link = f'https://image.tmdb.org/t/p/original/{m.poster_path}'
# print(link)


# org_string = 'https://www.dropbox.com/s/chdsz9gtjweedwt/Bloodshot%20%282020%29%20Hindi%205.1.mkv?dl=1'
# replacementStr = 'raw=1'
# print(strValue)
# # Replace last character of string with 'X'
# org_string[:-4] + replacementStr
# print(strValue)


def get_movie_detail(movie_id_tmd):
    tmdb = TMDb()
    tmdb.api_key = 'fb86432acfe5114ca73b86d4cbe66ef2'
    tmdb.language = 'en'
    tmdb.debug = True
    movie = Movie()
    m = movie.details(movie_id_tmd)
    # Get Youtube Id From m.keys() dictionary
    print(m.key)


def get_movie_detail2(operation, movie_id_tmd):
    tmdb = TMDb()
    tmdb.api_key = 'fb86432acfe5114ca73b86d4cbe66ef2'
    tmdb.language = 'en'
    tmdb.debug = True
    movie = Movie()
    m = movie.details(movie_id_tmd)
    if operation == 1:
        link = f'https://www.youtube.com/watch?v={m.keys()[0]}'
        print(link)
    else:
        return 'Error'


get_movie_detail(93456)
# get_movie_detail2(1,93456)
