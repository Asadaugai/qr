"""
Simple Backend Server for Task 4 - True Security
The actual API is called server-side, browser never sees it.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import secrets
import urllib.request

# Store mappings: short_id -> actual_endpoint
url_mappings = {}


class SecureAPIHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        path = self.path.strip('/')
        
        # Check if short_id exists
        if path in url_mappings:
            actual_endpoint = url_mappings[path]
            
            try:
                # Call actual URL server-side (browser never sees it)
                with urllib.request.urlopen(actual_endpoint) as response:
                    data = response.read()
                    content_type = response.headers.get('Content-Type', 'text/html')
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(data)
                print(f"✓ Proxied: {actual_endpoint} (hidden from browser)")
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                error_html = f"<h1>Error</h1><p>{str(e)}</p>"
                self.wfile.write(error_html.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_html = "<h1>404 Not Found</h1><p>Short URL not found</p>"
            self.wfile.write(error_html.encode())
    
    def do_POST(self):
        if self.path == '/create-short':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            actual_endpoint = data.get('actual_endpoint')
            short_id = secrets.token_urlsafe(6)
            url_mappings[short_id] = actual_endpoint
            
            short_url = f"http://localhost:5000/{short_id}"
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'short_id': short_id,
                'short_url': short_url,
                'actual_endpoint': actual_endpoint
            }
            self.wfile.write(json.dumps(response).encode())
            print(f"✓ Created: {short_id} -> {actual_endpoint}")
    
    def log_message(self, format, *args):
        pass


if __name__ == '__main__':
    server = HTTPServer(('', 5000), SecureAPIHandler)
    print("=" * 60)
    print("Secure Backend Server Started")
    print("=" * 60)
    print("Server: http://localhost:5000")
    print("\nSecurity: Actual API is called server-side")
    print("Browser NEVER sees the actual endpoint!")
    print("=" * 60)
    print("\nPress Ctrl+C to stop\n")
    server.serve_forever()
