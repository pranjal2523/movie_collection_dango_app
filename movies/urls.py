from django.urls import path
from .views import (
    MovieListView,
    CollectionView,
    CollectionDetailView,
    RequestCountView,
    RequestCountResetView
)


urlpatterns = [

    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('collection/', CollectionView.as_view(), name='collection-list'),
    path(
        'collection/<uuid:pk>/',
        CollectionDetailView.as_view(),
        name='collection-detail'
    ),
    path('request-count/', RequestCountView.as_view(), name='request-count'),
    path(
        'request-count/reset/',
        RequestCountResetView.as_view(),
        name='request-count-reset'
    ),
]
