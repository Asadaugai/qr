# QR Code Generator - All 4 Tasks

Simple Python implementation for generating QR codes.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python qr_generator.py
```

## Tasks

### Task 1: Basic QR Code
Generate a simple QR code for any text or URL.

### Task 2: PDF QR Code
Generate a QR code that opens a PDF file when scanned.

### Task 3: API Endpoint QR Code
Generate a QR code that calls an API endpoint when scanned.

### Task 4: Secure API QR Code ⭐
Generate a QR code with a short URL that hides the actual API endpoint for security.

**How it works:**
- Backend server creates short URL (e.g., `http://localhost:5000/abc123`)
- QR code contains only the short URL
- When scanned, backend calls actual API **server-side**
- Browser NEVER sees the actual endpoint
- **True security** - actual API is completely hidden!

## Output Files

- `task1_basic_qr.png` - Basic QR code
- `task2_pdf_qr.png` - PDF QR code
- `task3_api_qr.png` - API endpoint QR code
- `task4_secure_api_qr.png` - Secure API QR code with hidden endpoint

## Example Usage

```python
from qr_generator import task_4_secure_api_qr

# Task 4: Create secure QR code with short URL
result = task_4_secure_api_qr("https://api.example.com/sensitive")

if result['success']:
    print(result['short_url'])  # https://tinyurl.com/abc123
    print(result['actual_endpoint'])  # https://api.example.com/sensitive
```

**Security Benefits:**
- ✅ Backend calls API server-side (not browser redirect)
- ✅ Browser never sees actual endpoint
- ✅ True security - endpoint completely hidden
- ✅ Uses Python's built-in http.server (no Flask/Django)
