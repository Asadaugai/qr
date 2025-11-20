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


class UploadedFile(models.Model):
    """Store uploaded files (PDFs, documents, etc.)"""
    file_id = models.CharField(max_length=16, unique=True, db_index=True)
    file = models.FileField(upload_to='uploads/')
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()  # in bytes
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.file_id} - {self.original_filename}"
    
    @staticmethod
    def generate_file_id():
        """Generate unique file ID"""
        while True:
            file_id = secrets.token_urlsafe(8)
            if not UploadedFile.objects.filter(file_id=file_id).exists():
                return file_id
