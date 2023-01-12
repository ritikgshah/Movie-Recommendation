from django.shortcuts import render
from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import random

df = pd.read_csv("IMDb movies.csv")
df = df.replace(np.nan,"Nan",regex =True)
languages = df['language'].tolist()
language = []
for ll in languages:
    if ',' in ll:
        lan = ll.split(',')
        lan = lan[0]
    else:
        lan = ll
    language.append(lan)

df['Language'] = language

df['Language'] = language
df3 = zip(df['original_title'].tolist(),df['genre'].tolist(),df['actors'].tolist(),df['director'].tolist(),df['Language'].tolist(),df['country'].tolist(),df['avg_vote'].tolist(),df['year'].tolist())
data = pd.DataFrame(df3)
data.columns = ['Title','Genre','Cast','Director','Language','Country','Rating','Year']
data = data.set_index('Title')
movies_list =["Alien","Cast Away","Batman Begins","Inception","No Smoking"]
global recommend
recommend = []
def country(movie):
    for i in range(85855):
        if data.index[i] == movie:
            return data['Country'].iloc[i]
    return "No info"
def lan(movie):
    for i in range(85855):
        if data.index[i] == movie:
            return data['Language'].iloc[i]
    return "No info"

def rating(movie):
    for i in range(85855):
        if data.index[i] == movie:
            return data['Rating'].iloc[i]
    return -1
def year(movie):
    for i in range(85855):
        if data.index[i] == movie:
            return data['Year'].iloc[i]
    return -1

def get_index_from_title(dff,title):
    for i in range(len(dff.index)):
        if dff.index[i] == title:
            return i
    return -1
def get_title_from_index(dff,index):
    i = int(index)
    return dff.index[i]

def recomendations(movie):
    Country = country(movie)
    Language = lan(movie)
    r = rating(movie)
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
    dff = dff[dff['Language'] == Language]
    dff = dff[dff['Rating']>=r2]
    dff = dff[dff['Rating']<=r1]
    dff = dff[dff['Year']>=yy]
    dff['soup'] = dff['Genre']+','+dff['Director']
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(dff['soup'])
    cosine_sim = cosine_similarity(count_matrix)
    movie_index = get_index_from_title(dff,movie)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
    movie_index = sorted_similar_movies[:10]
    movies = []
    for i in movie_index:
        movies.append(get_title_from_index(dff,i[0]))
    return movies


def home(request):
    movies = random.sample(movies_list, 5)
    for i in movies:
        l = recomendations(i)
        recommend += l
    return render(request,'home.html',{"movies":movies_list,"recommend":recommend})

# Create your views here.
