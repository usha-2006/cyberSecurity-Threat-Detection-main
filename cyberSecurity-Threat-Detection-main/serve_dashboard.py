#!/usr/bin/env python3
"""
Simple HTTP server to serve the dashboard and avoid CORS issues.
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time

import os

# Allow overriding port via environment variable to avoid conflicts
PORT = int(os.environ.get('DASHBOARD_PORT', '3001'))

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_dashboard_server():
    """Start the dashboard HTTP server."""
    print(f"🚀 Starting Dashboard Server on http://localhost:{PORT}")
    print("=" * 50)
    
    # Change to dashboard directory
    dashboard_dir = os.path.join(os.path.dirname(__file__), 'dashboard')
    os.chdir(dashboard_dir)
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"✅ Dashboard server running at http://localhost:{PORT}")
        print(f"📁 Serving files from: {dashboard_dir}")
        print(f"🌐 Open your browser to: http://localhost:{PORT}")
        print("=" * 50)
        
        # Open browser automatically after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open(f'http://localhost:{PORT}')
            print("🌐 Browser opened automatically!")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Dashboard server stopped.")

if __name__ == "__main__":
    start_dashboard_server()
