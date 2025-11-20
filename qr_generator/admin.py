from django.contrib import admin
from .models import UploadedFile, QRCode


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'token', 'uploaded_at']
    readonly_fields = ['token', 'uploaded_at']
    search_fields = ['original_filename', 'token']


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['qr_type', 'content', 'created_at']
    list_filter = ['qr_type', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['content']
