# QR Code Generator

A simple Django app to generate QR codes from URLs or uploaded files.

## Features

- ✅ Generate QR codes from any URL
- ✅ Upload files and generate QR codes with secure random links (UUID tokens)
- ✅ Download generated QR codes as PNG images
- ✅ Clean, modern UI with gradient design
- ✅ File paths are hidden - only secure tokens are exposed

## How to Run

### 1. Activate Virtual Environment
```bash
qr\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Database Migrations
```bash
python manage.py migrate
```

### 4. Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

### 5. Start Development Server
```bash
python manage.py runserver
```

### 6. Open in Browser
Visit: http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
qr_project/          # Main project settings
├── settings.py      # Django configuration
├── urls.py          # Main URL routing
└── wsgi.py          # WSGI application

qr_generator/        # QR generator app
├── models.py        # Database models (UploadedFile, QRCode)
├── views.py         # View logic
├── forms.py         # Form definitions
├── urls.py          # App URL routing
├── admin.py         # Admin panel configuration
└── templates/       # HTML templates
    └── qr_generator/
        ├── base.html
        ├── home.html
        └── result.html

manage.py            # Django management script
requirements.txt     # Python dependencies
```

## How It Works

### URL QR Code:
1. User enters a URL
2. QR code is generated with that URL
3. User can download the QR code

### File QR Code (Secure):
1. User uploads a file
2. File is saved with a random UUID token (e.g., `a3f2b1c4-...`)
3. QR code contains: `http://yoursite.com/download/a3f2b1c4-...`
4. Original file path is NEVER exposed
5. File can only be accessed via the secure token

## Security Features

- Files are accessed via UUID tokens, not direct paths
- Original filenames are preserved but paths are hidden
- Each file gets a unique, unguessable token
- No directory traversal vulnerabilities

## Technologies Used

- Django 5.2
- qrcode library with PIL
- SQLite database
- Pure CSS (no external frameworks)
