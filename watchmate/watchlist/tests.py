from lib2to3.pgen2 import token
from urllib import response
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token 
from watchlist.api import serializers
from watchlist import models

# Create your tests here.

class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(username="example", password='Ashu@9824')
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name = 'Netflix', about = 'Streaming platform for shows and movies',
                                                                website = 'https://www.netflix.com' )

    def test_streamplatform_create(self):
        data={
            'name':'Netflix',
            'about':'Streaming platform for shows and movies',
            'website':'https://www.netflix.com'
        }
        response=self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response=self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
   
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,) ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(username="example", password='Ashu@9824')
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name = 'Netflix', about = 'Streaming platform for shows and movies',
                                                                website = 'https://www.netflix.com' )

        self.watchlist=models.WatchList.objects.create(title="example", description='example moview description', platform=self.stream,
                                                         active=True )

    def test_watchlist_create(self):
        
        data={
            'title':'Dhamal',
            'description':'Nice movie',
            'platform':self.stream,
            'active':True
        }
        response= self.client.post(reverse('movie_list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response =self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie_detail', args=(self.watchlist.id,) ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'example' )

class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(username="example", password='Ashu@9824')
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name = 'Netflix', about = 'Streaming platform for shows and movies',
                                                                website = 'https://www.netflix.com' )

        self.watchlist=models.WatchList.objects.create(title="example", description='example moview description', platform=self.stream,
                                                         active=True )

        self.watchlist2=models.WatchList.objects.create(title="example", description='example moview description', platform=self.stream,
                                                         active=True )

        self.review=models.Review.objects.create(review_user = self.user, rating = 5, text = 'Amazing moview review', 
                                                 watchlist = self.watchlist2, active = True)

    def test_review_create(self):
        data={
            'review_user':self.user,
            'rating':5,
            'text':'Amazing moview review',
            'watchlist':self.watchlist,
            'active':True
        }

        response = self.client.post(reverse('review_create', args = (self.watchlist.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        
        response = self.client.post(reverse('review_create', args = (self.watchlist.id, )), data)  #if someone add the moview for second time
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data={
            'review_user':self.user,
            'rating':5,
            'text':'Amazing moview review',
            'watchlist':self.watchlist,
            'active':True
        }

        self.client.force_authenticate(user=None )
        response = self.client.post(reverse('review_create', args = (self.watchlist.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        data={
            'review_user':self.user,
            'rating':4,
            'text':'Amazing moview review',
            'watchlist':self.watchlist,
            'active':False
        }

        response = self.client.put(reverse('review_detail', args = (self.review.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review_list', args = (self.watchlist.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse('review_detail', args = (self.review.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_review_user(self):
        response = self.client.get('/watchlist/reviews/?username'+self.user.username )
        self.assertEqual(response.status_code, status.HTTP_200_OK) 













