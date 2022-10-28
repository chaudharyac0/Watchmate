from multiprocessing import context
from platform import platform
import re
from shutil import move
from django.shortcuts import render,redirect
from requests import Response, delete
from watchlist.api import serializers
from watchlist.models import WatchList,StreamPlatform,Review
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from watchlist.api import permisions
from django.shortcuts import get_object_or_404
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from watchlist.api import throttling
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from user_app.api import pagination
#class based views

class UserReview(generics.ListAPIView):

    serializer_class = serializers.ReviewSerializer
   
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username = username)




class ReviewCreate(generics.CreateAPIView):

    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_querset = Review.objects.filter(watchlist=watchlist,review_user=review_user)

        if review_querset.exists():
            raise ValidationError("You have already reviewd this movie")

        if watchlist.total_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
            
        watchlist.total_rating = watchlist.total_rating + 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist,review_user=review_user)
        

class ReviewList(generics.ListAPIView):
    
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permisions.ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review_detail'


class StreamPlatformVS(viewsets.ModelViewSet):

    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permisions.AdminOrReadOnly]

 
class StreamPlatformAV(APIView):
    
    permission_classes = [permisions.AdminOrReadOnly]

    def get(self,request):
        platform = StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(platform,many=True, context={'request':request})
        return Response(serializer.data)

    def post(self,request):
        serializer = serializers.StreamPlatformSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetail(APIView):

    permission_classes = [permisions.AdminOrReadOnly]

    def get(self,request,pk):
        
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error':'Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.StreamPlatformSerializer(platform, context={'request':request})
        return Response(serializer.data)

    def put(self,request,pk):

        platform = StreamPlatform.objects.get(pk=pk)        
        serializer = serializers.StreamPlatformSerializer(platform, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class WatchListGV(generics.ListAPIView):

    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    pagination_class = pagination.WatchListCPagination
    

class WatchListAV(APIView):

    permission_classes = [permisions.AdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = serializers.WatchListSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchListDetailAV(APIView):

    permission_classes = [permisions.AdminOrReadOnly]

    def get(self,request,pk):

        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error':'MOVIE Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.WatchListSerializer(movie, context={'request':request})
        return Response(serializer.data)

    def put(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)