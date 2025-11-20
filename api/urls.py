"""
API URLs - Like FastAPI's APIRouter
Maps URLs to views (endpoints)
"""
from django.urls import path
from . import views

urlpatterns = [
    # QR Code endpoints
    path('basic-qr', views.BasicQRView.as_view(), name='basic-qr'),
    path('pdf-qr', views.PDFQRView.as_view(), name='pdf-qr'),
    path('api-qr', views.APIQRView.as_view(), name='api-qr'),
    path('secure-qr', views.SecureQRView.as_view(), name='secure-qr'),
    
    # Secure URL endpoints
    path('create-short', views.CreateShortURLView.as_view(), name='create-short'),
    path('short/<str:short_id>', views.ProxyShortURLView.as_view(), name='proxy-short'),
    
    # File endpoints
    path('files/<str:file_id>', views.FileDownloadView.as_view(), name='file-download'),
    
    # General QR generator
    path('generate-qr', views.GenerateQRView.as_view(), name='generate-qr'),
    
    # Health check
    path('health', views.HealthCheckView.as_view(), name='health'),
]
