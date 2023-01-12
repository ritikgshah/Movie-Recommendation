from django.shortcuts import render
import pandas as pd
import numpy as np
import imdb
from sklearn.metrics import jaccard_score
from scipy import stats
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import requests
from requests import get
from bs4 import BeautifulSoup
import random
from django.http import HttpResponse
import pymongo
from requests_html import HTMLSession
from requests import get
import datetime
import re
client = pymongo.MongoClient("mongodb://localhost:27017/")
print(client)

db = client["MovieReco"]
collection = db["info"]
collection_rating = db["ratings"]

df = pd.read_csv("IMDb movies.csv")
df = df.replace(np.nan,"Nan",regex =True)

languages = df['language'].tolist()
language = []
for ll in languages:
    if ',' in ll:
        lan = ll.split(',')
        lan = lan[0]
    else: lan = ll
    language.append(lan)

df['Language'] = language
Genre =['Horror','Thriller','Comedy']
dff = pd.read_csv("Ratingss.csv")
table = dff.transpose()
table.columns = table.iloc[1]
table = table.iloc[2:]
table = table.fillna(0.0)
ddf = pd.read_csv("Recommender.csv")
df3 = zip(df['original_title'].tolist(),df['genre'].tolist(),df['actors'].tolist(),df['director'].tolist(),df['Language'].tolist(),df['country'].tolist(),df['avg_vote'].tolist(),df['year'].tolist())
data = pd.DataFrame(df3)
data.columns = ['Title','Genre','Cast','Director','Language','Country','Rating','Year']

df4 = zip(df['original_title'].tolist(),df['genre'].tolist(),df['Language'].tolist())
genre_tables = pd.DataFrame(df4)
genre_tables.columns = ['Title','Genre','Language']
data = data.set_index('Title')
genre_tables = genre_tables.set_index('Title')

global likem
likem=[]
global dislikem
dislikem = []
global reviews
reviews = []
global rmovies
rmovies =[]
global movies_list
movies_list =["Alien","Cast Away","Batman Begins","Inception","No Smoking"]
global lang
lang = ['English','Hindi']
global like
like=[]
global dislike
dislike =[]

def password_change(email,old_password, new_password):
    return 
    

def signup(name, email, password, MovieList3, GenreList):
    present = collection.find_one({"email": email})
    if(present==None):
        collection.insert_one({"name": name, "email": email, "password": password, "movieList":MovieList3, "like":[], "Genre List":GenreList})
    else:
        print("email already in use. Pls login")

def extract_Genre(email):
    one = collection.find_one({"email": email})
    GenreList = one["Genre List"]
    return(GenreList)


def login(email, password):
    one = collection.find_one({"email": email})
    if (one == None):
        print("email doesnt exist")
        return False
    else:
        if (one["password"] == password):
            print("login successful")
            return True
        else:
            print("incorrect passwrod")
            return False
    return True

def updateMovieList(email, movieName):
    '''
    Add movie to movie list
    '''
    one = collection.find_one({"email": email})
    movieL = one["movieList"]
    if(movieName not in movieL):
        movieL.append(movieName)
        prev = {"email": email}
        nextt = {"$set":{"movieList": movieL}}
        collection.update_one(prev,nextt)

def findLatestMovie(email):
    one = collection.find_one({"email": email})
    movieL = one["movieList"]
    return (movieL[-1])

def password_change(email, old_password, new_password):
    one = collection.find_one({"email": email})
    old_pass = one["password"]
    if (old_pass == old_password):
        prev = {"email": email}
        nextt = {"$set": {"password": new_password}}
        collection.update_one(prev, nextt)
    else: print("old password incorrect")

def history(email):
    one = collection.find_one({"email": email})
    movieL = one["movieList"]
    return (movieL)

def llike(email, movie_name):
    one = collection.find_one({"email": email})
    like_list = one['like']
    if (movie_name in like_list):
        print("movie already liked")
        return (-1)
    like_list.append(movie_name)
    prev = {"email": email}
    nextt = {"$set": {"like": like_list}}
    collection.update_one(prev, nextt)
    print("movie liked successfully")
    return (1)

