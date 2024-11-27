from django.http import JsonResponse
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    MovieListView, 
    CollectionView,
    CollectionDetailView,
    RequestCountView,
    RequestCountResetView
)
from middleware.request_counter import RequestCounterMiddleware


urlpatterns = [

    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('collection/', CollectionView.as_view(), name='collection-list'),
    path('collection/<uuid:pk>/', CollectionDetailView.as_view(), name='collection-detail'),

    path('request-count/', RequestCountView.as_view(), name='request-count'),
    path('request-count/reset/', RequestCountResetView.as_view(), name='request-count-reset'),
]