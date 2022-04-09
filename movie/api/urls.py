from django.urls import path, include
from movie.api.views import movie_list, movie_details


urlpatterns = [
  path('list/', movie_list, name='movie_list'),
  path('<int:pk>', movie_details, name='movie_detail'),
]
