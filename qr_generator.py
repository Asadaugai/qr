
import qrcode
import secrets
from pathlib import Path
import requests

def generate_qr_code(data: str, output_path: str) -> str:
    """
    Core function to generate a QR code.
    
    Args:
        data: The data to encode in the QR code
        output_path: Path where the QR code image will be saved
        
    Returns:
        Path to the generated QR code image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    
    return output_path


def task_1_basic_qr(data: str, output_path: str = "task1_basic_qr.png") -> str:
    """
    Task 1: Generate a basic QR code.
    
    Args:
        data: Text or URL to encode
        output_path: Output file path
        
    Returns:
        Path to generated QR code
    """
    return generate_qr_code(data, output_path)


def task_2_pdf_qr(pdf_url: str, output_path: str = "task2_pdf_qr.png") -> str:
    """
    Task 2: Generate a QR code that opens a PDF file when scanned.
    
    Args:
        pdf_url: URL or local path to the PDF file
        output_path: Output file path
        
    Returns:
        Path to generated QR code
    """
    # If it's a local file, convert to file:// URL
    if Path(pdf_url).exists():
        pdf_url = f"file:///{Path(pdf_url).absolute().as_posix()}"
    
    return generate_qr_code(pdf_url, output_path)


def task_3_api_qr(api_endpoint: str, output_path: str = "task3_api_qr.png") -> str:
    """
    Task 3: Generate a QR code that calls an API endpoint when scanned.
    
    Args:
        api_endpoint: The API endpoint URL
        output_path: Output file path
        
    Returns:
        Path to generated QR code
    """
    return generate_qr_code(api_endpoint, output_path)


def task_4_secure_api_qr(
    actual_endpoint: str,
    output_path: str = "task4_secure_api_qr.png"
) -> dict:
    """
    Task 4: Generate a QR code with a short endpoint that hides the actual API.
    
    Creates short URL via backend server that proxies API calls.
    Browser NEVER sees the actual endpoint - true security!
    
    Args:
        actual_endpoint: The actual API endpoint to hide
        output_path: Output file path for QR code
        
    Returns:
        Dictionary with QR path, short URL, and actual endpoint
    """
    try:
        import requests
        
        # Create short URL via backend server
        response = requests.post(
            "http://localhost:5000/create-short",
            json={"actual_endpoint": actual_endpoint}
        )
        
        if response.status_code == 201:
            data = response.json()
            short_url = data['short_url']
            
            # Generate QR code with short URL
            qr_path = generate_qr_code(short_url, output_path)
            
            return {
                'success': True,
                'qr_path': qr_path,
                'short_url': short_url,
                'actual_endpoint': actual_endpoint
            }
        else:
            return {
                'success': False,
                'error': 'Failed to create short URL'
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': 'Backend not running. Start: python simple_backend.py'
        }


if __name__ == "__main__":

    
    # Task 1: Basic QR Code
    print("\n[Task 1] Generate a basic QR code")
    qr1 = task_1_basic_qr("https://www.python.org")
    print(f"✓ Generated: {qr1}")
    print(f"  Data: https://www.python.org")
    
    # Task 2: PDF QR Code
    print("\n[Task 2] Generate QR code for PDF")
    pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    qr2 = task_2_pdf_qr(pdf_url)
    print(f"✓ Generated: {qr2}")
    print(f"  PDF URL: {pdf_url}")
    
    # Task 3: API Endpoint QR Code
    print("\n[Task 3] Generate QR code for API endpoint")
    api_endpoint = "https://jsonplaceholder.typicode.com/posts/1"
    qr3 = task_3_api_qr(api_endpoint)
    print(f"✓ Generated: {qr3}")
    print(f"  API Endpoint: {api_endpoint}")
    
    # Task 4: Secure API QR Code with Short Endpoint
    print("\n[Task 4] Generate secure QR code with short endpoint")
    actual_url = "https://www.google.com"  # Use a real website
    result = task_4_secure_api_qr(actual_url)
    
    if result.get('success'):
        print(f"✓ Generated: {result['qr_path']}")
        print(f"  Short URL: {result['short_url']}")
        print(f"  Actual URL (hidden): {result['actual_endpoint']}")
        print(f"  Security: Actual endpoint is hidden from QR code!")
        print(f"  Note: Backend proxies the actual page")
    else:
        print(f"✗ Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("All tasks completed!")
    print("=" * 60)