def unlike(email, movie_name):
    one = collection.find_one({"email": email})
    like_list = one['like']
    if (movie_name not in like_list):
        print("Unable to select option. Movie has not been liked")
        pass
    like_list.remove(movie_name)
    prev = {"email": email}
    nextt = {"$set": {"like": like_list}}
    collection.update_one(prev, nextt)

def extract_movie_ratings(movie_name):
    present = collection_rating.find_one({"movie": movie_name})
    rating_map = present["rating_map"]
    print(rating_map)
    return (rating_map)

def rating_true_false(email,movie_name):
    present = collection_rating.find_one({"movie": movie_name})
    if(present is None): return(-1)
    if(email in present["rating_map"]):
        print("movie is already rated by you")
        return(1)
    else: return(-1)

def like_true_false(email,movie_name):
    one = collection.find_one({"email": email})
    like_list = one['like']
    if(movie_name in like_list):
        print("movie already liked")
        return(1)
    else: return(0)

def add_ratings2(email, movie_name, rating, review):
    present = collection_rating.find_one({"movie": movie_name})
    print(present)
    if(present == None):
        rating_map={}
        rating_map[email] = [rating,review]
        collection_rating.insert_one({"movie": movie_name, "rating_map": rating_map})
    else:
        new_rating_map = present["rating_map"]
        new_rating_map[email] = [rating, review]
        prev = {"movie": movie_name}
        nextt = {"$set":{"rating_map": new_rating_map}}
        collection_rating.update_one(prev,nextt)

def update_ratings2(email,movie_name,rating,review):
    present = collection_rating.find_one({"movie": movie_name})
    new_rating_map = present["rating_map"]
    new_rating_map[email] = [rating,review]
    prev = {"movie": movie_name}
    nextt = {"$set":{"rating_map": new_rating_map}}
    collection_rating.update_one(prev,nextt)

def removeMovieList(email,movie_name):
    one = collection.find_one({"email": email})
    movieL = one["movieList"]
    movieL.remove(movie_name)
    prev = {"email": email}
    nextt = {"$set":{"movieList": movieL}}
    collection.update_one(prev,nextt)

def extract_person_movie_ratings(email):
    rated_dict={}
    for document in collection_rating.find():
        rating_map = document['rating_map']
        if(email in rating_map):
            rated_movie = document['movie']
            rated_dict[rated_movie] = rating_map[email]
    print(rated_dict)
    return(rated_dict)

def country(movie):
    for i in range(85855):
        if data.index[i] == movie: return data['Country'].iloc[i]
    return "No info"

def langu(movie):
    for i in range(85855):
        if data.index[i] == movie: return data['Language'].iloc[i]
    return "No info"

def rating(movie):
    for i in range(85855):
        if data.index[i] == movie: return data['Rating'].iloc[i]
    return -1

def year(movie):
    for i in range(85855):
        if data.index[i] == movie: return data['Year'].iloc[i]
    return -1

def get_index_from_title(dff,title):
    for i in range(len(dff.index)):
        if dff.index[i] == title: return i
    return -1

def get_title_from_index(dff,index):
    i = int(index)
    return dff.index[i]

def recomendations(movie):
    print(movie)
    Country = country(movie)
    print(Country)
    Language = langu(movie)
    print(Language)
    r = rating(movie)
    print(rating)
    y = year(movie)
    yy = y - 10
    r1 =0
    r2 =0
    if r+2 > 10:
        r1+= r
        r2+= r-2
    elif r-2 < 0:
        r1+= r+2
        r2+= 0
    else:
        r1+= r+2
        r2+= r-2
    dff = data[data['Country'] == Country]
    #print(dff.head())
    dff = dff[dff['Language'] == Language]
    #print(dff.head())
    dff = dff[dff['Rating']>=r2]
    #print(dff.head())
    dff = dff[dff['Rating']<=r1]
    #print(dff.head())
    dff = dff[dff['Year']>=yy]
    dff['soup'] = dff['Genre']+','+dff['Director']
    print(dff['soup'])
    if len(dff['soup']) == 0:
        return
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(dff['soup'])
    cosine_sim = cosine_similarity(count_matrix)
    movie_index = get_index_from_title(dff,movie)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
    movie_index = sorted_similar_movies[:10]
    movies = []
    for i in movie_index: movies.append(get_title_from_index(dff,i[0]))
    return movies

