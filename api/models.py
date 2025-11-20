"""
Models - Like Pydantic models but for database
Think: SQLAlchemy models in FastAPI
"""
from django.db import models
import secrets


class ShortURL(models.Model):
    """Store short URL mappings - Like a database table"""
    short_id = models.CharField(max_length=16, unique=True, db_index=True)
    actual_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    access_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.short_id} -> {self.actual_url}"
    
    @staticmethod
    def generate_short_id():
        """Generate unique short ID"""
        while True:
            short_id = secrets.token_urlsafe(6)
            if not ShortURL.objects.filter(short_id=short_id).exists():
                return short_id
