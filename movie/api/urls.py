from django.urls import path, include
from movie.api.views import (WatchListAPIView, WatchDetailAPIView,
                             StreamPlatformAPIView, StreamPlatformDetailAPIView,
                             ReviewList, ReviewDetail, CreateReview)


urlpatterns = [
    path('movies/', WatchListAPIView.as_view(), name='movie_list'),
    path('movie/<int:pk>', WatchDetailAPIView.as_view(), name='movie_detail'),
    path('stream/', StreamPlatformAPIView.as_view(), name='stream'),
    path('stream/<int:pk>', StreamPlatformDetailAPIView.as_view(), name='streamDetail'),

    path('movie/<int:pk>/review-create', CreateReview.as_view(), name='review_create'),
    path('movie/<int:pk>/review-list', ReviewList.as_view(), name='review_list'),
    path('movie/review-detail/<int:pk>', ReviewDetail.as_view(), name='review_detail'),
]
