import uuid
from django.db import models


class UploadedFile(models.Model):
    """Store uploaded files with secure random access tokens"""
    file = models.FileField(upload_to='uploads/')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.original_filename} ({self.token})"
    
    class Meta:
        ordering = ['-uploaded_at']


class QRCode(models.Model):
    """Store generated QR codes"""
    QR_TYPE_CHOICES = [
        ('url', 'URL'),
        ('file', 'File'),
    ]
    
    qr_type = models.CharField(max_length=10, choices=QR_TYPE_CHOICES)
    content = models.TextField()  # URL or file token
    qr_image = models.ImageField(upload_to='qr_codes/')
    uploaded_file = models.ForeignKey(
        UploadedFile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='qr_codes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.qr_type} - {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']
