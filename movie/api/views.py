from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from movie.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from movie.models import WatchList, StreamPlatform, Review
from movie.api.serializers import (WatchListSerializer, StreamPlatformSerializer,
                                   ReviewSerializer)


class StreamPlatformViewset(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer

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
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2

        movie.number_rating += 1
        movie.save()

        serializer.save(watchlist=movie, review_user=user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [AdminOrReadOnly]
    permission_classes = [ReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class StreamPlatformAPIView(APIView):

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