def getid(movie):
    ans = []
    for i in range(85855):
        if df['original_title'].iloc[i] == movie: ans.append(i)
    ind = ans[0]
    id = df['imdb_title_id'].iloc[ind]
    return id

def getmovies(word):
    movies = []
    for i in range(85855):
        l = df['actors'].iloc[i]
        l = str(l)
        if (l.find(word) != -1): movies.append(df['original_title'].iloc[i])
    return movies

def getmovies_director(word):
    movies = []
    for i in range(85855):
        l = df['director'].iloc[i]
        l = str(l)
        if (l.find(word) != -1): movies.append(df['original_title'].iloc[i])
    return movies

def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

def get_year(movie):
    ans = []
    for i in range(85855):
        if df['original_title'].iloc[i] == movie: ans.append(i)
    ind = ans[0]
    id = df['year'].iloc[ind]
    return id

def get_ratings(movie):
    for i in range(85855):
        if df['original_title'].iloc[i] == movie: return df['avg_vote'].iloc[i]
    return 0

def get_lan(movie):
    ans = []
    for i in range(85855):
        if ddf['original_title'].iloc[i] == movie: ans.append(i)
    ind = ans[0]
    id = ddf['Language'].iloc[ind]
    return id

def get_soup(movie):
    ans = []
    for i in range(85855):
        if ddf['original_title'].iloc[i] == movie: ans.append(i)
    ind = ans[0]
    id = ddf['soup'].iloc[ind]
    return id

def checkemail(e):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, e)):
        return True
    return False

def get_image(movie_id):
    print(movie_id)
    try:
        headers = {"Accept-Language": "en-US, en;q=0.5"}
        url = "https://www.imdb.com/title/"+movie_id+"/"

        results_poster_url = requests.get(url, headers=headers) 
        soup_poster_url = BeautifulSoup(results_poster_url.text, "html.parser")
        
        poster_url = soup_poster_url.find_all('div', class_="ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width Poster__CelPoster-sc-6zpm25-0 kPdBKI celwidget ipc-sub-grid-item ipc-sub-grid-item--span-2")
        poster_url = str(poster_url[0].a)
        poster_url = poster_url[83:]
        poster_url = poster_url[:poster_url.find('/?')]
        poster_url = "http://www.imdb.com/"+poster_url

        results_media_url = requests.get(poster_url, headers=headers) 
        soup_media_url = BeautifulSoup(results_media_url.text, "html.parser")
        poster_media_url = soup_media_url.find_all('img',class_="MediaViewerImagestyles__PortraitImage-sc-1qk433p-0 bnaOri")

        poster_media_url = str(poster_media_url[0])
        poster_media_url = poster_media_url[poster_media_url.find('srcset=')+8:]
        poster_media_url = poster_media_url[:poster_media_url.find('.jpg')+4]
        
        image = poster_media_url
    except IndexError:
        image = ""
    return image

def rating_recommendation(movie):
    id = getid(movie)
    r = table[id][:-2]
    movie_lang = table[id][-1]
    movies = []
    pc = []
    pv = []
    lang = []
    for i in table.columns:
        if 'tt' in i:
            k = table[i][:-2]
            p_cc, p_v = stats.pearsonr(r, k)
            movies.append(table[i][-2])
            p_c = abs(p_cc)
            pc.append(p_cc)
            pv.append(p_v)
            lang.append(table[i][-1])
        else: pass
    vt = zip(movies, pc, pv, lang)
    df2 = pd.DataFrame(vt)
    df2.columns = ['Movie', 'P_c', 'P_v', 'Language']
    rslt_df = df2.sort_values(by=['P_c', 'P_v'], ascending=False)
    rslt_df = rslt_df[rslt_df['Language'] == movie_lang]
    ans = rslt_df['Movie'].tolist()
    fans = ans[1:6]
    return fans

def genremovies(genre):
    movies= []
    for i in range(len(genre_tables.index)):
        l = genre_tables['Genre'].iloc[i]
        if l.find(genre)!= -1:
            if genre_tables['Language'].iloc[i] == lang[0]: movies.append(genre_tables.index[i])
            if genre_tables['Language'].iloc[i] == lang[1]: movies.append(genre_tables.index[i])
    return random.sample(movies, 10)

def SignUp(request):
    return render(request,'signup_movie.html')

