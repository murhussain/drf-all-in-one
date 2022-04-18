from django.urls import path, include
from rest_framework.routers import DefaultRouter

from movie.api.views import (WatchListAPIView, WatchDetailAPIView,
                             StreamPlatformAPIView, StreamPlatformDetailAPIView,
                             WatchListListAPIView, ReviewDetail, CreateReview, StreamPlatformViewset,
                             UserReview, UserReview2, ReviewList,
                             WatchSearchListAPIView, WatchOrderingListAPIView)

router = DefaultRouter()
router.register('stream', StreamPlatformViewset, basename='streams')

urlpatterns = [
    path('movies/', WatchListAPIView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', WatchDetailAPIView.as_view(), name='movie_detail'),

    path('', include(router.urls)),
    path('stream/', StreamPlatformAPIView.as_view(), name='stream'),
    path('stream/<int:pk>/', StreamPlatformDetailAPIView.as_view(), name='streamDetail'),

    path('movie/<int:pk>/review-create', CreateReview.as_view(), name='review_create'),
    path('movie/<int:pk>/review-list/', ReviewList.as_view(), name='review_list'),
    path('movie/review-detail/<int:pk>/', ReviewDetail.as_view(), name='review_detail'),

    # Filtering, Search and pagination
    path('reviews/<str:username>', UserReview.as_view(), name='user-review-detail'),
    path('reviews/', UserReview2.as_view(), name='user-reviewParam-detail'),
    path('watch-list/', WatchListListAPIView.as_view(), name='watch_list'),
    path('watch-list/search/', WatchSearchListAPIView.as_view(), name='watch_list-search'),
    path('watch-list/ordered/', WatchOrderingListAPIView.as_view(), name='watch_list-ordered'),
]