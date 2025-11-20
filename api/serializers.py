"""
Serializers - Like Pydantic models in FastAPI
Used for request/response validation
"""
from rest_framework import serializers
from .models import ShortURL


class CreateShortURLRequest(serializers.Serializer):
    """Request body for creating short URL - Like FastAPI's BaseModel"""
    actual_url = serializers.URLField(required=True)


class ShortURLResponse(serializers.ModelSerializer):
    """Response for short URL - Like FastAPI's response_model"""
    short_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ShortURL
        fields = ['short_id', 'short_url', 'actual_url', 'created_at']
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/short/{obj.short_id}')
        return f'/api/short/{obj.short_id}'


class GenerateQRRequest(serializers.Serializer):
    """Request for generating QR code"""
    data = serializers.CharField(required=True)
    task_type = serializers.ChoiceField(
        choices=['basic', 'pdf', 'api', 'secure'],
        default='basic'
    )
