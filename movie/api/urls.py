from django.urls import path, include
from movie.api.views import MovieListAPIView, MovieDetailAPIView


urlpatterns = [
  path('list/', MovieListAPIView.as_view(), name='movie_list'),
  path('<int:pk>', MovieDetailAPIView.as_view(), name='movie_detail'),
]
