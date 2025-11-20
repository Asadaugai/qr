import qrcode
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.urls import reverse
from .models import UploadedFile, QRCode
from .forms import URLQRForm, FileQRForm


def home(request):
    """Home page with both forms"""
    url_form = URLQRForm()
    file_form = FileQRForm()
    
    context = {
        'url_form': url_form,
        'file_form': file_form,
    }
    return render(request, 'qr_generator/home.html', context)


def generate_url_qr(request):
    """Generate QR code from URL"""
    if request.method == 'POST':
        form = URLQRForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            
            # Generate QR code
            qr_image = create_qr_code(url)
            
            # Save to database
            qr_code = QRCode.objects.create(
                qr_type='url',
                content=url,
            )
            qr_code.qr_image.save(
                f'qr_{qr_code.id}.png',
                ContentFile(qr_image),
                save=True
            )
            
            return redirect('qr_result', qr_id=qr_code.id)
    
    return redirect('home')


def generate_file_qr(request):
    """Generate QR code from uploaded file"""
    if request.method == 'POST':
        form = FileQRForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            
            # Save the uploaded file with secure token
            file_obj = UploadedFile.objects.create(
                file=uploaded_file,
                original_filename=uploaded_file.name
            )
            
            # Create secure download URL using token
            download_url = request.build_absolute_uri(
                reverse('download_file', kwargs={'token': file_obj.token})
            )
            
            # Generate QR code with the secure URL
            qr_image = create_qr_code(download_url)
            
            # Save QR code to database
            qr_code = QRCode.objects.create(
                qr_type='file',
                content=download_url,
                uploaded_file=file_obj
            )
            qr_code.qr_image.save(
                f'qr_{qr_code.id}.png',
                ContentFile(qr_image),
                save=True
            )
            
            return redirect('qr_result', qr_id=qr_code.id)
    
    return redirect('home')


def qr_result(request, qr_id):
    """Display generated QR code"""
    qr_code = get_object_or_404(QRCode, id=qr_id)
    
    context = {
        'qr_code': qr_code,
    }
    return render(request, 'qr_generator/result.html', context)


def download_file(request, token):
    """Download file using secure token"""
    uploaded_file = get_object_or_404(UploadedFile, token=token)
    
    try:
        return FileResponse(
            uploaded_file.file.open('rb'),
            as_attachment=True,
            filename=uploaded_file.original_filename
        )
    except FileNotFoundError:
        raise Http404("File not found")


def create_qr_code(data):
    """Helper function to generate QR code image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()
