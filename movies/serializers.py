from rest_framework import serializers
from .models import Collection, Movie
import uuid

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'uuid', 'movies']
        read_only_fields = ['uuid'] 
        
    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        collection = Collection.objects.create(
            **validated_data, 
            uuid=uuid.uuid4(),
            user=self.context['request'].user
        )
        
        for movie_data in movies_data:
            Movie.objects.create(collection=collection, **movie_data)
        
        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', None)
        
        # Update collection details
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        # If movies are provided, clear existing and create new
        if movies_data is not None:
            instance.movies.all().delete()
            for movie_data in movies_data:
                Movie.objects.create(collection=instance, **movie_data)
        
        return instance