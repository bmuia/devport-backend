from rest_framework import serializers
from .models import App, AccessToken

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'title', 'consumer_key', 'consumer_secret', 'created_at']


class AccessTokenSerializer(serializers.ModelSerializer):
    app_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = AccessToken
        fields = ['id', 'token','created_at','app_title']


