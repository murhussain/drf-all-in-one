from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from movie.api.pagination import WatchlistPagination, WatchlistCursorPagination
from movie.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from movie.models import WatchList, StreamPlatform, Review
from movie.api.serializers import (WatchListSerializer, StreamPlatformSerializer,
                                   ReviewSerializer)
from movie.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle

# Much more about filtering, Search and Ordering

"""Here we are overriding get_queryset() function, 
they need to create a form and user a post request to get all 
reviews associated to a particular user. Simply
This called 'FILTERING AGAINST URL' """


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)


"""Here we are passing parameter in the URL to get all 
reviews associated to a particular user. Simply
This called 'FILTERING AGAINST PASSING PARAMETER' """


class UserReview2(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


"""Here we are passing parameter in the URL to FILTER 
movies associated to a particular title or platform__name. Simply
This called 'FILTERING AGAINST FILTER_BACKENDS' """


class WatchListListAPIView(generics.ListAPIView):
    serializer_class = WatchListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'platform__name']

    def get_queryset(self):
        return WatchList.objects.all()


"""Here we are passing parameter in the URL to SEARCH 
movies associated to a particular title or platform__name. Simply
This called 'FILTERING AGAINST SEARCH_FILTER' """


class WatchSearchListAPIView(generics.ListAPIView):
    serializer_class = WatchListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title', 'platform__name']
    # pagination_class = WatchlistPagination
    pagination_class = WatchlistCursorPagination

    def get_queryset(self):
        return WatchList.objects.all()


"""Here we are passing parameter in the URL to ORDERING 
movies associated to a particular title or platform__name. Simply
This called 'FILTERING AGAINST ORDERING_FILTER' """


class WatchOrderingListAPIView(generics.ListAPIView):
    serializer_class = WatchListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']
    pagination_class = WatchlistPagination

    def get_queryset(self):
        return WatchList.objects.all()


# End of filtering, Search and Ordering
class StreamPlatformViewset(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]


class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)

        user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=user)

        if review_queryset.exists():
            raise ValidationError("You've already reviewed this movie")

        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2

        movie.number_rating += 1
        movie.save()

        serializer.save(watchlist=movie, review_user=user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # Defining throttle inside view without creating a separate file
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class StreamPlatformAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