def SignUpcheck(request):
    movielist = []
    genrelist = []
    name = request.GET['Name']
    Email = request.GET['Email']
    Password = request.GET['Password']
    phNo = request.GET['phone']
    phoneno = []
    check = checkemail(Email)
    m1= request.GET['movie1']
    movielist.append(m1)
    m2 = request.GET['movie2']
    movielist.append(m2)
    m3 = request.GET['movie3']
    movielist.append(m3)
    m4 = request.GET['movie4']
    movielist.append(m4)
    m5 = request.GET['movie5']
    movielist.append(m5)
    g1 = request.GET['genre1']
    genrelist.append(g1)
    g2 = request.GET['genre2']
    genrelist.append(g2)
    g3 = request.GET['genre3']
    genrelist.append(g3)
    if check == False:
        return HttpResponse('Invalid Email')
    for i in range(len(phNo)):
        if phNo[i] == ',':
            if len(phNo[:i]) == 10:
                phoneno.append(phNo[:i])
    if phNo[len(phNo) - 10:len(phNo)] not in phoneno and len(phNo[len(phNo) - 10:len(phNo)]) == 10:
        phoneno.append(phNo[len(phNo) - 10:len(phNo)])
    for i in phoneno:
        if i.isnumeric() == False:
            return HttpResponse('Invalid Phone Number')

    signup(name,Email,Password, movielist,genrelist)

    return render(request,'signup_movie.html')

def Login_check(request):
    global email
    s=""
    email = request.GET['emailid']
    passwd = request.GET['passwd']
    check = login(email, passwd)
    if check == False:
        s+="Login Failed. Password/email correct"
        return render(request,'signup_movie.html',{"invalid":s})
    return render(request,'Disclamer.html')

def change_pass(request):
    
    old_pass = request.GET['old_pass']
    new_pass = request.GET['new_pass']
    
    one = collection.find_one({"email": email})
    old_password = one["password"]
    if old_pass==old_password:
        prev = {"email": email}
        nextt = {"$set":{"password": new_pass}}
        collection.update_one(prev,nextt)
        return render(request,'signup_movie.html')
    return HttpResponse("Error: check if old password is correct or new password is not same as the old password")
    
    """
    confirmation = password_change(email,old_pass, new_pass)
    if confirmation == 1:
        return HttpResponse("Error: check if old password is correct or new password is not same as the old password")
    print(confirmation)
    return render(request,'change_pass.html',{'check': confirmation})
    """
    

def change_pass_pg(request):
    return render(request,'change_pass.html')

def home(request):
    recommend_list = []
    mm = history(email)
    movies= random.sample(mm, 5)
    print(movies)
    #movies = random.sample(movies_list, 5)
    for i in movies:
        l = recomendations(i)
        recommend_list += l

    recommend_list = set(recommend_list)
    recommend = random.sample(recommend_list, 10)
    m1 = []
    m2 =[]
    m3 =[]
    m4 = []
    genremovies1 = genremovies(Genre[0])
    genremovies2 = genremovies(Genre[1])
    genremovies3 = genremovies(Genre[2])
    for i in recommend:
        m = []
        m.append(i)
        link = get_image(getid(i))
        m.append(link)
        m1.append(m)
    for i in genremovies1:
        m = []
        m.append(i)
        link = get_image(getid(i))
        m.append(link)
        m2.append(m)
    for i in genremovies2:
        m = []
        m.append(i)
        link = get_image(getid(i))
        m.append(link)
        m3.append(m)
    for i in genremovies3:
        m = []
        m.append(i)
        link = get_image(getid(i))
        m.append(link)
        m4.append(m)
    return render(request,'home.html',{"genre1":Genre[0],"genre2":Genre[1],"genre3":Genre[2],
    "movies1": m1,"movies2":m2,"movies3":m3,"movies4":m4})

