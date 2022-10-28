from django.db import router
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from watchlist.api.views import (WatchListAV,WatchListDetailAV,
                                 StreamPlatformAV,StreamPlatformDetail,
                                 ReviewList,ReviewDetail,ReviewCreate,
                                 StreamPlatformVS,UserReview,WatchListGV)

router=DefaultRouter()     #Used to combine two or more url link
router.register('stream',StreamPlatformVS,basename='streamplatform')

urlpatterns = [
     
    path('list/',WatchListAV.as_view(),name='movie_list'),
    path('<int:pk>/',WatchListDetailAV.as_view(),name='movie_detail'),
    path('list2/',WatchListGV.as_view(),name='watch_list'),

    # path('stream/',StreamPlatformAV.as_view(),name='stream_list'),
    # path('stream/<int:pk>',StreamPlatformDetail.as_view(),name='streamplatform-detail'),
    path('',include(router.urls)),

    path('<int:pk>/review_create/',ReviewCreate.as_view(),name='review_create'),
    path('<int:pk>/reviews/',ReviewList.as_view(),name='review_list'),  #All the reviews for a particular movie
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review_detail'),
   
    path('reviews/',UserReview.as_view(),name='user_review_detail'),

]
