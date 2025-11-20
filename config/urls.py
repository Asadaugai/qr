"""
Main URL routing - Like FastAPI's app.include_router()
"""
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),  # All our endpoints start with /api/
]