def ExtractPoster_BG(movie_id,director_id,director_name):

    cast_arr = []
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    url = "https://www.imdb.com/title/tt"+movie_id+"/"
    print(url)
    results = requests.get(url, headers=headers) 
    soup = BeautifulSoup(results.text, "html.parser")
    
    bg_url = soup.find_all('div', class_="ipc-media ipc-media--slate-16x9 ipc-image-media-ratio--slate-16x9 ipc-media--baseAlt ipc-media--slate-m ipc-slate__slate-image ipc-media__img")
    try:
        bg_url = str(bg_url[0])
        bg_url = bg_url[bg_url.find('src="')+5:]
        bg_url = bg_url[:bg_url.find('.jpg')+4]
    except KeyError:
        bg_url = ""
    
    cast_soup = soup.find_all('div', class_="ipc-media ipc-media--avatar ipc-image-media-ratio--avatar ipc-media--base ipc-media--avatar-m ipc-media--avatar-circle ipc-avatar__avatar-image ipc-media__img")   
    for i in range(8):
        single_cast = []
        cast = str(cast_soup[i])
        name = cast[cast.find('<img alt="')+10:]
        name = name[:name.find('"')]
        single_cast.append(name)
        img = cast[cast.find('src="')+5:]
        img = img[:img.find('"')]
        single_cast.append(img)
        cast_arr.append(single_cast)
        
    poster_url = soup.find_all('div', class_="ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width Poster__CelPoster-sc-6zpm25-0 kPdBKI celwidget ipc-sub-grid-item ipc-sub-grid-item--span-2")
    poster_url = str(poster_url[0].a)
    poster_url = poster_url[83:]
    poster_url = poster_url[:poster_url.find('/?')]
    poster_url = "http://www.imdb.com/"+poster_url

    results_media_url = requests.get(poster_url, headers=headers) 
    soup_media_url = BeautifulSoup(results_media_url.text, "html.parser")
    poster_media_url = soup_media_url.find_all('img',class_="MediaViewerImagestyles__PortraitImage-sc-1qk433p-0 bnaOri")

    poster_media_url = str(poster_media_url[0])
    poster_media_url = poster_media_url[poster_media_url.find('srcset=')+8:]
    poster_media_url = poster_media_url[:poster_media_url.find('.jpg')+4]
    
    director = []
    director.append(director_name)
    url_director = "https://www.imdb.com/name/nm"+director_id+"/"
    results_director = requests.get(url_director, headers=headers) 
    soup_director = BeautifulSoup(results_director.text, "html.parser")
    director_soup = soup_director.find_all('div', class_="image")
    director_url = str(director_soup[0])
    director_url = director_url[director_url.find('href="')+6:]
    director_url = director_url[:director_url.find('"')]
    director_url = "https://www.imdb.com"+director_url
    
    results_director = requests.get(director_url, headers=headers) 
    soup_director = BeautifulSoup(results_director.text, "html.parser")

    cast_director = soup_director.find_all('div', class_=["MediaViewerImagestyles__LandscapeContainer-sc-1qk433p-3 kXRNYt","MediaViewerImagestyles__PortraitContainer-sc-1qk433p-2 iUyzNI"])

    for img in cast_director:
        img = str(img)
        img_id = img[img.find('data-image-id="')+15:]
        img_id = img_id[:img_id.find('"')]
        img_id = img_id[-4:]
        if img_id == 'curr':
            img = img[img.find('src="')+5:]
            img = img[:img.find('"')]
            director.append(img)
            cast_arr.insert(0,director)
            break
    
    return poster_media_url, bg_url, cast_arr

def extractTrailer_watchlink(movie_name, movie_year):
    movie_name = str(movie_name)
    movie_year = str(movie_year)
    
    movie_name = movie_name.replace(" ", "+")
    url = 'https://google.com/search?q='+movie_name+'+('+movie_year+')'
    print(url)
    session = HTMLSession()
    r= session.get(url) 

    trailer = r.html.find('div[class="wDYxhc NFQFxe"]')
    trailer = trailer[0].html
    trailer = trailer[trailer.find('href="')+6:]
    trailer = trailer[:trailer.find('"')]
    trailer = trailer[trailer.find('watch?v=')+8:]
    trailer = 'https://www.youtube.com/embed/' + trailer
    
    url = r.html.find('div[class="fOYFme"]')
    url = url[0].html
    url = url[url.find('href="')+6:]
    url = url[:url.find('"')]
    
    return trailer,url

