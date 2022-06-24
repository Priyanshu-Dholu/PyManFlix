from tmdbv3api import TMDb, Movie

# TMDB API Section
tmdb = TMDb()
tmdb.api_key = 'fb86432acfe5114ca73b86d4cbe66ef2'
tmdb.language = 'en'
tmdb.debug = True

# Function To Get Movie Details
def get_movie_detail(operation, movie_id_tmd):    
    movie = Movie()
    m = movie.details(movie_id_tmd)
    if operation == 1:
        link = f'https://image.tmdb.org/t/p/w220_and_h330_face/{m.poster_path}'
        return link
    elif operation == 2:
        return f'{m.original_title}'
    elif operation == 3:
        return int(m.release_date[:4])
    elif operation == 4:
        return f'https://image.tmdb.org/t/p/w1280{m.backdrop_path}'
    elif operation == 5:
        return f'{m.overview}'
    elif operation == 6:
        link = m['videos']['results'][0]["key"]           
        return 'https://www.youtube.com/embed/' + link
    else:
        return 'Error'

# Function To Get Movie ID
def get_movie_id(movie_name):
    movie = Movie()
    search = movie.search(movie_name)
    movie_list_id = []      
    movie_list_title = []
    movie_list_poster = []
    final = []
    for i in search:
        for z in i:
            if z == 'id':
                movie_list_id.append(i[z])
            elif z == 'title':
                movie_list_title.append(i[z])                
            elif z == 'poster_path':
                movie_list_poster.append(i[z])     
            final = list(zip(movie_list_id,movie_list_title , movie_list_poster))                       
    
    return final
