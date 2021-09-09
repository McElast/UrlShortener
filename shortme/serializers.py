from rest_framework import serializers

from .models import ShortenUrl


class ShortenUrlSerializer(serializers.ModelSerializer):
    """
    Использует модель ShortenUrl для сериализации данных.
    """
    class Meta:
        model = ShortenUrl
        fields = ['original_url', 'short_url_part', 'added']
        lookup_field = 'short_url_part'
