# QR Code Generator - Frontend

Clean and simple frontend for the QR Code Generator API.

## Features

✅ 4 QR code types: Basic, PDF, API, Secure
✅ Clean, modern UI
✅ Real-time QR code generation
✅ Download QR codes
✅ Optional descriptions
✅ Responsive design
✅ Error handling

## How to Use

### 1. Start Django Backend
```bash
python manage.py runserver
```

### 2. Open Frontend
Open `frontend/index.html` in your browser

Or use a simple HTTP server:
```bash
cd frontend
python -m http.server 8080
```
Then open: `http://localhost:8080`

## File Structure

```
frontend/
  index.html    # Main HTML structure
  style.css     # Styling
  script.js     # JavaScript logic
  README.md     # This file
```

## Usage

1. **Select QR Type** - Click one of the 4 buttons
2. **Enter Data** - Fill in the required field
3. **Add Description** (Optional) - Add context for your QR code
4. **Generate** - Click "Generate QR Code"
5. **Download** - Save the QR code image

## API Endpoints Used

- `POST /api/basic-qr` - Basic URL QR code
- `POST /api/pdf-qr` - PDF link QR code
- `POST /api/api-qr` - API endpoint QR code
- `POST /api/secure-qr` - Secure URL QR code

## Browser Compatibility

✅ Chrome, Firefox, Safari, Edge (latest versions)

## Notes

- Make sure Django backend is running on `http://localhost:8000`
- If using different port, update `API_BASE_URL` in `script.js`
- For production, enable CORS in Django settings
