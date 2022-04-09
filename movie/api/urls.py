from django.urls import path, include
from movie.api.views import WatchListAPIView, WatchDetailAPIView, StreamPlatformAPIView, StreamPlatformDetailAPIView


urlpatterns = [
  path('watch/', WatchListAPIView.as_view(), name='movie_list'),
  path('watch/<int:pk>', WatchDetailAPIView.as_view(), name='movie_detail'),
  path('stream/', StreamPlatformAPIView.as_view(), name='stream'),
  path('stream/<int:pk>', StreamPlatformDetailAPIView.as_view(), name='streamDetail', )
]
