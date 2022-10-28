from dataclasses import fields
from pickletools import read_long1
from wsgiref.validate import validator
from numpy import source
from rest_framework import serializers
from watchlist.models import WatchList,StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):

    review_user=serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model=Review
        exclude=['watchlist']


class WatchListSerializer(serializers.ModelSerializer):

    platform=serializers.CharField(source='platform.name')
    
    class Meta:
        model=WatchList
        fields="__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    
    watch_list=WatchListSerializer(many=True, read_only=True)
   
    class Meta:
        model=StreamPlatform
        fields="__all__"