from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class ReviewCreateThrottle(UserRateThrottle):

    scope= 'review_create'

class ReviewListThrottle(UserRateThrottle):

    scope = "review_list"