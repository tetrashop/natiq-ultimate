from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

os.chdir('public')
httpd = HTTPServer(('0.0.0.0', 3000), SimpleHTTPRequestHandler)
print("Server running on http://0.0.0.0:3000")
httpd.serve_forever()
