import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from .CONSTANTS.config import CONFIG


class HTTPHandler(SimpleHTTPRequestHandler):
    """Simple HTTPS handler to serve from public directory"""

    def __init__(self, *args,
                 **kwargs):
        root_path = os.path.join(os.getcwd(), "public")
        super().__init__(*args, directory=root_path, **kwargs)

def serve():
    """Run basic web server in directory"""
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HTTPHandler)
    CONFIG["base_url"] = "/"
    print("Stating server on http://127.0.0.1:8000.\n Close with ^C")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nClosing server")
        exit(0)