def getrecommendationsbysearch(request):    

    name = request.GET['q']
    updateMovieList(email, name)
    ia = imdb.IMDb()
    search = ia.search_movie(name)[0]
    movie = ia.get_movie(search.movieID)

    if movie.data['year'] is not None: year = movie.data['year']
    else: year = "Data Not Avaliable"

    if movie.data['genres'] is not None: genre = movie.data['genres']
    else: genre = "Data Not Avaliable"

    if movie.data['plot outline'] is not None: plot = movie.data['plot outline']
    else: plot = "Data Not Avaliable"

    if movie.data['directors'] is not None:
        dir_id = movie.get('directors')[0].personID
        dir_name = movie.get('directors')[0]['name']
        poster,bg,cast_arr = ExtractPoster_BG(search.movieID,dir_id,dir_name)
    else: pass

    if movie.data['rating']: rating = movie.data['rating']
    else: rating = "Data Not Avaliable"

    trailer,watch = extractTrailer_watchlink(name, year)
    runtime=""
    try:
        runtime+= movie.data['runtimes'][0]
        runtime+= ' min'
    except KeyError:
        runtime+=""

    cert_arr = movie.get('certificates')
    cert = "Not Rated"
    for country in cert_arr:
        if country.startswith('United States'):
            if country.endswith(')'):
                pass
            else:
                country = country[country.find(':')+1:]
                cert = country

    recmovies = rating_recommendation(name)
    m1 = []

    for i in recmovies:
        m = []
        m.append(i)
        link = get_image(getid(i))
        m.append(link)
        m1.append(m)

    return render(request, 'recommendation.html',
                  {'movie': name, "year": year, "ImageBG": bg, "poster": poster, "cast": cast_arr, "genre": genre, "plot": plot,
                    "Ratings": rating, "movies1": m1, "trailer": trailer, "watch": watch,"Runtime":runtime,"Cert":cert})

def user_ratings(movie_id):
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    url = "http://www.imdb.com/title/tt"+movie_id+"/reviews?start=0"
    results_trailer = requests.get(url, headers=headers) 
    soup_trailer = BeautifulSoup(results_trailer.text, "html.parser")
    stars = soup_trailer.find_all('div', class_="ipl-ratings-bar")
    reviews = soup_trailer.find_all('div', class_="text show-more__control")
    ratings = []
    rreview = []
    maximum = max(len(stars),len(reviews)) 
    for i in range(maximum):
        rrreview = []
        try:
            star = str(stars[i])
            star = star[star.find('<path d="M0 0h24v24H0z" fill="none"></path>\n</svg>\n<span>'):]
            star1 = star[57]
            star1check = star[58]
            check=""
            star2=""
            if star1check == '0':
                star1+='0'
                check+='1'
            if check=='1':
                star2+= star[92:95]
            else:
                star2+= star[91:94]
            rating = star1+star2
            rrreview.append(rating)
        except IndexError:
            rrreview.append("No rating given")
        try:
            review = str(reviews[i])
            review = review[37:]
            review = review.replace("</div>","")
            #print(review)
            rrreview.append(review)
        except IndexError:
            rrreview.append("No review given")
        ratings.append(rrreview)
    
    return ratings

def ratingpage(request):
    name = request.GET['q']
    ia = imdb.IMDb()
    search = ia.search_movie(name)[0]
    movie_ID = search.movieID
    
    rrating = user_ratings(movie_ID)
    rating = ""
    r= ""
    if rating_true_false(email,name) == 1:
        rating+= extract_movie_ratings(name)
        return render(request,'check.html',{"movie":name,"Rating":rating,"Review":r})
    return render(request,'review.html',{"movie":name,"Reviews":rrating})

def ratingcheckpage(request):
    name = request.GET['q']
    rmovies.remove(name)
    return render(request,'review.html',{"movie":name})

def like_dislike(request):
    name = request.GET['q']
    m=[]
    like_return = request.GET['rating']
    like_return = int(like_return)
    review = request.GET['review']
    if like_return >=7:
        if like_true_false(email,name) == 1: pass
        else: llike(email,name)
        updateMovieList(email,name)
    else:
        if name in dislike: pass
        else: dislike.append(name)
        if name in like: unlike(email,name)
        if name in movies_list: removeMovieList(email,name)

    if rating_true_false("akul.mangal@gmail.com", name) == 1: update_ratings2(email, name, like_return, review)
    else: add_ratings2(email, name, like_return, review)
    str="Your rating has been submitted"
    return render(request, 'review.html',{"Like":str,"movie":name})

