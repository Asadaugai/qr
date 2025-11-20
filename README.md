# QR Code Generator with Analytics

A simple Django app to generate QR codes from URLs or uploaded files with comprehensive analytics tracking.

## Features

- ✅ Generate QR codes from any URL
- ✅ Upload files and generate QR codes with secure random links (UUID tokens)
- ✅ Download generated QR codes as PNG images
- ✅ **Track comprehensive analytics:**
  - Total scans
  - Unique users
  - Countries & Cities (IP geolocation)
  - Device types (iPhone, Android, Desktop, etc.)
  - Browsers & Operating Systems
  - Time of day distribution
  - Traffic sources
- ✅ Beautiful analytics dashboard
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


## Analytics Features

### What Gets Tracked:
When someone scans a QR code (for files), the system automatically tracks:

1. **Total Scans** - Every time the QR is scanned
2. **Unique Users** - Based on IP + User Agent hash
3. **Location** - Country and City (using IP geolocation)
4. **Device Info** - iPhone, Android, Desktop, Tablet
5. **Browser** - Chrome, Safari, Firefox, etc.
6. **Operating System** - iOS, Android, Windows, etc.
7. **Time of Day** - Hourly distribution of scans
8. **Traffic Source** - Where the scan came from (usually "Direct" for QR codes)

### How to View Analytics:
1. Generate a file QR code
2. On the result page, click "📊 View Analytics"
3. See comprehensive stats and charts

### Privacy Note:
- IP addresses are stored but only used for geolocation and unique user counting
- User identifiers are MD5 hashed (IP + User Agent)
- No personal information is collected

## API Used:
- **ipapi.co** - Free IP geolocation (no API key needed for basic usage)
- Limit: 1,000 requests/day on free tier

## New Dependencies:
- `requests` - For making HTTP calls to geolocation API
- `user-agents` - For parsing device/browser information
