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
        return f'{m.release_date}'
    elif operation == 4:
        return f'https://image.tmdb.org/t/p/w1280{m.backdrop_path}'
    elif operation == 5:
        return f'{m.overview}'
    elif operation == 6:
        link = m['videos']['results'][0]["key"]
        print('https://www.youtube.com/embed/' + link)
        return 'https://www.youtube.com/embed/' + link
    else:
        return 'Error'

# get_movie_id('Minions')


# Function To Get Movie ID from TMDB
# def get_movie_id_tmdb(movie_name):
#     movie = Movie()
#     search = movie.search(movie_name)
#     movie_list = []            
#     for i in search:
#         movie_list.append(i['id'])
       
#     return movie_list[0]

# get_movie_id_tmdb('Minions')
# Function To Get Movie ID and Moveie Name from TMDB
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

mdata = get_movie_id('Harry Potter')
# print(mdata)
for x in mdata :
    print(x[2])

# print(mdata[1])
# for mov in mdata:
#     print(mov)
    # print(mov)
    # print(mov)