def getrecommendationsbychoice(request):
    val1=[]
    val2=[]
    color1 =[]
    color2=[]
    name = request.GET['movie']
    updateMovieList(email, name)
    ia = imdb.IMDb()
    search = ia.search_movie(name)[0]
    movie = ia.get_movie(search.movieID)

    if movie.data['year'] is not None: year = movie.data['year']
    else: year = "Data Not Avaliable"

    if movie.data['genres'] is not None: genre = movie.data['genres']
    else: genre = "Data Not Avaliable"

    if movie.data['plot outline'] is not None: plot = movie.data['plot outline']
    else: plot = "Data Not Avaliable"

    if movie.data['directors'] is not None:
        dir_id = movie.get('directors')[0].personID
        dir_name = movie.get('directors')[0]['name']
        poster,bg,cast_arr = ExtractPoster_BG(search.movieID,dir_id,dir_name)
    else: pass

    if movie.data['rating']: rating = movie.data['rating']
    else: rating = "Data Not Avaliable"

    trailer,watch = extractTrailer_watchlink(name, year)
    runtime=""
    try:
        runtime+= movie.data['runtimes'][0]
        runtime+= ' min'
    except KeyError:
        runtime+=""

    cert_arr = movie.get('certificates')
    cert = "Not Rated"
    for country in cert_arr:
        if country.startswith('United States'):
            if country.endswith(')'):
                pass
            else:
                country = country[country.find(':')+1:]
                cert = country

    recmovies = rating_recommendation(name)
    m1 = []

    for i in recmovies:
        m = []
        m.append(i)
        link = get_image(getid(i))
        m.append(link)
        m1.append(m)

    return render(request, 'recommendation.html',
                  {'movie': name, "year": year, "ImageBG": bg, "poster": poster, "cast": cast_arr, "genre": genre, "plot": plot,
                    "Ratings": rating, "movies1": m1, "trailer": trailer, "watch": watch,"Runtime":runtime,"Cert":cert})
                    
def ratingpage2(request):
    name = request.GET['movie']
    ia = imdb.IMDb()
    search = ia.search_movie(name)[0]
    movie_ID = search.movieID
    
    rrating = user_ratings(movie_ID)
    rating=""
    r=""
    if rating_true_false(email, name) == 1:
        dict1 = extract_movie_ratings(name)[email]
        rating += str(dict1[0])
        r+= dict1[1]
        return render(request, 'check2.html', {"movie": name, "Rating": rating, "Review": r})
    return render(request,'review2.html',{"movie":name,"Reviews":rrating})

def ratingcheckpage2(request):
    name = request.GET['movie']
    #rmovies.remove(name)
    return render(request,'review2.html',{"movie":name})

def like_dislike2(request):
    name = request.GET['movie']
    m = []
    like_return = request.GET['rating2']
    like_return = int(like_return)
    review = request.GET['review2']
    if like_return >= 7:
        if like_true_false(email, name) == 1: pass
        else: llike(email, name)
        updateMovieList(email,name)
    else:
        if name in dislike: pass
        else: dislike.append(name)
        if like_true_false(email, name) == 1: unlike(email, name)
        if name in movies_list: removeMovieList(email, name)

    if rating_true_false(email, name) == 1: update_ratings2(email, name, like_return, review)
    else: add_ratings2(email, name, like_return, review)
    str = "Your rating has been submitted"
    return render(request, 'review2.html',{"Like": str,"movie":name})

headers = {"Accept-Language": "en-US, en;q=0.5"}
def extractKnownFor(person_id):
    knownFor_arr = []
    
    url = "https://www.imdb.com/name/nm"+person_id+"/"
    results_cast = requests.get(url, headers=headers) 
    soup_cast = BeautifulSoup(results_cast.text, "html.parser")

    cast_soup = soup_cast.find_all('div', class_="uc-add-wl-widget-container")

    for i in range(4):
        movie = []
        cast = str(cast_soup[i])
        img = cast[cast.find('src="')+5:]
        img = img[:img.find('"')]
        
        name = cast[cast.find('<img alt="')+10:]
        name = name[:name.find('"')]
        movie.append(name)
        
        knownFor_arr.append(movie)
        movie.append(img)
        
    return knownFor_arr

