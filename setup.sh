#!/bin/bash
# natiq-ultimate v6.0 Setup Script

echo "🧠 natiq-ultimate v6.0 Setup"
echo "============================="

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version detected"
else
    echo "❌ Python 3.8 or higher is required"
    echo "📦 Install Python 3.8+ from: https://www.python.org/downloads/"
    exit 1
fi

# Create project structure
echo "📁 Creating project structure..."
mkdir -p public/assets/css public/assets/js api

# Copy files (assuming files are in current directory)
echo "📦 Copying files..."

# Check if files exist
if [ -f "index.html" ]; then
    cp index.html public/
    echo "✅ index.html copied"
fi

if [ -f "dashboard.html" ]; then
    cp dashboard.html public/
    echo "✅ dashboard.html copied"
fi

if [ -f "style.css" ]; then
    cp style.css public/assets/css/
    echo "✅ style.css copied"
fi

if [ -f "app.js" ]; then
    cp app.js public/assets/js/
    echo "✅ app.js copied"
fi

if [ -f "api/index.py" ]; then
    echo "✅ API files already exist"
fi

# Create default API files if they don't exist
if [ ! -f "api/index.py" ]; then
    echo "⚡ Creating default API structure..."
    
    # Create minimal API file
    cat > api/index.py << 'PYEOF'
"""
natiq-ultimate v6.0 - Minimal API
"""
import json
from http.server import BaseHTTPRequestHandler
from datetime import datetime

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/health':
            self.send_json_response({
                'status': 'active',
                'system': 'natiq-ultimate',
                'version': '6.0.0',
                'timestamp': datetime.now().isoformat()
            })
        else:
            self.send_error(404, "Not Found")
    
    def send_json_response(self, data):
        response = json.dumps(data, ensure_ascii=False)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response.encode())

if __name__ == "__main__":
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 3000), Handler)
    print("🚀 Server running on http://localhost:3000")
    server.serve_forever()
PYEOF
    echo "✅ Created minimal API"
fi

# Create vercel.json
if [ ! -f "vercel.json" ]; then
    cat > vercel.json << 'JSONEOF'
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/",
      "dest": "/public/index.html"
    },
    {
      "src": "/dashboard.html",
      "dest": "/public/dashboard.html"
    },
    {
      "src": "/assets/(.*)",
      "dest": "/public/assets/$1"
    },
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
JSONEOF
    echo "✅ Created vercel.json"
fi

echo ""
echo "🎉 Setup completed!"
echo ""
echo "🚀 To run locally:"
echo "   python api/index.py"
echo ""
echo "🌐 Then open: http://localhost:3000"
echo ""
echo "📦 To deploy to Vercel:"
echo "   npm i -g vercel"
echo "   vercel"
echo ""
echo "🧠 natiq-ultimate v6.0 is ready!"
