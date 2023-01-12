
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views
from . import recommender

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', recommender.SignUp, name='home'),
    path('Login/',recommender.Login_check, name='login'),
    path('SignUp/', recommender.SignUpcheck, name='signup'),
    path('Home/',recommender.home, name='HomePage'),
    path('recommendations/', recommender.getrecommendationsbysearch, name='recommendations'),
    path('review_page/',recommender.ratingpage,name='ratings'),
    path('review_checkpage/',recommender.ratingcheckpage,name='checkratings'),
    path('review_checkpage2/', recommender.ratingcheckpage2, name='checkratings2'),
    path('review_page2/',recommender.ratingpage2,name='ratings2'),
    path('likedislike1/', recommender.like_dislike, name='ld1'),
    path('recommendations2/', recommender.getrecommendationsbychoice, name='recommendations2'),
    path('likedislike2/', recommender.like_dislike2, name='ld2'),
    path('settings/', recommender.Settings, name='Setting'),
    path('History/', recommender.History, name='History'),
    path('Rating/', recommender.Reviews, name='Rating'),
    path('People/', recommender.getdetails, name='People'),
    path('Director/', recommender.director, name='Director'),
    path('ChangePass/', recommender.change_pass, name = 'changePass'),
    path('passChange/', recommender.change_pass_pg, name = 'passChange'),
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)