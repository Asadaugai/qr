"""
Views - Like FastAPI route functions
Each class is like a FastAPI router endpoint
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import requests
import qrcode
import io
import base64

from .models import ShortURL
from .serializers import CreateShortURLRequest, ShortURLResponse, GenerateQRRequest


class CreateShortURLView(APIView):
    """
    POST /api/create-short
    Like: @app.post("/api/create-short")
    """
    def post(self, request):
        serializer = CreateShortURLRequest(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        actual_url = serializer.validated_data['actual_url']
        short_id = ShortURL.generate_short_id()
        
        short_url_obj = ShortURL.objects.create(
            short_id=short_id,
            actual_url=actual_url
        )
        
        response_serializer = ShortURLResponse(
            short_url_obj,
            context={'request': request}
        )
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ProxyShortURLView(APIView):
    """
    GET /api/short/<short_id>
    Like: @app.get("/api/short/{short_id}")
    Proxies to actual URL (browser never sees real URL)
    """
    def get(self, request, short_id):
        short_url_obj = get_object_or_404(ShortURL, short_id=short_id)
        
        # Increment access count
        short_url_obj.access_count += 1
        short_url_obj.save(update_fields=['access_count'])
        
        try:
            # Fetch actual URL server-side
            response = requests.get(short_url_obj.actual_url)
            
            # Return the actual content
            return HttpResponse(
                response.content,
                content_type=response.headers.get('Content-Type', 'text/html'),
                status=response.status_code
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch URL: {str(e)}'},
                status=status.HTTP_502_BAD_GATEWAY
            )


class GenerateQRView(APIView):
    """
    POST /api/generate-qr
    Like: @app.post("/api/generate-qr")
    Generates QR code and returns as base64 image
    """
    def post(self, request):
        serializer = GenerateQRRequest(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data['data']
        task_type = serializer.validated_data['task_type']
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return Response({
            'qr_code': f'data:image/png;base64,{img_base64}',
            'data': data,
            'task_type': task_type
        })


class BasicQRView(APIView):
    """POST /api/basic-qr - Generate basic QR code"""
    def post(self, request):
        data = request.data.get('data', 'https://www.python.org')
        description = request.data.get('description')
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        response_data = {
            'qr_code': f'data:image/png;base64,{img_base64}',
            'data': data
        }
        
        if description:
            response_data['description'] = description
        
        return Response(response_data)


class PDFQRView(APIView):
    """POST /api/pdf-qr - Generate PDF QR code"""
    def post(self, request):
        pdf_url = request.data.get('pdf_url')
        description = request.data.get('description')
        
        if not pdf_url:
            return Response(
                {'error': 'pdf_url is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(pdf_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        response_data = {
            'qr_code': f'data:image/png;base64,{img_base64}',
            'pdf_url': pdf_url
        }
        
        if description:
            response_data['description'] = description
        
        return Response(response_data)


class APIQRView(APIView):
    """POST /api/api-qr - Generate API endpoint QR code"""
    def post(self, request):
        api_endpoint = request.data.get('api_endpoint')
        description = request.data.get('description')
        
        if not api_endpoint:
            return Response(
                {'error': 'api_endpoint is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(api_endpoint)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        response_data = {
            'qr_code': f'data:image/png;base64,{img_base64}',
            'api_endpoint': api_endpoint
        }
        
        if description:
            response_data['description'] = description
        
        return Response(response_data)


class SecureQRView(APIView):
    """POST /api/secure-qr - Generate secure QR code with hidden URL"""
    def post(self, request):
        actual_url = request.data.get('actual_url')
        description = request.data.get('description')
        
        if not actual_url:
            return Response(
                {'error': 'actual_url is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create short URL
        short_id = ShortURL.generate_short_id()
        short_url_obj = ShortURL.objects.create(
            short_id=short_id,
            actual_url=actual_url
        )
        
        short_url = request.build_absolute_uri(f'/api/short/{short_id}')
        
        # Generate QR code with short URL
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(short_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        response_data = {
            'qr_code': f'data:image/png;base64,{img_base64}',
            'short_url': short_url,
            'short_id': short_id,
            'actual_url': actual_url
        }
        
        if description:
            response_data['description'] = description
        
        return Response(response_data)


class HealthCheckView(APIView):
    """GET /api/health - Health check"""
    def get(self, request):
        return Response({
            'status': 'healthy',
            'total_short_urls': ShortURL.objects.count()
        })