def getdetails(request):
    name = request.GET['name']
    ia = imdb.IMDb()
    search = ia.search_person(name)
    search = search[0]
    search = search.personID
    actor = ia.get_person(search)

    try:
        history = actor.get('biography')
        history = str(history[0])
    except KeyError:
        history="Biography"
    try:
        image = ia.get_person_filmography(search)['data']['headshot']
    except KeyError: image=""

    search_info = ia.get_person(search)
    actor_results = ia.get_person_filmography(search)

    try: name = search_info['name']
    except: name="Not available"

    try: Dob = search_info['birth date']
    except: Dob = "Not available"

    try: birthName = actor.get('birth name')
    except: birthName = "Not available"

    try: nickname = actor.get('nick names')
    except: nickname = "Not available"

    try: place = actor_results['data']['birth info']['birth place']
    except: place="Not available"

    try: KnownFor = extractKnownFor(search)
    except: KnownFor = "Not available"


    movielist = getmovies(name)
    m1 = []
    for i in movielist:
        m = []
        m.append(i)
        link = get_ratings(i)
        if link == 0:
            try:
                movies_list.append(i)
                ia = imdb.IMDb()
                search = ia.search_movie(i)[0]
                movie = ia.get_movie(search.movieID)
                rating = movie.data['rating']
            except: rating = "Rating not Avaliable"
            if rating == "Rating not Avaliable": link= "Rating not Avaliable"
            else: link = rating
        m.append(link)
        m1.append(m)

    return render(request, 'people.html',
                  {'name': name, "History": history, "Dob": Dob, "Image": image, "Place": place, "movies": m1,"Like":like,"Known_For":KnownFor, "birthName":birthName,"nickname":nickname})

def director(request):
    name = request.GET['director']
    ia = imdb.IMDb()
    search = ia.search_person(name)
    search = search[0]
    search = search.personID
    actor = ia.get_person(search)

    try:
        history = actor.get('biography')
        history = str(history[0])
    except KeyError:
        history="Biography"
    try:
        image = ia.get_person_filmography(search)['data']['headshot']
    except KeyError:
        image=""
    search_info = ia.get_person(search)
    actor_results = ia.get_person_filmography(search)
    try:
        name = search_info['name']
    except:
        name="Not available"
    try:
        Dob = datetime.datetime.strptime(search_info.get('birth date'), '%Y-%m-%d').strftime('%d %B, %Y')
    except:
        Dob = "Not available"

    try: birthName = actor.get('birth name')
    except: birthName = "Not available"

    try: nickname = actor.get('nick names')
    except: nickname = "Not available"

    try:
        place = actor_results['data']['birth info']['birth place']
    except:
        place="Not available"

    try: KnownFor = extractKnownFor(search)
    except: KnownFor = "Not available"
    
    movielist = getmovies_director(name)
    m1 = []
    for i in movielist:
        m = []
        m.append(i)
        link = get_ratings(i)
        if link == 0:
            try:
                movies_list.append(i)
                ia = imdb.IMDb()
                search = ia.search_movie(i)[0]
                movie = ia.get_movie(search.movieID)
                rating = movie.data['rating']
            except:
                rating = "Rating not Avaliable"
            if rating == "Rating not Avaliable":
                link= "Rating not Avaliable"
            else:
                link = rating
        m.append(link)
        m1.append(m)

    return render(request, 'directors.html',
                  {'name': name, "History": history, "Dob": Dob, "Image": image, "Place": place, "movies": m1,"Like":like,"Known_For":KnownFor, "birthName":birthName,"nickname":nickname})

def Settings(request): return render(request,'settings.html')

def History(request):
    m=[]
    movie = history(email)
    for i in range(len(movie)):
        mm = []
        mm.append(movie[i])
        mm.append(rating(movie[i]))
        mm.append(year(movie[i]))
        m.append(mm)
    return render(request,'history.html',{'movies':m})

def Reviews(request):
    m=[]
    movie = extract_person_movie_ratings(email)
    keys = movie.keys()
    for i in keys:
        mm=[]
        r= movie[i]
        rr = r[0]
        rrr = r[1]
        mm.append(i)
        mm.append(rr)
        mm.append(rrr)
        m.append(mm)

    return render(request,'Rating.html',{'movies':m})