import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Collection, Movie
from .serializers import CollectionSerializer
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.http import JsonResponse
from middleware.request_counter import RequestCounterMiddleware


# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MovieListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # get the page number from query params
            page = request.query_params.get('page', 1)

            # Configure retry strategy
            retry_strategy = Retry(
                total=3,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"]
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            
            # Create session with retry mechanism
            session = requests.Session()
            session.mount("https://", adapter)
            
            url = settings.MOVIE_API_URL + f'?page={page}' 
            # Make request with authentication and SSL verification bypass
            response = session.get(
                url,
                auth=(
                    settings.MOVIE_API_USERNAME,
                    settings.MOVIE_API_PASSWORD
                ),
                params=request.query_params,
                verify=False
            )
            response.raise_for_status()
            return Response(response.json())

        except requests.exceptions.SSLError as ssl_error:
            return Response({
                'error': 'SSL Certificate Verification Failed',
                'details': str(ssl_error)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except requests.exceptions.ConnectionError as conn_error:
            return Response({
                'error': 'Connection Error',
                'details': str(conn_error)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except requests.exceptions.Timeout as timeout_error:
            return Response({
                'error': 'Request Timeout',
                'details': str(timeout_error)
            }, status=status.HTTP_408_REQUEST_TIMEOUT)

        except requests.exceptions.RequestException as e:
            return Response({
                'error': 'Movie API Request Failed',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        collections = Collection.objects.filter(user=request.user)
        collection_serializer = CollectionSerializer(collections, many=True)

        # Calculate top 3 favorite genres
        movie_genres = Movie.objects.filter(
            collection__user=request.user
        ).values('genres')
        genre_counts = {}
        for movie in movie_genres:
            genres = movie['genres'].split(',') if movie['genres'] else []
            for genre in genres:
                genre_counts[genre.strip()] = genre_counts.get(genre.strip(), 0) + 1

        top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        favorite_genres = ', '.join([genre for genre, _ in top_genres])

        return Response({
            'is_success': True,
            'data': {
                'collections': collection_serializer.data,
                'favourite_genres': favorite_genres
            }
        })

    def post(self, request):
        serializer = CollectionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            collection = serializer.save()
            return Response(
                {'collection_uuid': collection.uuid},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            collection = Collection.objects.get(uuid=pk, user=request.user)
            serializer = CollectionSerializer(collection)
            return Response(serializer.data)
        except Collection.DoesNotExist:
            return Response(
                {'message': "No collection found!"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            collection = Collection.objects.get(uuid=pk, user=request.user)
            serializer = CollectionSerializer(
                collection, 
                data=request.data, 
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Collection.DoesNotExist:
            return Response(
                {'message': "No collection found!"},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            collection = Collection.objects.get(uuid=pk, user=request.user)
            collection.delete()
            return Response(
                {'message': "Collection deleted successfully!"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Collection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RequestCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return the current request count
        return JsonResponse({
            'requests': RequestCounterMiddleware.get_count()
        })


class RequestCountResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Reset the request count to 0
        RequestCounterMiddleware.reset_count()
        return JsonResponse({
            'message': 'request count reset successfully'
        })
