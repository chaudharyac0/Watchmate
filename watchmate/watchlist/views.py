# from django.shortcuts import render,redirect
# from .models import Movie
# from django.http import JsonResponse

# # Create your views here.
# def movielist(request):
#     movie_list=Movie.objects.all()
#     context={
#         'movie_list':list(movie_list.values())
#     }

#     return JsonResponse(context)
    
# def moviedetail(request,pk):
#     detail=Movie.objects.get(pk=pk)
#     context={
#         'name':detail.name,
#         'description':detail.description,
#         'active':detail.active
#     }

#     return JsonResponse(context)
    