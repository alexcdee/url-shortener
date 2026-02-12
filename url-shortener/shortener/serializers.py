from rest_framework import serializers
from .models import UrlData

class UrlDataSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = UrlData
        fields = ['id', 'url', 'slug', 'created', 'short_url']
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/{obj.slug}')
        return f'/{obj.slug}'
    