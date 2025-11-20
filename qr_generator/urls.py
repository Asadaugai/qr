from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate/url/', views.generate_url_qr, name='generate_url_qr'),
    path('generate/file/', views.generate_file_qr, name='generate_file_qr'),
    path('result/<int:qr_id>/', views.qr_result, name='qr_result'),
    path('download/<uuid:token>/', views.download_file, name='download_file'),
]
